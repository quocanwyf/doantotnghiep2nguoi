# T-024 — 04. S4/S8 và điểm nối AI với app

## 1. Pipeline và vai trò

Hồ sơ đã resolve cung cấp **reference của A**. Observation có một/nhiều mặt → detector bbox + landmarks → alignment/embedding cho từng mặt → S4 chọn candidate theo reference A hoặc unresolved → S8 candidate/reference A → AI verdict. Business pre/final-check, retry, role và ghi check-in nằm ngoài model.

S4 là **target selection**, không phải classifier xác định toàn bộ danh sách sinh viên. Encoder tạo vector 512 chiều; cosine là tín hiệu so sánh, không phải xác suất đúng identity. App runtime chưa biết mặt chọn đúng/sai; các nhãn CORRECT_TARGET/FALSE_SELECTION trong report chỉ có vì benchmark có ground truth.

## 2. Những gì nghiên cứu đã thử

| Phương án | Rule | Vai trò hiện tại |
| --- | --- | --- |
| B0/A0 | Một face thì đưa candidate sang verification; nhiều face unresolved. | Baseline gốc, nhánh đơn giản để đối chiếu. |
| P1 | Chọn top-1 duy nhất trong cảnh nhiều mặt, không guard score/margin. | Đối chứng nghiên cứu; không tự dùng làm fallback khi P2 unresolved. |
| P2 | Top-1 duy nhất + score đạt τ + khoảng cách top1/top2 đạt δ. | Selective S4 đã có code/evidence, giữ làm cấu hình nghiên cứu tham chiếu. |

P2 parameters từ [T-017 code](../../../scripts/t017_s4_run.py):

```text
tau   = 0.14789717107158995
delta = 0.07647264965285691
select iff unique top-1 AND top_score >= tau AND top_score - second_score >= delta
```

**Giới hạn code quan trọng:** `select_p1/select_p2` hiện trả `None` khi có ít hơn hai score. Code này dùng cho benchmark multi-face; không phải dispatcher của toàn app. `None` không cho phép ép chọn một face hoặc gọi S8 với candidate cũ.

**Đề xuất integration cần Hy ghi thành adapter/config:** zero-face → unresolved/no-face; exactly-one → nhánh một mặt B0 đưa candidate sang S8; ≥2 → P2 giữ nguyên τ/δ; tie → unresolved. Đây là nối hai nhánh đã nghiên cứu, **chưa phải dispatcher app đã implement/test/freeze**. Bảng T-024 một mặt “khi S4 chọn candidate theo rule” không có nghĩa hàm P2 hiện tự support một mặt. Ghi branch/version và kiểm khi integration, không sửa các runner/evaluation cũ để giả rằng đã có dispatcher này.

## 3. S8 hiện có và giới hạn

S8 nghiên cứu đọc **chính selected cosine** đã tính giữa selected-face embedding và reference embedding. Không dùng crop/reference mới hoặc encoder thứ hai để recompute một tín hiệu độc lập.

```text
S4 selected → S8 ACCEPT iff selected_score >= theta
           → NOT_VERIFIED otherwise
S4 unresolved → S8 NOT_RUN (không ép chọn)
```

`theta=0.23` là research/reference operating point T-023, không phải ngưỡng demo/deployment đã freeze. T-024 không retune. Khi dùng cho development integration, ghi rõ research config; trước test cuối khóa operating point/AIConfig được duyệt, không chọn lại từ kết quả test. Mốc lịch sử 0.122254/0.15 và stress 0.25 không tự thay thế config này.

Ở T-023, S8 reject 30/38 hard negative nhưng còn accept 8/38, selected genuine accept 55/55. Điều này giúp giữ encoder để tích hợp, chưa chứng minh auto-check-in đạt acceptable risk. Hai stage cùng signal nên không gọi S8 là hàng rào nhận dạng độc lập. [Report có mẫu số/giới hạn](../../05-evaluation/T-023-encoder-evaluation-result.md).

## 4. Đề xuất contract tối thiểu — chưa có endpoint/SDK

| Chiều | Thông tin cần giữ | Vì sao |
| --- | --- | --- |
| App → AI | attempt ID, observation ID/capture index, resolved record ID, reference asset/version, observation, AIConfig version | Giữ đúng claim/reference và đúng frame trong lượt. |
| AI → App | detection count/boxes, selected detection hoặc null, S4 status/reason, selected score/margin nếu có, S8 verdict hoặc NOT_RUN/UNAVAILABLE, runtime, AIConfig/reference/observation versions | Route retry/manual và audit đúng stage; không suy PASS từ score. |
| App → Decision/write | Business checks/versions, authority/auto flag, duplicate/effective record, AI result liên kết observation, counters và human evidence nếu có | Final check, confirmed write và nguồn quyết định. |

Tên field cụ thể/API/format ảnh do Hy chọn; dữ liệu private như ảnh/embedding không đưa lên Git hoặc log công khai. Reference chỉ được lấy từ record đã resolve, không tìm reference nào có score cao nhất để fit scene. Đổi model/preprocessing/reference version phải invalidation cache; không dùng vector tạo bởi model khác.

**Ví dụ DTO minh họa, toàn bộ ID/score giả, không phải output thí nghiệm:**

```json
{
  "attempt_id": "demo-attempt-001",
  "observation_id": "demo-observation-001",
  "record_id": "demo-record-001",
  "reference_version": "demo-ref-v1",
  "ai_config_version": "research-reference-v1",
  "detection_count": 2,
  "s4": {"status": "SELECTED", "selected_detection": 1, "score": 0.31, "margin": 0.12},
  "s8": {"status": "ACCEPT", "score": 0.31, "score_source": "REUSED_SELECTED_COSINE"}
}
```

Đây mới là AI result; app vẫn phải final-check/authority/write. Với unresolved: selected_detection/score là null, S8 NOT_RUN. Lỗi reference/decode/runtime có reason riêng, không giả thành score 0 hoặc ACCEPT; mapping chưa rõ route business/manual/hold.

## 5. Preprocessing phải giữ đúng điểm nối

[`get_faces`](../../../scripts/t017_s4_run.py) decode bằng OpenCV BGR, gọi detector lấy bbox/landmarks, tạo InsightFace `Face`, gọi recognition `.get(image, face)` để thư viện alignment/preprocessing rồi L2-normalize embedding. [`unit`](../../../scripts/t011_xqlfw_r50_comparison.py) kiểm 512 chiều, finite, norm khác 0. Cosine = dot product của hai vector normalized.

Hy cần giữ màu, orientation, landmarks/alignment và normalization tương thích khi đổi runtime. Không tự crop bbox/resize hoặc double-convert RGB/BGR rồi coi là cùng pipeline. BFW letterbox/two-panel là preprocessing **dựng benchmark**, không yêu cầu app chia camera thành hai panel. Nếu port ONNX ra runtime khác, ghi input/output transform và kiểm parity trước test cuối; không tự đổi τ/δ/θ để che sai khác integration.
