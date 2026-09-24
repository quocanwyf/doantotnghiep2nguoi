# File ngoài Git cần bàn giao riêng

`.gitignore` loại dữ liệu khuôn mặt, checkpoint, model export, log lớn, đầu ra build và bí mật khỏi Git. **Ignore không tự gỡ file đã từng được Git theo dõi**; kiểm tra file chuẩn bị commit trước khi push. Không đăng dữ liệu định danh hoặc link chia sẻ riêng tư vào repository công khai.

Khi một task cần file ngoài Git, thêm một mục theo mẫu. Gửi bằng kênh riêng mà hai người thống nhất, đối chiếu SHA-256 sau khi nhận. Không ghi khóa truy cập hay thông tin cá nhân trong file này.

```md
## A-001 — Tên file/nhóm file

- Task liên quan:
- Mục đích và cách dùng:
- Tên, phiên bản, dung lượng:
- SHA-256:
- Người giữ và người cần nhận:
- Trạng thái: Chưa gửi | Đã gửi | Đã nhận và kiểm tra
- Vị trí lưu: mô tả chung; gửi đường dẫn riêng qua kênh an toàn
- Ngày cập nhật:
```

Hiện chưa có file cần bàn giao ngoài Git.
