# Câu hỏi chưa chốt

Giữ câu hỏi ở đây đến khi có bằng chứng trả lời và quyết định liên quan. Không xem câu trả lời phỏng đoán là ý thầy. Bài toán nhóm đã chọn ở [D-001](decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md); hướng khảo sát ở [D-002](decisions/T-007-D-002-chon-huong-khao-sat-t005.md).

1. Kỳ thi mục tiêu là kỳ thi nào? Quy chế cụ thể cho phép thiết bị hỗ trợ bước nào, bước nào giám thị vẫn phải làm? Ngày/nguồn buổi Quốc An và Minh Hy thống nhất T-004/T-007 có cần bổ sung vào biên bản không?
2. Optimization chạy lúc training hay inference có phù hợp kỳ vọng của thầy? Thuật toán tìm kiếm ngoài optimizer huấn luyện như Adam/SGD có là yêu cầu không?
3. Thành phần nào là bottleneck theo baseline và error analysis, search space/objective function phù hợp là gì?
4. Operating point, acceptance criteria, metric chính, split và giao thức đánh giá cần chốt theo hậu quả false accept/false reject thế nào?
5. Dataset/weight công khai nào có quyền và tệp dùng được cho đồ án? Domain gap cửa phòng thi được đánh giá hoặc giới hạn kết luận ra sao? Dữ liệu người thật chỉ được xét khi có quyền phù hợp.
6. Mobile chạy Android/iOS, on-device/server, offline/online; thiết bị đo và tiêu chí demo tối thiểu là gì?
7. Mốc nộp, lịch gặp và hình thức báo cáo được yêu cầu là gì?
8. Ai có quyền xử lý ngoại lệ, sửa lượt ghi nhận; quy tắc muộn, nhầm phòng, trùng lượt và “chưa đến” của kỳ thi mục tiêu là gì?

Khi giải quyết câu hỏi, dẫn đến biên bản/nguồn và tạo file quyết định nếu đó là lựa chọn chính thức.

## Câu hỏi còn mở của generic baseline T-008

OQ-001–OQ-023 được quản lý tại [T-008, mục 18](../01-problem/T-008-requirements.md#18-open-questions--deferred-policies). Nhóm cần review semantics của workflow/authority/roster để freeze cấu trúc; giá trị policy theo kỳ thi, điều kiện triển khai và câu hỏi nghiên cứu có thể tiếp tục mở theo đúng phạm vi. T-009 audit candidate với giả định/gap được ghi rõ; T-010 khóa profile và protocol trước phép thử. Chưa có xác minh As-Is thực địa và chưa thể tuyên bố giảm nhân sự.
