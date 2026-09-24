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

## A-001 — Bản ghi định hướng gốc

- Task liên quan: khởi động dự án
- Mục đích: đối chiếu với `brief.md` khi có chi tiết chưa rõ
- Tên, phiên bản, dung lượng: `dinhhuongdatn.docx`, bản nhận ngày 2026-09-24, 51.495 byte
- SHA-256: `B819734B280E8E5A68B238DF9C2023D21271896EE9F66967A39780E6EFBA4E63`
- Người giữ và người cần nhận: hai thành viên tự điền
- Trạng thái: Chưa xác nhận người còn lại đã nhận
- Vị trí lưu: gửi riêng; không đặt link riêng tư trong GitHub
- Ngày cập nhật: 2026-09-24
