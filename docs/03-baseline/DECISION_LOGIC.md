# Decision Logic — Phase 03 Baseline

## Chuỗi suy luận

1. T-008 xác định capability, policy và rủi ro cần kiểm chứng.
2. T-009 audit candidate và loại/hoãn những candidate chưa đủ bằng chứng khả dụng.
3. [T-010](T-010-protocol.md) biến uncertainty còn lại thành E1 detection, E2 1:1 verification, E3 workflow fixture và M1 đo vận hành; mỗi nhánh dẫn ID TQ/FR/RISK của T-008 dự thảo, stage T-005 và giới hạn T-009.
4. Protocol phải được review/freeze trước khi T-011 xem benchmark để tránh chọn metric, threshold, split hoặc preprocessing theo kết quả.
5. T-011 chỉ tạo evidence và ghi deviation.
6. T-012 phân tích lỗi baseline và chọn uncertainty/câu hỏi experiment tiếp theo; final technical decision chỉ sau experiment và review có đủ evidence.

## Quy tắc

- Không gọi candidate nào là tốt nhất ở T-010.
- Không dùng dataset chưa qua file/label/rights/schema gate.
- Không tune threshold trên test.
- Không dùng external/test set để sửa config rồi báo lại cùng tập đó.
- Acceptance target chưa có quyết định nghiệp vụ phải để TBD.
- Nếu T-008 đổi capability, protocol liên quan phải mở lại.
- Nếu T-011 lệch protocol, deviation phải được ghi và có thể cần chạy lại như experiment mới.

## Quyết định hiện tại và điều kiện bước sau

T-010 mới ở mức **design draft**, chưa là protocol locked. Kiểm archive XQLFW cho thấy 6.000 pair đều có ảnh nhưng 10 fold chính thức trùng identity giữa các fold; nguồn công bố cho tải, quyền ảnh dẫn xuất chưa được xác nhận đầy đủ. Vì vậy XQLFW chưa tự động thành main test hoặc bằng chứng unseen identity. Dataset detection, quyền ảnh, policy profile, mục tiêu chấp nhận và thiết bị đích còn mở.

Có thể review cách đo và chuẩn bị fixture/code mà không xem locked test. T-011 chỉ chạy so sánh được gọi là locked khi dữ liệu, split, weight/preprocessing, metric, điều kiện đo và review của Minh Hy đã được ghi; nếu target nghiệp vụ vẫn TBD, chỉ báo số liệu mô tả và không kết luận pass/fail hoặc model cuối.
