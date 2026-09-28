# Logic quyết định — 05: đánh giá S4 và điều kiện chốt kỹ thuật

## T-015 → T-016: vì sao cần phân tích lỗi paired

[T-008](../01-problem/T-008-requirements.md) cần chọn đúng người tương ứng hồ sơ đã khai trước xác minh 1:1. [B0 T-012](../03-baseline/T-012-B0-pipeline-choice.md) từ chối chọn khi nhiều detection; [T-014](../04-optimization/T-014-method-protocol.md) đặt P1 ép chọn và P2 có nhánh chưa kết luận để kiểm trade-off. [T-015](../04-optimization/T-015-proposed-run.md) đã tạo cùng một tập/runner và khóa P2 trước evaluation; P2 có 35 present đúng, 6 unresolved và 2 absent false-selection trên 41/35 trial proxy. Bảng tổng không cho biết **vì sao** đổi được coverage và lỗi nào còn lại, nên T-016 đọc raw đã khóa theo sample, score/gap và ảnh audit.

## T-016 → xác nhận riêng → T-017

[T-016](T-016-comparison-ablation.md) thấy P1 luôn false-select khi target vắng do quy tắc ép chọn; P2 giảm 33/35 lỗi này nhưng hai absent có score và margin đều qua ngưỡng. Sáu present unresolved chia thành rớt score, rớt gap hoặc cả hai. Mọi present được chấm có box mục tiêu; chất lượng ảnh chỉ là dấu hiệu trực quan, chưa là nguyên nhân định lượng. Sai khác gán điểm tâm từ box và thiếu identity người nền làm yếu nhãn, nên kết quả hiện tại hỗ trợ **giữ selective S4 để nghiên cứu**, chưa chốt P2/ngưỡng triển khai.

**Việc tiếp theo được suy ra:** muốn quyết định kỹ thuật cuối cần một task xác nhận sạch trên holdout chưa xem, protocol/nhãn khóa trước score mới và cùng cấu hình P2 frozen. Nếu không đủ nhãn absent tin cậy, nêu rõ giới hạn. Đây là đề xuất task riêng, không sửa T-015 hoặc tune evaluation. [T-017 trên Sheet](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0) đang là bước tổng hợp quyết định; nếu rerun chưa có, T-017 chỉ được ghi quyết định có điều kiện và bằng chứng còn thiếu.
