# Bàn giao T-002 — đề xuất use case của Quốc An

- Người làm, ngày: Quốc An, với AI hỗ trợ cập nhật; 2026-09-24.
- Link task trên Sheet: https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0 (dòng T-002).
- Commit/PR: https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1 (draft); cập nhật phạm vi dataset công khai tại 0c73cf36893bad7c839f0424d79607899586b15e.
- Tóm tắt thay đổi và file chính: docs/01-problem/quoc-an-proposal.md chọn bối cảnh kiểm tra thí sinh tại cửa phòng thi; mục tiêu sản phẩm là máy xử lý lượt thường lệ để giảm nhu cầu người chuyên kiểm tra tại từng phòng, ghi nhận người đã đến/vắng và chuyển ngoại lệ. Luồng khai báo mã trước rồi xác minh mặt 1:1, kiểm tra phòng/ca/giờ/trùng lượt. T-005 khảo sát kỹ thuật tại docs/02-survey/README.md (bốn tài liệu phân rã, dataset, model và thí nghiệm).
- Cách kiểm tra; kết quả thực tế: đối chiếu với T-005 và quy chế THPT được công bố. Chưa có mã, benchmark hoặc pilot để chứng minh mức giảm nhân sự. Đồ án dự kiến dùng dataset công khai cho nhận diện và hồ sơ giả lập cho nghiệp vụ, không xin dữ liệu thí sinh kỳ thi thật. Quy chế THPT vẫn có bước giám thị đối chiếu trực tiếp.
- Quyết định hoặc giả định liên quan: Quốc An thông báo nhóm đã chọn bối cảnh T-002 ở T-004. Sheet và docs/00-project/decisions/ chưa có bản ghi ngày/người chốt/nguồn; cần đồng bộ để đây là quyết định chính thức của repo. Chưa chốt dataset, model, ngưỡng hay thuật toán tối ưu.
- Điều chưa xong, trở ngại, người cần tiếp tục: đồng bộ quyết định T-004; đặc tả nghiệp vụ kịch bản thi, nhất là mức tự động hóa, giấy tờ, đi muộn, sai phòng, nghi giả mạo, người quyết định và mất mạng. Ghi rõ phần nào được đo bằng dataset công khai, phần nào chỉ mô phỏng logic. Công cụ thư mục cục bộ gặp lỗi khởi tạo nên thay đổi được ghi trên nhánh GitHub, chưa kiểm tra checkout cục bộ.
- File ngoài Git: không có.
