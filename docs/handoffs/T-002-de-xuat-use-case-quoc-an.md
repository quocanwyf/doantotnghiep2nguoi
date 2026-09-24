# Bàn giao T-002 — đề xuất use case của Quốc An

- Người làm, ngày: Quốc An, với AI hỗ trợ cập nhật; 2026-09-24.
- Link task trên Sheet: https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0 (dòng T-002).
- Commit/PR: https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1 (draft); cập nhật nghiệp vụ b531e8503765bf0af4b92e364ffd025a86890677.
- Tóm tắt thay đổi và file chính: docs/01-problem/quoc-an-proposal.md chọn bối cảnh kiểm tra thí sinh tại cửa phòng thi; mục tiêu sản phẩm là máy xử lý lượt thường lệ để giảm nhu cầu một người chuyên kiểm tra tại cửa mỗi phòng, ghi nhận người đã đến/vắng và chuyển ngoại lệ cho người có thẩm quyền. Luồng khai báo mã trước rồi xác minh mặt 1:1, kiểm tra phòng/ca/giờ/trùng lượt. docs/02-survey/quoc-an-survey.md là khảo sát T-005 đi kèm.
- Cách kiểm tra; kết quả thực tế: đọc lại luồng và đối chiếu với khảo sát T-005 và quy chế THPT được công bố. Chưa có mã, dữ liệu hay pilot để chứng minh mức giảm nhân sự. Quy chế THPT vẫn có bước giám thị đối chiếu trực tiếp; mục tiêu giảm người đứng cửa phải diễn giải theo loại kỳ thi và phạm vi được phép.
- Quyết định hoặc giả định liên quan: Quốc An thông báo nhóm đã chọn bối cảnh T-002 ở T-004. Sheet và docs/00-project/decisions/ chưa có bản ghi ngày/người chốt/nguồn cho T-004 tại thời điểm cập nhật; cần đồng bộ để đây là quyết định chính thức của repo. Chưa chốt dataset, model, ngưỡng hay thuật toán tối ưu.
- Điều chưa xong, trở ngại, người cần tiếp tục: nhóm cần biên bản T-004 và cổng đặc tả nghiệp vụ chi tiết cho kỳ thi pilot, nhất là mức tự động hóa, giấy tờ, đi muộn, sai phòng, nghi giả mạo, người quyết định và mất mạng. Công cụ thư mục cục bộ gặp lỗi khởi tạo nên thay đổi được ghi trên nhánh GitHub, chưa kiểm tra checkout cục bộ.
- File ngoài Git: không có.
