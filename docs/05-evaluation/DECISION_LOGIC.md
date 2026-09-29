# Logic quyết định — 05: đánh giá S4 và điều kiện chốt kỹ thuật

## T-015 → T-016: vì sao cần phân tích lỗi paired

[T-008](../01-problem/T-008-requirements.md) cần chọn đúng người tương ứng hồ sơ đã khai trước xác minh 1:1. [B0 T-012](../03-baseline/T-012-B0-pipeline-choice.md) từ chối chọn khi nhiều detection; [T-014](../04-optimization/T-014-method-protocol.md) đặt P1 ép chọn và P2 có nhánh chưa kết luận để kiểm trade-off. [T-015](../04-optimization/T-015-proposed-run.md) đã tạo cùng một tập/runner và khóa P2 trước evaluation; P2 có 35 present đúng, 6 unresolved và 2 absent false-selection trên 41/35 trial proxy. Bảng tổng không cho biết **vì sao** đổi được coverage và lỗi nào còn lại, nên T-016 đọc raw đã khóa theo sample, score/gap và ảnh audit.

## T-016 → T-017 xác nhận sạch

[T-016](T-016-comparison-ablation.md) thấy P1 luôn false-select khi target vắng do quy tắc ép chọn; P2 giảm 33/35 lỗi này nhưng hai absent có score và margin đều qua ngưỡng. Sáu present unresolved chia thành rớt score, rớt gap hoặc cả hai. Mọi present được chấm có box mục tiêu; chất lượng ảnh chỉ là dấu hiệu trực quan, chưa là nguyên nhân định lượng. Sai khác gán điểm tâm từ box và thiếu identity người nền làm yếu nhãn, nên kết quả hiện tại hỗ trợ **giữ selective S4 để nghiên cứu**, chưa chốt P2/ngưỡng triển khai.

**Việc tiếp theo được suy ra và đã chạy ở T-017:** dùng holdout chưa xem, khóa protocol/điểm thị giác/nhãn trước score và giữ P2 frozen. [T-017](T-017-clean-confirmation.md) có 49 present, 41 absent usable. P2 đúng 46 present, unresolved 3; vẫn false-select 2 absent. Sai khác điểm tâm T-015 được khắc phục ở thứ tự gán nhãn, còn self-confirm và identity người nền là giới hạn.

## T-017 → quyết định nghiên cứu → bằng chứng triển khai còn thiếu

**Context:** B0 không xử lý cảnh nhiều mặt; P1 ép chọn cả khi target vắng; P2 giảm lỗi đó nhưng hai false-selection absent lặp trên holdout sạch. **Decision:** giữ selective S4 làm ứng viên, chưa chốt P2/ngưỡng cho app thật. **Why:** phép thử xác nhận giá trị coverage nhưng không loại hết rủi ro absent, chưa có S8 end-to-end hoặc dữ liệu/thiết bị miền đích. **Affects next:** app có thể dùng B0/fallback và giữ `unresolved` để người phụ trách xử lý; nếu đưa P2 vào demo nghiên cứu thì selection không tự cấp quyền. Task kỹ thuật sau phải xuất phát từ lỗi absent S4, kiểm S4→S8 và điều kiện thiết bị/policy, với protocol và holdout mới trước khi tối ưu. Không sửa T-015/T-017 sau khi xem kết quả.
