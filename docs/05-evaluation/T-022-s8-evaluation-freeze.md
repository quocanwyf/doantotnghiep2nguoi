# T-022 — Freeze trước một lượt evaluation S8

**Ngày/người duyệt rule:** 2026-09-29, Quốc An. **Trạng thái tại lúc tạo bản ghi này:** metadata, ground truth, split, source/model và code đã khóa; **chưa tính score evaluation**. Đây là XQLFW synthetic/controlled proxy, không phải tỷ lệ lỗi tại cửa phòng thi. [Báo cáo development và rule đã duyệt](T-022-s8-development-analysis.md).

## Rule và mẫu số cố định

- **Primary:** `θ_research=0,15`, S8 `ACCEPT ⇔ cosine ≥ θ`. Rule được chọn hoàn toàn từ development: trong grid đã công bố, `θ ≥ θ_old`; bảo toàn 29/29 genuine đã được S4 chọn đúng ở trạng thái accept; giảm số hard negative S4 chuyển đến được accept; phá hòa theo ordinary FMR, genuine FNMR rồi θ thấp hơn. Development chọn 0,15, **không chọn bằng evaluation**.
- **Historical baseline:** `θ_old=0,122254` từ T-020. **Stress point:** `θ=0,25` được công bố từ development; không phải threshold mới/optimal/deployment. Cả ba mốc được báo trên **cùng một lượt evaluation**, không chọn lại sau khi xem số.
- S4/P2 giữ `τ=0,14789717107158995`, `δ=0,07647264965285691` từ T-017. Cùng SCRFD-500MF + MobileFaceNet (buffalo_sc), CPUExecutionProvider, detector input 640×640, `det_thresh=0,5`, encoder input 112×112. Box chọn sai và S8 accept được báo tách biệt; S4 unresolved không ép qua S8.
- Evaluation đã khóa: **30 target-present + 30 target-absent scene**, **355 genuine + 131 ordinary-impostor pair**. Trong 128 scene evaluation candidate: 60 usable, 14 `AMBIGUOUS`, 54 detector-excluded. Trong 613 pair candidate: 486 usable, 113 detector-excluded, 14 excluded do trùng scene pair. Tất cả status và ground truth nằm trong manifest hash dưới đây; không loại mẫu theo output model.
- Identity nguồn development/evaluation giao nhau: **0**, được kiểm khi freeze. Không dùng T-017/T-020 failure để tune ngược rule.

## Hash/version đóng băng trước score

| Thành phần | SHA-256 / version |
|---|---|
| Locked benchmark manifest `locked-benchmark-v2.json` | `d752c99fae5071c2aedb7fe0e40842b8b25c05decf539b61df8e988fee8ec131` |
| **Evaluation ground truth + toàn bộ status/exclusion** (canonical fingerprint) | **`1a1adbc67fb327888b5b40f95b31f79c312e7a5730d5e115ecc05ccdbd2f0a19`** |
| Evaluation scene ID + file SHA list | `b270031caa0332ca2dc9a1fe4698eb46797f0ea88ad981d628e0d6febf060944` |
| XQLFW ZIP 1.0 | `1af459679fba23a12f4d83c82a81523eb930a4aec759eebefcbdde69a678962c` |
| XQLFW official pairs | `636852f90b886f3f56c73b13c9775f7ffcd37662dbb189c694f6a0a605b63b84` |
| T-014 identity split | `23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2` |
| T-015 scene manifest | `ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74` |
| T-017 scene manifest | `5ca44481ce26abe62e2e699bdaae44c7b9227f2a5c54f6ac9d865330ad658290` |
| buffalo_sc model pack | `57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72` |
| SCRFD `det_500m.onnx` | `5e4447f50245bbd7966bd6c0fa52938c61474a04ec7def48753668a9d8b4ea3a` |
| MobileFaceNet `w600k_mbf.onnx` | `9cc6e4a75f0e2bf0b1aed94578f144d15175f357bdc05e815e5c4a02b319eb4f` |
| Development summary dùng chọn rule | `c279922825717fab6959d5f0ff3437f4087e917e0123ba623251136227b91485` |
| Private freeze JSON `freeze-v1.json` | **`37071ad8bd244ddad1cf1d45fc279d642903b18f073553cb04d51eb1e45ad705`** |
| Evaluation protocol/code version | `T-022-S8-evaluation-v1`; commit chuẩn bị code `120fbff` |
| `scripts/t011_xqlfw_baseline.py` | `17c9d013ae3fe74a0e67a378fa3011b30563833b35bbc5cba39ee8b07066e4e0` |
| `scripts/t017_s4_run.py` | `7f9fc57e33a6b8f9e2c37f56737082ebf3a3549ff352c7a8ba46a59eee4550a2` |
| `scripts/t022_s8_development.py` | `ebf169ede8316c30464e10fa10487ab6da0c9824726144510a9a08881fbe2445` |
| `scripts/t022_s8_evaluation.py` | `41fa7d2cfda4d80672ba4a69155b39647c0e091659e14de318ee57170944e73d` |
| `scripts/t022_freeze_s8_evaluation.py` | `baddf4f64634d8ad38a9339a8c6858d9cf3491d5cf7ed37f2f3bf0e30e2ae9c2` |

Runtime tại freeze: Windows 11, Python 3.12.2, OpenCV 5.0.0, ONNX Runtime 1.20.1, InsightFace 0.7.3, NumPy 2.2.6, CPUExecutionProvider. Evaluation script kiểm lại hash code, runtime package, manifest, nguồn, model, nhãn/status và rule trước inference. Mỗi scene PNG evaluation cũng được đối chiếu SHA-256 với manifest trong bước freeze; script kiểm lại trước khi chấm scene.

Private freeze file và ảnh/raw/summary lưu ngoài Git tại `%TEMP%/T-022-s8-evaluation-v1/` và `%TEMP%/T-022-controlled-s8-v1/`; không commit ảnh mặt, identity, embedding hoặc raw score. Hai archive nguồn tải lại từ đúng release công khai đã ghi ở T-009/T-010 vì bản local cũ không còn; SHA-256 **khớp chính xác** các mốc trước. `%TEMP%` có thể bị dọn; cần lưu riêng khi bàn giao sang máy khác.

## Phép chạy đã khóa

1. Chạy preflight chỉ kiểm hash/cấu hình, không suy luận score.
2. Chạy **một lượt** `scripts/t022_s8_evaluation.py` trên split evaluation; script từ chối ghi đè output. Raw per-sample và summary ngoài Git, ghi hash sau run.
3. Primary report ở `θ=0,15`: S4 present correct/wrong/unresolved; S4 absent no-select/false-select; selected genuine S8 accept/reject; hard negative S8 accept/reject; ordinary FMR, genuine FNMR; pipeline absent `no-select / false-select→reject / false-select→accept`. Báo thêm θ lịch sử và stress point trên cùng scores như đã công bố.
4. Không đổi GT, exclusion, model, `τ,δ`, threshold hoặc chọn lại rule theo evaluation. Sau run, nếu kết quả không xác nhận trade-off phù hợp thì **đóng T-022** và mở câu hỏi mới ở task encoder/model; không tune tiếp trên chính holdout này.
