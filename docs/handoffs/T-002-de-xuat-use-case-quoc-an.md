# Bàn giao T-002 — đề xuất use case của Quốc An

- Người làm, ngày: Quốc An, với AI hỗ trợ soạn bản đề xuất; 2026-09-24.
- Link task trên Sheet: https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0 (dòng T-002).
- Commit/PR: https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1 (draft); bản đầu 2e2e108e633f795b14f0f01bb7156f5f02b4272e.
- Tóm tắt thay đổi và file chính: docs/01-problem/quoc-an-proposal.md khảo sát sáu use case; mỗi use case nối vấn đề nghiệp vụ, camera, 1:1/1:N, đầu ra, ràng buộc, pipeline và hướng đo sơ bộ. Có tiêu chí lọc và cầu nối sang giai đoạn 02.
- Cách chạy/kiểm tra; kết quả thực tế: không có mã chạy. Đọc đề xuất và đối chiếu với yêu cầu T-002 trên Sheet, docs/01-problem/README.md và docs/00-project/brief.md. Đã kiểm tra nguồn NIST về 1:1/1:N và điều kiện sử dụng được nêu từ trang gốc của nguồn. Chưa thực nghiệm hoặc kiểm chứng quyền dùng bộ dữ liệu cụ thể.
- Quyết định hoặc giả định liên quan: đây là đề xuất riêng của Quốc An; chưa chọn use case, dữ liệu, model, metric hay thuật toán cho nhóm. B, C và D chỉ được ưu tiên kiểm tra tiếp theo giả thuyết, không phải kết luận T-004.
- Điều chưa xong, trở ngại, người cần tiếp tục: Quốc An xem/sửa đề xuất; Minh Hy hoàn thành T-003 độc lập; cả hai so sánh ở T-004. Công cụ đọc/ghi thư mục cục bộ gặp lỗi khởi tạo, nên file được tạo trên nhánh GitHub, chưa kiểm tra checkout cục bộ.
- File ngoài Git: không có.
