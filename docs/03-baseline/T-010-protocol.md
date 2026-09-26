# T-010 — Khóa giao thức baseline trước khi chạy

**Ngày thiết kế:** 2026-09-26. **Người thực hiện:** Quốc An. **Trạng thái:** dự thảo để Minh Hy review; chưa chạy baseline, chưa xem kết quả so sánh và chưa chọn model cuối.

## 1. Mục tiêu và ranh giới

T-010 chuyển capability/rủi ro nghiệp vụ từ T-008 và các candidate đủ điều kiện từ T-009 thành một **protocol có thể chạy lại** cho T-011. Mục tiêu là khóa câu hỏi, dữ liệu, split, preprocessing, biến kiểm soát, metric, thiết bị và cách ghi nhận kết quả **trước khi xem benchmark**.

T-010 không chứng minh model nào tốt hơn, không tối ưu threshold trên test set, không tự đặt acceptance target chưa được nhóm chốt và không thay đổi yêu cầu nghiệp vụ để làm một candidate kỹ thuật trở nên phù hợp.

Đầu vào hiện tại:
- T-008 ở PR #3 vẫn đang được Minh Hy review; capability/TQ từ đó là baseline tạm thời và phải đối chiếu lại trước khi khóa protocol.
- T-009 ở PR #5 đã audit B0 một số dataset/weight; smoke runtime chỉ chứng minh khả dụng file/runtime, không phải accuracy.

## 2. Câu hỏi thí nghiệm

### E1 — Detection component
**Câu hỏi:** trên cùng dữ liệu ảnh nguyên khung và cùng thiết bị đo, YuNet, BlazeFace full-range và SCRFD-500MF khác nhau thế nào về detection quality và chi phí chạy?

- **Biến thay đổi:** detector candidate.
- **Giữ cố định:** dataset/split, annotation chuẩn, quy tắc resize/input, thiết bị, warm-up, số lần lặp, cách đo latency và quy tắc match prediction–ground truth.
- **Metric:** metric chuẩn của dataset khi phù hợp (ví dụ precision/recall/AP), error slices nếu nhãn cho phép, latency và resource.
- **Giới hạn:** kết quả E1 không tự chứng minh end-to-end verification hoặc target selection S4.

### E2 — 1:1 face verification
**Câu hỏi:** với cùng protocol reference/probe và split hợp lệ, các encoder đủ điều kiện phân tách genuine/impostor thế nào?

Pool ban đầu:
- MobileFaceNet từ `buffalo_sc`: đã qua file/runtime gate ở T-009.
- EdgeFace XS, AdaFace R18, R50: chỉ được đưa vào run nếu hoàn tất weight/runtime/preprocessing gate trước khi freeze.

- **Biến thay đổi:** encoder/weight candidate.
- **Giữ cố định:** reference/probe protocol, split, thiết bị và procedure đo.
- **Preprocessing:** mỗi candidate dùng alignment/color/normalization đúng implementation/weight đã pin; không ép một crop tùy tiện cho mọi model.
- **Metric:** ROC, FMR/FNMR theo threshold, TAR tại các FMR được protocol cho phép báo cáo, EER khi phù hợp.
- **Quy tắc threshold:** chọn/tune trên dev; test chỉ dùng để đánh giá sau khi config và operating point đã khóa.

### E3 — Uncertain / retry / manual-review behavior
**Câu hỏi:** khi input hoặc model output không đủ chắc chắn, workflow có dẫn đến outcome đúng theo policy T-008 không?

Đây là test logic/policy bằng fixture, không phải benchmark model. Case tối thiểu:
- không thấy mặt;
- nhiều mặt nhưng chưa xác định được target;
- verification score nằm vùng uncertain;
- record/ca/phòng không khớp;
- retry vượt giới hạn;
- chuyển manual review;
- authority xác nhận/từ chối theo T-008.

Kết quả E3 là expected state/outcome pass/fail, không phải face-recognition accuracy.

## 3. Data gate trước khi khóa dataset

Không dataset nào được gọi là `main test`, `dev` hay `external` cho đến khi:
1. file ảnh/annotation thực tải và parse được;
2. quyền/điều kiện sử dụng của ảnh, annotation và protocol được ghi rõ;
3. schema nhãn đáp ứng đúng câu hỏi thí nghiệm;
4. manifest có identity/session/frame information đủ để kiểm leakage;
5. protocol pairs/path thực sự trỏ tới file tồn tại;
6. artifact có version/checksum;
7. domain gap và capability không đo được được ghi rõ.

Candidate từ T-009:
- detection: ưu tiên kiểm WIDER FACE; FDDB là external/dự phòng nếu cần và phải có quy tắc ellipse riêng;
- verification: XQLFW có file pairs đã kiểm, nhưng archive ảnh/path/rights chưa đủ để khóa làm main test;
- external portal/video: ChokePoint chỉ dùng nếu archive/rights/label mapping được xác minh;
- LFW chỉ smoke/reference, không dùng làm bằng chứng triển khai cửa phòng thi.

