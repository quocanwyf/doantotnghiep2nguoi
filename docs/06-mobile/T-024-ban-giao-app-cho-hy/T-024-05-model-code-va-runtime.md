# T-024 — 05. Model, file code và runtime tham chiếu

## 1. Model cần chuyển/tải

**Pack:** InsightFace `buffalo_sc.zip` (14.969.382 byte). SHA-256:

```text
57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72
```

| File trong pack | Nhiệm vụ | SHA-256 |
| --- | --- | --- |
| `det_500m.onnx` — SCRFD-500MF | Face detection và landmarks cho alignment | `5e4447f50245bbd7966bd6c0fa52938c61474a04ec7def48753668a9d8b4ea3a` |
| `w600k_mbf.onnx` — MobileFaceNet | Face embedding 512 chiều | `9cc6e4a75f0e2bf0b1aed94578f144d15175f357bdc05e815e5c4a02b319eb4f` |

Nguồn đã audit: [model zoo](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md), [release model-zoo](https://github.com/deepinsight/insightface/releases/tag/model-zoo); đối chiếu [external-assets A-002](../../00-project/external-assets.md). Weight được nguồn giới hạn cho nghiên cứu phi thương mại; quyền code không tự là quyền tái phân phối weight. Không commit pack/ONNX lên repo công khai.

**Trạng thái chuyển:** chưa xác nhận Hy đã nhận/tải và kiểm hash. Bộ MD này cung cấp danh mục/cách kiểm, không chứa weight. Không có “model tối ưu mới” sau fine-tune; đóng góp hiện tại là selective S4, nghiên cứu S8 decision và cách tích hợp/đánh giá.

## 2. Config/runtime đã dùng trong nghiên cứu

| Thành phần | Mốc tham chiếu |
| --- | --- |
| Runtime | Python 3.12.2; InsightFace 0.7.3; ONNX Runtime 1.20.1; CPUExecutionProvider. |
| Module | Chỉ detection + recognition của buffalo_sc. |
| Detector | `det_size=(640,640)`, `det_thresh=0.5`, `max_num=0`, metric default. |
| Embedding | InsightFace recognition alignment/preprocess + normalized vector 512 chiều. |
| P2 | τ/δ ở [contract AI](T-024-04-s4-s8-va-ai-contract.md), không retune. |
| S8 | Selected cosine ≥θ; T-023 θ=0.23 là research reference, chưa freeze demo. |

Các số runtime là mốc đã ghi, không cam kết có sẵn dependency trên máy Hy hoặc khả năng chạy trực tiếp trên mobile. Hy chọn on-device/service theo thiết bị và ghi quyết định; nếu thay provider/runtime/preprocessing, kiểm parity và timing thiết bị trước kết luận tương đương.

## 3. Code nào đọc/tái dùng

| File / symbol | Công dụng | Lưu ý |
| --- | --- | --- |
| [t011_xqlfw_baseline.py](../../../scripts/t011_xqlfw_baseline.py) — `prepare_pack` | Lấy đúng hai ONNX từ ZIP vào `cache/models/buffalo_sc`, trả hash. | App cần startup hash guard; không tự tải pack khác khi thiếu weight. |
| [t011_xqlfw_r50_comparison.py](../../../scripts/t011_xqlfw_r50_comparison.py) — `unit` | Validate + L2-normalize embedding. | Tái dùng helper không có nghĩa đổi sang R50. |
| [t017_s4_run.py](../../../scripts/t017_s4_run.py) — `get_faces`, `select_p1`, `select_p2`, `TAU`, `DELTA` | Decode/detect/align/embedding và selection nhiều mặt. | P2 cần ≥2 scores; dispatcher một mặt phải được nối riêng. |
| [t023_development.py](../../../scripts/t023_development.py) — `features`, `score_split` | Ví dụ load đúng pack, hash, reference/scene embedding và cosine/P2. | `score_split` đọc BFW locked benchmark; không phải API camera/roster app. |
| [t022_s8_development.py](../../../scripts/t022_s8_development.py) — `threshold_row` | Rule score ≥θ và cách báo genuine/ordinary/hard negative/pipeline. | Code phân tích offline, không trả PASS/check-in. |
| [t023_evaluation.py](../../../scripts/t023_evaluation.py) | Một lượt frozen holdout T-023; report đã lưu. | Không chạy lại để dựng app/tune; không sửa runner/hash cũ. |
| [t020_s4_s8_replay.py](../../../scripts/t020_s4_s8_replay.py) | Replay score T-017 với historical S8 threshold. | Dùng hiểu failure/history; không dùng làm cấu hình S8 mới nhất. |

Các script import helper lẫn nhau; copy riêng một file có thể thiếu dependency. Giữ checkout nghiên cứu khi đọc/tái dùng, rồi tách adapter app có version/tests riêng. Không quảng bá chúng là SDK mobile đã đóng gói.

## 4. Cách khởi tạo tối thiểu cho adapter Python

Đoạn sau minh họa phần load đang dùng trong code nghiên cứu; **không phải command chạy app hoặc experiment mới**. Cần môi trường dependency phù hợp và model ZIP đã nhận/kiểm hash. `cache_path` là thư mục model ngoài Git do Hy đặt.

```python
from pathlib import Path
from zipfile import ZipFile
from insightface.app import FaceAnalysis
from t011_xqlfw_baseline import prepare_pack
from t023_development import EXPECTED_ONNX

cache_path = Path("local-model-cache")
with ZipFile("buffalo_sc.zip") as model_zip:
    root, hashes = prepare_pack(model_zip, cache_path)
if hashes != EXPECTED_ONNX:
    raise ValueError("Unexpected detector/encoder weights")
app = FaceAnalysis(name="buffalo_sc", root=str(root),
                   allowed_modules=["detection", "recognition"],
                   providers=["CPUExecutionProvider"])
app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
```

Trong layout script hiện tại, các helper ở `scripts/`; đoạn import cần adapter đặt trong layout import phù hợp hoặc cấu hình đường dẫn module. Sau startup, adapter decode reference/observation, dùng `get_faces`, normalize, tính cosine, dispatch S4 rồi S8 theo [contract](T-024-04-s4-s8-va-ai-contract.md). App quản lý business/retry/write riêng.

Kiểm file nhận trên Windows bằng `Get-FileHash -Algorithm SHA256 -LiteralPath '<duong-dan-file>'`; so pack và từng ONNX với bảng trên. Hy lưu local asset path/version trong môi trường riêng, không ghi đường dẫn ảnh cá nhân/secret lên Git.

## 5. Evidence đủ để bắt đầu app, chưa phải kết quả app

[T-023 report](../../05-evaluation/T-023-encoder-evaluation-result.md) và [freeze](../../05-evaluation/T-023-evaluation-freeze.md) là nguồn kết quả/model/code phiên bản nghiên cứu. 55/55 selected genuine được accept; 30/38 hard negative bị reject, 8/38 còn accept tại θ=0.23. Đây là BFW controlled proxy, không latency/false-accept rate cửa phòng. Hiện chưa có bằng chứng buộc đổi encoder; giữ mốc này để integration, không tự train/thử thêm model.
