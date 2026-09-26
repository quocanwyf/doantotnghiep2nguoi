# T-008 — Bàn giao bản review BA, task còn đang làm

- **Ngày / người làm:** 2026-09-26, Quốc An với AI hỗ trợ; Minh Hy là người review theo Sheet.
- **Trạng thái:** bàn giao phần cập nhật tài liệu để nhóm review; chưa hoàn tất/freeze T-008.
- **Nguồn:** bản phân tích 20 mục đã thảo luận và phản hồi BA của Quốc An trong chat: giữ nền tảng, bổ sung Core Decisions, As-Is và gates, không viết lại từ đầu để chọn công nghệ.
- **PR:** [PR #3 — draft](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/3); commit của lần cập nhật trong lịch sử PR.
- **Đầu ra:** [T-008-requirements.md](../01-problem/T-008-requirements.md); logic phase 01/02; hướng dẫn đọc, status/questions và nguyên tắc thẩm quyền trong workflow.
- **Thay đổi:** đưa bản phân tích trong chat vào file T-008; giữ 24 SC, 17 BR, 19 FR, 10 NFR, 12 risk và 23 OQ; thêm lớp đọc nhanh, kế hoạch thu bằng chứng As-Is, phân loại FR theo độ sẵn sàng, G9/GI/GO và điều kiện freeze. Mục 19 nối ID BR-01–BR-08 của bản repo cũ sang ID mới để không mất traceability.
- **Kiểm tra:** đủ 20 mục và dải ID; tham chiếu ID có định nghĩa; bảng đủ cột; code fence Mermaid cân bằng; liên kết file Markdown tương đối tồn tại; đọc lại authority, absent/check-in, fallback và gate. Chưa chạy pilot hoặc xác minh quy chế; chưa render Mermaid bằng renderer.
- **Còn thiếu:** As-Is thực địa; định nghĩa attendance, bằng chứng xác minh, hồ sơ/roster và ranh giới quyền được nhóm duyệt; người/cách fallback thực tế.
- **Bước tiếp:** Quốc An tổng hợp câu trả lời G9 theo mục 18, Minh Hy review. T-009 có thể audit nguồn/khả dụng song song, nhưng không chốt mức phù hợp phụ thuộc gate còn mở. Freeze nghiên cứu theo mục 20; chưa tuyên bố được triển khai thật hoặc giảm nhân sự.
- **File ngoài Git:** không có dữ liệu/tài liệu đầu vào mới cần trao riêng.