Nếu không candidate nào vượt data gate, protocol phải ghi **blocked by data evidence**, không chọn dataset chỉ vì dễ tải.

## 4. Split và chống leakage

### Detection
- ưu tiên split chính thức;
- không để frame gần nhau cùng sequence rơi vào cả dev và test nếu gây leakage;
- subset tự tạo phải có manifest bất biến và quy tắc lấy mẫu.

### Verification
- dev/test tách theo identity khi cấu trúc dataset cho phép;
- nếu protocol chuẩn cố định không identity-disjoint, phải ghi đúng giới hạn;
- threshold/config chỉ chọn trên dev;
- test chạy sau freeze;
- external set không dùng tuning.

### Workflow fixture
- fixture nghiệp vụ tách khỏi dữ liệu mặt;
- mỗi case có input state, policy config, expected transition/outcome và trace về T-008.

## 5. Preprocessing và điều kiện so sánh

Fair comparison không có nghĩa mọi model phải dùng cùng preprocessing. Mỗi run phải pin:
- model/weight source;
- checksum;
- input size;
- color order;
- normalization;
- detector score/NMS threshold nếu có;
- landmark/alignment rule;
- similarity/distance function và chiều score;
- runtime/library version.

Sau khi freeze, không sửa preprocessing dựa trên test result; nếu cần thay đổi phải mở revision/experiment mới.

## 6. Metric và acceptance criteria

| Experiment | Metric chính | Metric phụ | Acceptance target |
|---|---|---|---|
| E1 detector | metric chuẩn dataset / recall/AP phù hợp | latency, resource, error slices | TBD từ rủi ro và thiết bị |
| E2 verification | FMR/FNMR, ROC/TAR@FMR | EER, latency/resource | TBD từ rủi ro T-008 |
| E3 workflow | expected outcome pass/fail | retry/manual count | Theo policy T-008 sau review |

**Nguyên tắc:** metric được định nghĩa trước; acceptance target nghiệp vụ chưa được nhóm chốt phải để `TBD`, không tự đặt số sau khi xem kết quả.

## 7. Thiết bị và cách đo

Nếu target hardware chưa chốt, tách:
- **reference environment** để tái lập baseline;
- **target environment** chỉ thêm khi nhóm xác nhận thiết bị triển khai.

Với latency/resource:
- ghi CPU/GPU, RAM, OS, runtime version;
- warm-up trước đo;
- cùng procedure và cùng scope thời gian giữa candidate;
- báo median và percentile phù hợp;
- model-only và end-to-end latency phải được phân biệt nếu đo cả hai.

## 8. Reproducibility manifest cho T-011

Mỗi run phải ghi:
- `experiment_id`;
- commit SHA;
- dataset version/checksum;
- manifest/split version;
- weight checksum;
- preprocessing config;
- seed nếu có randomness;
- package/runtime versions;
- hardware;
- raw predictions/results;
- metric summary;
- deviation log.

Không âm thầm thay dataset, weight, threshold hoặc preprocessing giữa các run.

## 9. Freeze gate trước T-011

T-010 chỉ được coi là **locked** khi:
1. T-008 đã review đủ để không còn thay đổi capability trực tiếp ảnh hưởng experiment, hoặc điểm mở đã được ghi rõ;
2. dataset cho từng run vượt data gate;
3. weight/preprocessing được pin;
4. split/manifest đóng băng;
5. metric và procedure đo được chốt;
6. acceptance target chưa có quyết định được để TBD;
7. Minh Hy review protocol **trước khi nhóm xem baseline**.

Mọi thay đổi sau freeze phải có revision/experiment mới và lý do.

## 10. Bàn giao cho T-011

T-011 nhận:
- danh sách run được phép chạy;
- manifest/split đã khóa;
- config per candidate;
- metric/procedure;
- environment/measurement procedure;
- expected artifacts/naming;
- danh sách TBD/limitation không được suy diễn.

T-011 chỉ tạo **evidence thực nghiệm**; chưa chọn final model/pipeline.

## 11. Điểm đang mở

- T-008 PR #3 chưa review xong.
- Dataset chính chưa vượt đầy đủ file/label/rights gate theo T-009.
- Target hardware chưa xác nhận.
- Acceptance target nghiệp vụ cho FMR/FNMR/latency chưa chốt.
- EdgeFace/AdaFace/R50 chưa qua runtime gate tương đương MobileFaceNet.

Chuỗi trace: **T-008 capability/risk → T-009 candidate audit → T-010 protocol freeze → T-011 baseline evidence → T-012 technical decision**.
