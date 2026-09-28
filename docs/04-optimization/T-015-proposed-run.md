# T-015 — Chạy thử S4 theo protocol T-014

**Trạng thái:** đã chạy T-015, chờ phân tích trade-off T-016; không chọn cấu hình triển khai. **Người thực hiện:** Quốc An. **Protocol bất biến:** [T-014](T-014-method-protocol.md). **Vai trò:** đo B0/P1/P2 trên proxy XQLFW; không đại diện lượt check-in thật hoặc quyết định cho vào phòng.

## 1. Câu hỏi và thứ tự thực hiện

T-012 cho thấy B0 để `UNRESOLVED` khi SCRFD trả nhiều detection. T-013 xác nhận có thể gán nhãn proxy có kiểm soát. T-014 đã khóa A0/B0, P1 và P2. T-015 kiểm xem P1/P2 tăng số lần chọn đúng người mục tiêu trên cảnh nhiều mặt như thế nào, với giá phải trả ở chọn nhầm khi target-present và chọn người khi target-absent.

Thứ tự bắt buộc: **chọn scene/ref → rà nguồn/ảnh → R50 audit-only → khóa manifest nhãn → B0/P1 trên development → tìm đúng `τ,δ` trên development → khóa tham số và mã → một lượt evaluation**. Không dùng score MBF hoặc outcome P1/P2 để sửa nhãn, thay scene hay đổi split.

## 2. Mốc khóa nhãn trước score candidate

Ngày 2026-09-28, script [chọn scene](../../scripts/t015_scene_manifest.py) kiểm SHA-256 nguồn và split T-014, chỉ chạy SCRFD-500MF 640×640 với detection threshold 0,5. Duyệt thứ tự T-014, chọn 64 scene đầu mỗi split có ≥2 detection, genuine reference và tối đa một scene cho mỗi identity nguồn. Development cần quét 597 ảnh, evaluation 452 ảnh; mỗi split chọn 64. Cả hai reference được chọn theo seed T-014 trước khi xem ảnh hoặc score.

128 scene và reference được rà trên 32 contact sheet riêng ngoài Git. Nhãn do **một lượt self-review của Codex**, không có người gán nhãn độc lập. Gương mặt mục tiêu được nhận diện trực quan từ scene và present reference; điểm tâm dùng để nối với đúng một box SCRFD. Cần ghi rõ hạn chế: trong bản tự rà này, tọa độ tâm được lấy theo tâm box đã nhận diện trực quan, nên bước nhập tọa độ **không độc lập với box detector**. Điểm P1/P2 chưa được xem ở giai đoạn này. Cảnh không chắc giữ `AMBIGUOUS`.

Script [audit nhãn](../../scripts/t015_label_audit.py) so metadata XQLFW, genuine pair và bytes JPG; chạy lại SCRFD kiểm box; dùng R50 từ T-011 **chỉ làm cross-check**, không làm candidate S4. Điều kiện present: reference đúng một mặt, target được nối duy nhất và R50 xếp target cao nhất. Điều kiện absent: absent reference đúng một mặt, nhìn ảnh không thấy target và max R50 thấp hơn positive anchor cùng scene. Bất đồng giữ `AMBIGUOUS`.

| Split | Scene đã chọn | Nhìn rõ target | Visual ambiguous | Extra detection không phải người thật | Present self-confirm | Absent self-confirm |
|---|---:|---:|---:|---:|---:|---:|
| Development | 64 | 54 | 9 | 1 | 43 | 37 |
| Evaluation | 64 | 55 | 9 | 0 | 41 | 35 |

**Mẫu số audit:** mỗi split có 64 scene được chọn trước khi biết score S4. Development có 54 scene nhiều người nhìn rõ, 9 scene visual `AMBIGUOUS` và 1 scene `EXCLUDED` khỏi proxy nhiều người vì detection thừa; evaluation có 55 scene rõ, 9 scene visual `AMBIGUOUS`, 0 scene loại do detection thừa. Sau các kiểm reference/R50, cặp *scene + present reference* dùng được/`AMBIGUOUS` là **43/21** ở development và **41/23** ở evaluation; cặp *scene + absent reference* là **37/27** và **35/29**. Số `AMBIGUOUS` theo cặp đã bao gồm scene bị loại do detection thừa ở development; không cộng các nhóm nguyên nhân như các tập rời nhau. Tất cả 128 scene và lý do từng reference vẫn còn trong manifest nhãn riêng, kể cả khi không vào mẫu chấm.

