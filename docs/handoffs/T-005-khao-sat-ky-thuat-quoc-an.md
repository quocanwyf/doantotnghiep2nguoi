# Bàn giao T-005 — khảo sát kỹ thuật cá nhân của Quốc An

- Người làm, ngày: Quốc An, với AI hỗ trợ soạn bản khảo sát; 2026-09-24.
- Link task trên Sheet: https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0 (dòng T-005; cần cập nhật lại phụ thuộc nếu nhóm xác nhận cách làm song song).
- Commit/PR: https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1 (draft).
- Tóm tắt thay đổi và các file chính: docs/02-survey/quoc-an-survey.md là bản khảo sát kỹ thuật cá nhân dựa trên docs/01-problem/quoc-an-proposal.md. Có yêu cầu dữ liệu/quyền dùng, 2 baseline dự kiến, pipeline, các hướng H1–H6, objective, metric, split, chi phí và rủi ro. Đây là ứng viên để so sánh với T-003/T-006 của Minh Hy, chưa phải lựa chọn chung.
- Cách chạy/kiểm tra; kết quả thực tế: đọc tài liệu và đối chiếu với T-002, README giai đoạn 02 và nguồn được liên kết. Chưa có mã, dữ liệu thu thập, thí nghiệm hay số liệu thực nghiệm; không có kiểm thử chương trình. Quyền dùng LFW/Replay-Attack và quyền dùng dữ liệu mô phỏng cần kiểm chứng trước khi tải/thu.
- Quyết định hoặc giả định liên quan: giả định luồng thí sinh khai báo mã rồi xác minh 1:1, một người trong vùng làm thủ tục mỗi lượt. H1/H2 chỉ được ưu tiên kiểm tra đầu tiên, chưa chốt tối ưu chính, model hay ngưỡng. T-004 và T-007 chưa thực hiện.
- Điều chưa xong, trở ngại, người cần tiếp tục: Quốc An kiểm tra khả năng có dữ liệu, quyền dùng và thiết bị; Minh Hy chuẩn bị T-003/T-006 độc lập; nhóm so sánh toàn bộ hai gói trước khi quyết định. Sheet/README hiện ghi T-005 phụ thuộc T-004, không đúng với cách làm song song vừa được Quốc An nêu; cần hai thành viên thống nhất chỉnh kế hoạch. Công cụ thư mục cục bộ lỗi nên tệp được tạo trên nhánh GitHub, chưa kiểm tra checkout cục bộ.
- File ngoài Git: không có.
