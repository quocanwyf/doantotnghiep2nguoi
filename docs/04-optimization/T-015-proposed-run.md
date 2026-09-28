# T-015 — Chạy thử S4 theo protocol T-014

**Trạng thái:** đang chạy; nhãn và tham số development đã khóa, evaluation chưa mở. **Người thực hiện:** Quốc An. **Protocol bất biến:** [T-014](T-014-method-protocol.md). **Vai trò:** đo B0/P1/P2 trên proxy XQLFW; không đại diện lượt check-in thật hoặc quyết định cho vào phòng.

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

## 4. Evaluation và kết luận

Chưa mở. Sau mốc khóa P2, chạy B0/P1/P2 đúng một lần với cùng detector, encoder, ảnh, CPU runner và nhãn. Báo present/absent riêng, count thô, Wilson 95%, failure case, median/p95 thời gian decode+detect, embedding và quyết định S4. Nếu không nối S8 verification 1:1 trong run này, không báo false accept/false reject của S8.

Kết luận T-015 chỉ dựa trên evidence evaluation; T-016 mới phân tích trade-off kỹ hơn. Không có kết luận hiệu quả cửa phòng hoặc chọn model cuối từ proxy XQLFW.
