# T-024 — 01. Context và phạm vi app

## 1. Bài toán cần hiện thực hóa

Thiết bị tại cửa phòng thi hỗ trợ một người **khai mã hồ sơ/SBD → kiểm điều kiện nghiệp vụ → xác minh người tương ứng hồ sơ → ghi check-in hoặc chuyển xử lý**. Camera có thể thấy nhiều mặt; nhiều mặt không tự đồng nghĩa có nhiều người cùng khai mã, và không bắt buộc retry nếu S4 đã chọn được candidate.

Mục tiêu là giảm thao tác đối chiếu ở lượt bình thường và có đường xử lý ngoại lệ. Chưa có kỳ thi cụ thể hoặc số đo thực địa để kết luận giảm bao nhiêu nhân sự. [T-008](../../01-problem/T-008-requirements.md) là business baseline generic; [T-024](../../01-problem/T-024-demo-decision-policy.md) là profile demo đã duyệt.

## 2. Hai bề mặt sử dụng

1. **Thiết bị hướng về thí sinh ở cửa:** nhập mã, hiển thị hồ sơ đã resolve theo quyền, hướng dẫn camera/retry, báo outcome và nơi cần liên hệ.
2. **Phần dành cho người phụ trách:** xem lượt/case pending, confirm hoặc xử lý manual trong quyền, xem check-in, tình trạng hệ thống và audit cần thiết.

Đây là hai trách nhiệm giao diện, chưa chốt hai app hay hai thiết bị vật lý. Hy chọn việc chúng nằm trong cùng app có chế độ riêng, màn hình quản lý khác hoặc kiến trúc phù hợp. Màn hình quản lý phải kiểm quyền; thông tin cá nhân không cần hiện cho người đang xếp hàng.

## 3. Phần Hy và phần An

| Phần | Trách nhiệm theo hướng nhóm đã chốt |
| --- | --- |
| Hy — app/integration | UI/UX, nguồn roster demo và mapping reference, context phòng/ca, business checks, attempt/state, role/manual, retry, ghi/đọc check-in, audit, lỗi và phục hồi. Chọn stack/cách triển khai và ghi lý do. |
| An — AI | Bàn giao detector/encoder, S4/S8 rule/config, evidence và giới hạn; hỗ trợ adapter và kiểm sự tương thích. Không tự mở thêm nghiên cứu model/fine-tuning lúc này. |
| Điểm nối chung | Quy ước input/output, version của reference/AIConfig/ExamPolicy, xử lý lỗi, single-face branch, nơi chạy AI và cấu hình dùng khi test cuối. |

Hy có thể phát triển chi tiết nghiệp vụ app từ baseline, dùng mock/replay để dựng UI trước. Những thay đổi phòng/giờ/role nhỏ không mặc định làm lại nghiên cứu AI. Nếu đổi từ khai hồ sơ + verification 1:1 sang tìm identity toàn roster, đổi đối tượng xác minh hoặc semantics PASS, đó là thay đổi capability cần rà cùng An.

## 4. Thứ tự làm thực tế

1. Dựng dữ liệu demo và màn hình khai SBD → resolve hồ sơ → business pre-check.
2. Làm outcome/state và màn hình người phụ trách bằng output AI mock ghi rõ nguồn.
3. Nối nguồn observation, adapter detector/embedding → S4 → S8.
4. Nối retry budget, final-check, auto-check-in/manual và confirmed write.
5. Lưu audit tối thiểu, chạy end-to-end và sửa lỗi integration.
6. Khi app chạy ổn, dùng checklist test-profile để freeze input/config/case/expected result rồi kiểm chính thức và report.

Các lượt thử trong phát triển app là kiểm integration, không gọi là frozen evaluation mới của T-017/T-022/T-023 và không dùng holdout cũ để retune.

## 5. Các khái niệm không được gộp

- **Attempt:** một lượt xử lý claim đã resolve; có thể có nhiều capture/recovery.
- **Capture/observation:** một đầu vào ảnh trong attempt; mọi lần thu để kiểm đều tính global capture budget.
- **Check-in:** bản ghi nghiệp vụ hiệu lực sau quyết định có quyền và ghi thành công.
- **Entry authorization:** quyền vào theo nghiệp vụ; không suy từ detector hoặc mặc định PASS đã mở cửa.
- **Attendance:** kết quả tham dự theo định nghĩa riêng, không suy absent chỉ vì chưa check-in.
- **Override:** quyết định người có quyền cho case hiện tại. **Correction:** sửa bản ghi đã có với lịch sử trước/sau.

Scope hiện tại không tự thêm chống giả mạo/liveness, tracking theo video, OCR hoặc cơ chế mở khóa cửa. Nếu bổ sung, cần ghi câu hỏi/requirement mới; không coi chúng là capability đang có.
