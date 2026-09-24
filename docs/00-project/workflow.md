# Quy trình phối hợp qua Sheet và GitHub

Nhóm gồm **Quốc An (TV-A)** và **Minh Hy (TV-B)**. Hướng dẫn để Minh Hy bắt đầu trên máy riêng ở [onboarding.md](onboarding.md).

## Hai nguồn dùng cho hai mục đích

- [Google Sheet task](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0): mã việc, người làm chính, người review, trạng thái, hạn, trở ngại và link đầu ra.
- [GitHub repo](https://github.com/quocanwyf/doantotnghiep2nguoi): mã, kiến thức dự án, quyết định, kết quả và note bàn giao. Không tạo task board thứ hai trong repo.

## Một vòng làm việc

1. **Nhận việc:** đồng bộ `main` mới nhất (`git pull --ff-only`), xem task ID trên Sheet, đọc `AGENTS.md`, `status.md`, quyết định, note bàn giao và tài liệu giai đoạn liên quan. Mỗi task có một người phụ trách chính và một người review.
2. **Làm:** tạo nhánh ngắn gắn task ID, ví dụ `task/T-001-problem-scope`. Ghi cấu hình, nguồn và kết quả ngay trong tài liệu liên quan. Nếu phát sinh lựa chọn quan trọng, lập đề xuất quyết định để hai người xem; không tự coi nó là đã chốt.
3. **Bàn giao:** cập nhật tài liệu cùng mã; tạo `docs/handoffs/T-001-ten-ngan.md` theo mẫu. Ghi việc đã làm, cách chạy/kiểm tra, commit hoặc PR, điều còn vướng và file ngoài Git cần trao riêng. Nếu có file ngoài Git, thêm vào `external-assets.md`.
4. **Review và hợp nhất:** push nhánh, gửi PR cho người còn lại review. Sau khi gộp vào `main`, cập nhật dòng task trên Sheet bằng trạng thái và link PR/commit/tài liệu. Người kia pull `main` rồi đọc note bàn giao trước khi làm tiếp.
5. **Cuối tuần:** cả hai cập nhật chung một file `docs/progress/YYYY-Www.md`; sửa `status.md` nếu mốc hoặc rủi ro chung thay đổi.

Nếu chưa dùng PR, ít nhất hai người cần đồng bộ `main` trước khi sửa và review thay đổi quan trọng trước khi push. Tránh hai người cùng sửa một file chung trong thời gian dài.

## Điều kiện bàn giao xong

- Kết quả có đường dẫn và cách kiểm tra/tái lập.
- Tài liệu không mâu thuẫn với quyết định hoặc trạng thái hiện tại.
- Task trên Sheet dẫn tới đúng kết quả.
- Mọi file bị `.gitignore` chặn nhưng cần cho người kia đã có mục bàn giao và tình trạng gửi/nhận.
