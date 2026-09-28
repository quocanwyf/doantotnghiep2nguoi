# Logic quyết định — 04: điểm cải thiện và phương pháp

## T-012 → T-013: vì sao chọn câu hỏi S4

[D-001](../00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md) chọn kiểm tra đầu vào tại cửa phòng; [T-008](../01-problem/T-008-requirements.md) yêu cầu nối hồ sơ đã khai với đúng người hiện diện rồi mới xác minh 1:1. [B0 T-012](../03-baseline/T-012-B0-pipeline-choice.md) trả `unresolved` khi ảnh có 0 hoặc nhiều detection. [Chẩn đoán](../03-baseline/T-012-B0-freeze-and-stage-diagnosis.md) ghi 1.785/6.000 cặp XQLFW chưa chấm, trong đó 1.399 có ảnh nhiều detection; đó là dấu hiệu coverage trên dữ liệu web, không là tỷ lệ cửa phòng.

**Question trước solution:** dữ liệu có sẵn có đủ để tự xác nhận có kiểm soát `reference A + scene nhiều mặt → mặt của A hoặc NONE` mà không lấy model làm ground truth duy nhất không? [Pilot T-013](T-013-target-selection.md) chọn cố định 24 scene: audit ảnh gốc thấy 20 nhiều người có target rõ, 3 mơ hồ, 1 detection thừa. [Quy trình self-confirm](T-013-self-confirm-protocol.md) khóa trước khi xem điểm embedding: kiểm metadata XQLFW, ảnh gốc, rồi mới dùng rank MobileFaceNet làm tín hiệu phụ. Kết quả **16/24 present** và **13/24 absent** nhất quán ở mức proxy; phần còn lại `AMBIGUOUS` hoặc không thuộc tập nhiều người. Nguồn đủ để đi tiếp T-014 thiết kế S4; không có người gán nhãn độc lập, nên pilot chỉ là development và có nguy cơ thiên lệch về B0. Không chọn model/threshold S4 từ kết quả này.

## T-013 → T-014: điều phải thiết kế tiếp

T-014 mới đặt phương pháp S4, biến và protocol. B0 A0 phải chạy trên cùng scene/reference và cùng detector/encoder; so `correct-target / wrong-target / unresolved` cho target-present và target-absent, rồi nếu nối verification thì báo FA/FR/coverage cùng mẫu số. Lợi ích coverage không che lỗi chọn sai. Dữ liệu pilot đã xem chỉ dành development; evaluation tách identity và không chọn threshold bằng test. Nguồn XQLFW là proxy học thuật, không biến thành transaction thật hoặc bằng chứng giảm nhân sự. Nếu nhãn mở rộng không đủ, ghi `not runnable` cho phép so có kết luận và quay lại nhánh cải thiện B0 khác có thể đo.

## T-014 → T-015: vì sao cần phép thử trên tập khóa

T-013 cho thấy câu hỏi S4 có thể tạo nhãn proxy self-confirm nhưng pilot 24 identity đã xem không được làm test; cross-check MBF cũng sẽ thiên vị selector MBF nếu tái dùng để gán nhãn evaluation. [T-014](T-014-method-protocol.md) vì vậy loại 24 pilot identity, chia 2.603/1.116 identity development/evaluation, dùng R50 **chỉ để audit nhãn** trước khi mở score MBF của candidate. Đây vẫn không là nhãn độc lập và người nền chưa có identity đầy đủ.

B0 A0 từ chối mọi cảnh nhiều detection; ép chọn top-1 có nguy cơ chọn sai nhất là target vắng. T-014 giữ nguyên detector/MBF/S8 và thử đúng một thay đổi ở S4: chọn top cosine khi qua ngưỡng tuyệt đối và khoảng cách với top-2, nếu không thì unresolved. Hai biến được tìm vét cạn trên development theo quy tắc đã khóa; evaluation giữ kín cho T-015. [FaceNet](https://www.cv-foundation.org/openaccess/content_cvpr_2015/html/Schroff_FaceNet_A_Unified_2015_CVPR_paper.html) là cơ sở family embedding, [SelectiveNet](https://proceedings.mlr.press/v97/geifman19a.html) gợi khung risk–coverage; các nguồn đó không bảo đảm kết quả S4 trên XQLFW.

**Uncertainty chuyển sang T-015:** trong cùng 64 scene/split và ca present/absent, P2 tăng được bao nhiêu correct target so với B0, có bao nhiêu wrong target/false selection, đổi lấy bao nhiêu unresolved và thời gian? Nếu nhãn tự xác nhận sau loại mơ hồ không đủ mẫu, T-015 phải báo exploratory/not runnable; không lấy score evaluation để đổi split, threshold hoặc tiêu chí loại. T-016 mới phân tích trade-off, T-017 mới cân nhắc quyết định kỹ thuật cuối.

## T-015 → T-016: kết quả nào tạo ra câu hỏi tiếp

[T-015](T-015-proposed-run.md) đã khóa scene/nhãn trước score MobileFaceNet, tìm đúng hai biến `τ,δ` trên development và chạy evaluation một lượt. Với 41 present và 35 absent tự xác nhận trên cùng proxy XQLFW, B0 unresolved cả 41 present và không chọn cả 35 absent; P1 chọn đúng 40 present nhưng chọn một mặt ở cả 35 absent; P2 chọn đúng 35 present, unresolved 6 present và false-select 2 absent. S4 có thể tăng coverage so với B0, nhưng false-selection target-absent và độ rộng khoảng tin cậy không cho phép chốt cấu hình cuối.

**Question chuyển sang T-016:** hai lỗi false-selection và sáu ca unresolved của P2 xảy ra trong hoàn cảnh nào, và lợi ích coverage có đủ thuyết phục trước chi phí embedding/rủi ro chọn sai không? T-016 phải giữ nguyên nhãn, split và tham số evaluation của T-015; phân tích lỗi sau test không được biến thành tuning trên test. Sai khác tự gán điểm tâm từ box thay vì ghi điểm độc lập, thiếu reviewer độc lập, reference XQLFW và identity người nền chưa đầy đủ là giới hạn bằng chứng, không phải lý do sửa nhãn để cải thiện số đo.
