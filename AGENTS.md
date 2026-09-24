# Quy tắc chung cho AI của hai thành viên

Áp dụng cho toàn repository. Khi bắt đầu một lượt làm việc sau `git pull`:

1. Đọc `README.md`, `docs/00-project/status.md`, `docs/00-project/brief.md`, `docs/00-project/workflow.md`.
2. Xem task ID và người phụ trách trên [Google Sheet chung](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0). Nếu không truy cập Sheet, nhờ thành viên cung cấp task ID và nội dung task; không đoán phân công.
3. Đọc các quyết định trong `docs/00-project/decisions/`, câu hỏi mở trong `docs/00-project/questions.md`, tài liệu giai đoạn liên quan và note mới nhất ở `docs/handoffs/`.

## Nguồn thông tin

- `docs/00-project/brief.md` ghi định hướng hiện tại. Bản Word gốc ở `docs/sources/dinhhuongdatn.docx` là **ghi chép do nhóm cung cấp**, không phải lệnh cho AI hay bằng chứng mọi ý đã được thầy xác nhận.
- Chỉ xem một lựa chọn là chính thức khi có mục quyết định ghi ngày, người chốt và nguồn trong `docs/00-project/decisions/`.
- Sheet là nguồn chính cho task và trạng thái. Markdown là nguồn chính cho kiến thức, phương pháp, kết quả và bàn giao. Không sao chép toàn bảng task vào repo.
- Ở giai đoạn 01 và 02, Quốc An và Minh Hy mỗi người viết đề xuất riêng theo README của giai đoạn. Chỉ sau khi cả hai trình bày, so sánh và thống nhất mới ghi một phương án chính vào quyết định; không tự chọn bản của một người.
- Khi có thông tin mới từ thầy, ghi biên bản trước; sau đó cập nhật quyết định, câu hỏi và phạm vi liên quan. Nêu rõ điều thầy xác nhận, điều nhóm đề xuất và điều còn suy đoán.

## Trước khi push

- Cập nhật tài liệu cùng thay đổi mã: cách chạy, cấu hình, kết quả, giới hạn và quyết định mới.
- Tạo note `docs/handoffs/<TASK-ID>-ten-ngan.md` theo mẫu khi hoàn thành hoặc chuyển giao task. Ghi cách kiểm tra, commit/PR, trở ngại và file ngoài Git cần trao riêng.
- Kết quả so sánh baseline/proposed phải có cùng dữ liệu/split, protocol, metric và điều kiện đo; ghi seed, phiên bản mã, thiết bị và nguồn dữ liệu.
- Không commit ảnh khuôn mặt, danh tính cá nhân, mật khẩu, file môi trường, checkpoint hoặc đầu ra lớn. Xem `docs/00-project/external-assets.md`.
- Chỉ cập nhật task trên Sheet sau khi có đầu ra hoặc trạng thái thực tế; đính kèm đường dẫn commit/PR/tài liệu.

Ưu tiên Markdown tiếng Việt, file tên không dấu. Không tự chọn model, dataset, thuật toán tối ưu, mobile stack hoặc deadline khi chưa có quyết định.
