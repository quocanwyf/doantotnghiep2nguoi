# T-015 — Chạy thử S4 theo protocol T-014

**Trạng thái:** đang chạy; mốc khóa nhãn trước score P1/P2. **Người thực hiện:** Quốc An. **Protocol bất biến:** [T-014](T-014-method-protocol.md). **Vai trò:** đo B0/P1/P2 trên proxy XQLFW; không đại diện lượt check-in thật hoặc quyết định cho vào phòng.

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

**Chưa có kết quả P1/P2 tại mốc này.** Bất kỳ outcome nào dưới đây chỉ được ghi sau khi run thực tế với manifest nhãn trên. Nếu checksum thay đổi, dừng và điều tra; không cập nhật manifest theo score model.

## 3. Development và khóa P2

Chưa chạy. Sẽ ghi số scene/cặp hợp lệ và mọi outcome B0/P1; tìm toàn bộ midpoint grid của top-score `τ` và top-two gap `δ` theo [T-014](T-014-method-protocol.md), tối đa 16.900 cấu hình. Chỉ cấu hình có 0 wrong-target present và 0 false selection absent trên development được xét; chọn max correct-target present, hòa ưu tiên `τ` lớn hơn rồi `δ` lớn hơn. Khóa tham số, phiên bản mã và hash nhãn trước evaluation.

## 4. Evaluation và kết luận

Chưa mở. Sau mốc khóa P2, chạy B0/P1/P2 đúng một lần với cùng detector, encoder, ảnh, CPU runner và nhãn. Báo present/absent riêng, count thô, Wilson 95%, failure case, median/p95 thời gian decode+detect, embedding và quyết định S4. Nếu không nối S8 verification 1:1 trong run này, không báo false accept/false reject của S8.

Kết luận T-015 chỉ dựa trên evidence evaluation; T-016 mới phân tích trade-off kỹ hơn. Không có kết luận hiệu quả cửa phòng hoặc chọn model cuối từ proxy XQLFW.
