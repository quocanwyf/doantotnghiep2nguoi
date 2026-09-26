# Bàn giao T-007 — chọn hướng khảo sát T-005

- **Người làm, ngày:** Quốc An ghi nhận với AI hỗ trợ; 2026-09-25. Minh Hy cùng Quốc An đã chốt lựa chọn theo xác nhận của Quốc An; văn bản có thể được rà soát trong PR.
- **Task trên Sheet:** [T-007](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0).
- **Commit/PR:** [PR #1](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1); commit của lần cập nhật ghi trong lịch sử PR.
- **Đầu ra:** [selection](../02-survey/T-007-selection.md), [D-002](../00-project/decisions/T-007-D-002-chon-huong-khao-sat-t005.md), logic phase 02 và trạng thái dự án.
- **Cách kiểm tra/kết quả:** so T-005 với [T-006 của Minh Hy](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2) theo bài toán đã chọn ở D-001. T-005 khớp luồng mã → xác minh 1:1 → rule phòng/ca/giờ; T-006 xây trên điểm danh lớp 1:N. Nhóm theo hướng T-005 để chuẩn bị experiment, không chọn final dataset/model/optimization.
- **Giả định/giới hạn:** survey T-005 đã đủ phân tích task/data/model/experiment để review; chưa xác minh đầy đủ file/quyền/weight, chưa khóa protocol hay chạy baseline. Nguồn T-007 là xác nhận của Quốc An về quyết định chung; chưa có biên bản buổi chốt riêng trong repo.
- **Bước tiếp:** Rà soát D-002/selection; kiểm tra khả dụng và quyền của candidate, chốt protocol/split/metric/thiết bị, chạy baseline rồi phân tích lỗi trước khi chọn hướng tối ưu.
- **File ngoài Git:** không có.
