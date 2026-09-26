# Decision Logic — Phase 03 Baseline

## Chuỗi suy luận

1. T-008 xác định capability, policy và rủi ro cần kiểm chứng.
2. T-009 audit candidate và loại/hoãn những candidate chưa đủ bằng chứng khả dụng.
3. T-010 biến uncertainty còn lại thành câu hỏi thí nghiệm có biến thay đổi, biến giữ cố định, dữ liệu/split, preprocessing, metric và procedure tái lập.
4. Protocol phải được review/freeze trước khi T-011 xem benchmark để tránh chọn metric, threshold, split hoặc preprocessing theo kết quả.
5. T-011 chỉ tạo evidence và ghi deviation.
6. T-012 mới đối chiếu evidence với requirement để ra quyết định kỹ thuật hoặc kết luận chưa đủ căn cứ.

## Quy tắc

- Không gọi candidate nào là tốt nhất ở T-010.
- Không dùng dataset chưa qua file/label/rights/schema gate.
- Không tune threshold trên test.
- Không dùng external/test set để sửa config rồi báo lại cùng tập đó.
- Acceptance target chưa có quyết định nghiệp vụ phải để TBD.
- Nếu T-008 đổi capability, protocol liên quan phải mở lại.
- Nếu T-011 lệch protocol, deviation phải được ghi và có thể cần chạy lại như experiment mới.