Một số ảnh tham chiếu có nhiều detection nên không được ép vào mẫu chấm (development: present 11, absent 9; evaluation: present 13, absent 8). Bất đồng R50 present: development 1, evaluation 2. Mẫu số evaluation vượt mốc tối thiểu 30 present và 30 absent của T-014; việc đủ mẫu **không** xóa thiên lệch self-confirm, ảnh web XQLFW hoặc thiếu nhãn người nền.

Manifest private gồm tên ảnh, ảnh gốc, nhãn và score R50 lưu tại `C:\Users\Admin\AppData\Local\Temp\T-015-scenes-v1\`; không đưa ảnh, identity, embedding hoặc raw sample output lên Git. Các hash kiểm cố định trước khi mở MobileFaceNet:

- Split T-014: `23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2`.
- Scene/reference manifest: `ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74`.
- Locked label audit manifest: `747f9f0877b92c9f87fbceec944e4de5132c393cfa766f44fd6c9ea9ce333785`.

Ở **commit mốc nhãn `d1e8cb7`**, chưa có kết quả P1/P2. Bất kỳ outcome nào dưới đây được tạo **sau** mốc đó với manifest nhãn trên. Nếu checksum thay đổi, dừng và điều tra; không cập nhật manifest theo score model.

## 3. Development và khóa P2

[Script run](../../scripts/t015_s4_run.py) chạy trên **43 present và 37 absent self-confirm** của development. Mỗi scene/ref giữ nguyên SCRFD-500MF, landmark/crop 112, MobileFaceNet trong `buffalo_sc`, L2/cosine; chỉ S4 khác nhau. Cả 43 scene present đều có ≥2 detection (35 scene có 2, 7 có 3, 1 có 4); không có single-face trong tập chọn theo protocol.

| Nhánh | Present correct / wrong / unresolved (N=43) | Absent no-select / false-select (N=37) |
|---|---:|---:|
| B0/A0 | 0 / 0 / 43 | 37 / 0 |
| P1 top-1 | 43 / 0 / 0 | 0 / 37 |
| P2 chọn trên development | 40 / 0 / 3 | 37 / 0 |

Grid có **81 mốc `τ` × 81 mốc `δ` = 6.561 cấu hình**, kiểm hết; 4.815 cấu hình đạt ràng buộc 0 wrong-target present và 0 false-selection absent của development. Theo tie-break đã định trước, khóa **`τ = 0,14789717107158995`**, **`δ = 0,07647264965285691`**. Đây là tham số nghiên cứu, không là ngưỡng cho vào phòng thi hoặc bảo đảm 0 lỗi ngoài development.

Raw development từng scene/ref có scores, outcome và thời gian ở Temp ngoài Git; SHA-256 `ff1f98c177ddd70f79ca24365ba16a5b7045234a68c98bd090016452dc269fbd`. SHA-256 mã run **trước evaluation** `70f6bbd2f1c6dafa2b433779905df6539149a1c3c415a117aa76f84c2100fd3a`. File cấu hình khóa riêng lưu cùng thư mục Temp; SHA-256 `a63f64d7fa6cfe4d3d98f2d52c10a30d7bb8445b20de8b0e6b4780ff1ff7980d`. Các giá trị hash/tham số ở đây được commit **trước khi chạy evaluation**; mọi thay đổi code/nhãn sau đó phải dừng, không chạy lại tìm tham số theo evaluation.

## 4. Evaluation một lượt sau khi khóa P2

Đã chạy **một lượt** trên cùng script/weight/CPU runner và manifest đã khóa ở commit `c7785f6`, không tìm lại `τ,δ` hay thay sample theo outcome. Raw evaluation gồm từng scene/ref, toàn bộ score từng detection, ground truth box, outcome B0/P1/P2 và thời gian; SHA-256 `bfb452355ba038ea935b54e4daf1df76c01d28d1b437839dc3f4daaa579d1209`. File chỉ ở Temp ngoài Git. Hash mã, nhãn, scene và frozen config trong raw **khớp mốc trước evaluation**.

| Nhánh | Target-present: đúng / sai / unresolved (N=41) | Target-absent: không chọn / chọn sai (N=35) |
|---|---:|---:|
| B0/A0 | 0 / 0 / 41 | 35 / 0 |
| P1 top-1 | 40 / 1 / 0 | 0 / 35 |
| P2 selective | **35 / 0 / 6** | **33 / 2** |

Với P2, tỷ lệ correct target present là **35/41 = 85,4%** (Wilson 95%: 71,6–93,1%). Wrong target present **0/41** chỉ cho giới hạn trên Wilson khoảng **8,6%**, không chứng minh tỷ lệ thật bằng 0. False selection target-absent **2/35 = 5,7%** (Wilson 95%: 1,6–18,6%). Đây là **chọn một mặt khi người cần tìm không có trong cảnh**, chưa phải false acceptance của bước xác minh 1:1 hoặc quyết định vào phòng.

Tập đã chọn theo protocol gồm cảnh nhiều detection; **không có single-face trong mẫu chấm T-015**. Trong 41 present usable: 34 cảnh có 2 detection, 5 có 3, 2 có 4; trong 35 absent usable: 29/4/2 cảnh tương ứng. Cách này kiểm S4 ở nhánh B0 đang unresolved; không ước lượng hiệu quả trên phân bố tất cả lượt camera.

### Ca lỗi chính, giữ nguyên nhãn đã khóa

- P1 chọn sai target present ở `evaluation-014`; P2 abstain do gap top-2 `0,0401 < δ`.
- P2 unresolved 6 present: `evaluation-009` không qua cả score và gap; `evaluation-018`, `evaluation-047` không qua score; `evaluation-014`, `evaluation-030`, `evaluation-032` không qua gap. Các ca này cần review/fallback ở pipeline.
- P2 chọn một mặt ở 2 ca target-absent `evaluation-025` và `evaluation-053`; top-score/gap đều qua hai điều kiện đã khóa. Không sửa nhãn hoặc tham số sau khi thấy hai ca này.

### Chi phí trên cùng CPU runner

Windows 11, Python 3.12.2, OpenCV 5.0.0, ONNX Runtime 1.20.1, InsightFace 0.7.3, NumPy 2.2.6, 12 logical CPU; `CPUExecutionProvider`, model đã warm trong process, ONNX cache trên ổ cục bộ. Median/p95 của **76 trial usable**: scene decode+detect **44,13/51,97 ms**; reference decode+detect **41,85/53,80 ms**; embedding **mỗi mặt scene** **22,75/34,43 ms** trên 169 lần, reference một mặt **26,81/38,05 ms**. Quyết định P1 **0,0058/0,0101 ms**, P2 **0,0012/0,0026 ms** sau khi đã có scores. Hai reference dùng chung scene; thời gian scene được ghi vào hai dòng trial để truy vết, không diễn giải như 76 scene độc lập. B0 có thể dừng sau detection ở nhánh nhiều mặt, còn P1/P2 cần thêm embedding; đây không phải số đo throughput của thiết bị cửa phòng.

## 5. Diễn giải và giới hạn quyết định

P2 làm tăng coverage trên **present proxy nhiều mặt** so với B0 từ 0 lên 35/41 ca chọn đúng trong evaluation, và tránh được lỗi present mà P1 mắc ở một ca. Đổi lại, P2 vẫn **false-select 2/35 target-absent** và để 6/41 present unresolved. P1 ép chọn đạt 40/41 present nhưng chọn một mặt trong **35/35 absent**. Do đó evidence cho thấy hướng S4 selective đáng nghiên cứu tiếp, **chưa đủ để chọn P2 làm cấu hình cuối hoặc khẳng định hệ thống chấp nhận đúng người**. T-016 cần phân tích paired failure và cách xử lý false selection, rồi mới cân nhắc quyết định kỹ thuật.

Mẫu nhãn là self-confirm một người, R50 chỉ cross-check, không có reviewer độc lập. Nhãn nguồn XQLFW chỉ xác định identity chính; người nền không được gán danh tính đầy đủ, vì vậy không thể chứng minh mọi identity nền không overlap development/evaluation. 128 target/source identity đã chọn thì **64/64, giao 0**, và không trùng 24 pilot identity. Ảnh web XQLFW, present/absent nhân tạo 1:1, reference đôi khi nhiều mặt và cách ghi tâm từ box sau kiểm trực quan có thể gây thiên lệch. Ở evaluation, 23/64 present và 29/64 absent không vào mẫu chấm sau self-confirm; không được diễn giải kết quả trên 41/35 như toàn bộ 64 scene hoặc lượt check-in. Không chạy S8 verification 1:1 trong T-015, nên **không có số false accept/false reject của S8**. Không có policy kỳ thi hay thiết bị đích để đặt tiêu chí đạt nghiệp vụ và suy ra tiết kiệm nhân lực.
