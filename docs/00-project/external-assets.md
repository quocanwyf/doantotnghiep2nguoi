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

Các tài sản ngoài Git đang cần cho T-011 được ghi bên dưới.

## A-001 — XQLFW archive và giao thức pairs (T-011 E2)

- Task liên quan: T-009, T-010, T-011.
- Mục đích và cách dùng: ảnh/cặp xác minh 1:1 cho phép thử pair-fold học thuật; không dùng làm nhãn nghiệp vụ cửa phòng.
- Nguồn: [trang tải tác giả](https://martlgap.github.io/xqlfw/pages/download.html), [pairs release](https://github.com/Martlgap/xqlfw/releases/download/1.0/xqlfw_pairs.txt).
- Tên, phiên bản, dung lượng: xqlfw.zip 195.229.543 byte; xqlfw_pairs.txt 160.795 byte; release 1.0 của protocol.
- SHA-256: archive 1AF459679FBA23A12F4D83C82A81523EB930A4AEC759EEBEFCBDDE69A678962C; pairs 636852F90B886F3F56C73B13C9775F7FFCD37662DBB189C694F6A0A605B63B84.
- Người giữ và người cần nhận: bản cục bộ trên máy chạy T-011; Minh Hy có thể tải lại từ nguồn tác giả và đối chiếu hash.
- Trạng thái: Chưa gửi; không đưa ảnh, tên identity hoặc embedding vào Git.
- Vị trí lưu: thư mục tạm ngoài Git của máy chạy; đường dẫn máy cụ thể gửi riêng nếu cần.
- Ngày cập nhật: 2026-09-26.

## A-002 — InsightFace buffalo_sc model pack (T-011 E2)

- Task liên quan: T-009, T-011.
- Mục đích và cách dùng: SCRFD-500MF phát hiện/alignment và MobileFaceNet tạo embedding cho baseline học thuật; không là model cuối.
- Nguồn: [InsightFace model zoo](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md), [model zoo release](https://github.com/deepinsight/insightface/releases/tag/model-zoo). Model được tác giả giới hạn cho nghiên cứu phi thương mại.
- Tên, phiên bản, dung lượng: buffalo_sc.zip, 14.969.382 byte.
- SHA-256: 57D31B56B6FFA911C8A73CFC1707C73CAB76EFE7F13B675A05223BF42DE47C72.
- Người giữ và người cần nhận: bản cục bộ trên máy chạy T-011; Minh Hy có thể tải lại từ nguồn tác giả và đối chiếu hash.
- Trạng thái: Chưa gửi; không đưa checkpoint/weight vào Git.
- Vị trí lưu: thư mục tạm ngoài Git của máy chạy; đường dẫn máy cụ thể gửi riêng nếu cần.
- Ngày cập nhật: 2026-09-26.
