# Logic quyết định — 04: điểm cải thiện và phương pháp

## T-012 → T-013: vì sao chọn câu hỏi S4

[D-001](../00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md) chọn kiểm tra đầu vào tại cửa phòng; [T-008](../01-problem/T-008-requirements.md) yêu cầu nối hồ sơ đã khai với đúng người hiện diện rồi mới xác minh 1:1. [B0 T-012](../03-baseline/T-012-B0-pipeline-choice.md) trả `unresolved` khi ảnh có 0 hoặc nhiều detection. [Chẩn đoán](../03-baseline/T-012-B0-freeze-and-stage-diagnosis.md) ghi 1.785/6.000 cặp XQLFW chưa chấm, trong đó 1.399 có ảnh nhiều detection; đó là dấu hiệu coverage trên dữ liệu web, không là tỷ lệ cửa phòng.

**Question trước solution:** có thể dùng dữ liệu sẵn có để chấm `reference A + scene nhiều mặt → mặt của A hoặc NONE` với nhãn độc lập không? [Pilot T-013](T-013-target-selection.md) kiểm một mẫu cố định: 20/24 scene được đánh giá sơ bộ là nhiều người với target đủ rõ, 3 mơ hồ, 1 detection thừa; 16 ca rõ có reference một detection, cùng 20 ca nhiều người có absent-reference một detection. [Audit giữ/loại của 24 cảnh](T-013-target-selection.md) ghi 20 giữ tạm, 3 chưa thể gán chắc và 1 loại khỏi tập nhiều người; 24 ca absent vẫn chờ xác nhận độc lập. Nguồn đủ **hứa hẹn** để đề xuất S4 làm mục tiêu nghiên cứu cho T-014, với điều kiện nhóm review kết luận T-013, kiểm nhãn độc lập và khóa split trước run kết luận. Không sử dụng box/score model làm ground truth.

## T-013 → T-014: điều phải thiết kế tiếp

T-014 mới đặt phương pháp S4, biến và protocol. B0 A0 phải chạy trên cùng scene/reference và cùng detector/encoder; so `correct-target / wrong-target / unresolved` cho target-present và target-absent, rồi nếu nối verification thì báo FA/FR/coverage cùng mẫu số. Lợi ích coverage không che lỗi chọn sai. Dữ liệu pilot đã xem chỉ dành development; evaluation tách identity và không chọn threshold bằng test. Nguồn XQLFW là proxy học thuật, không biến thành transaction thật hoặc bằng chứng giảm nhân sự. Nếu nhãn mở rộng không đủ, ghi `not runnable` cho phép so có kết luận và quay lại nhánh cải thiện B0 khác có thể đo.
