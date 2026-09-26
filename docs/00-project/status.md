# Trạng thái dự án

- Cập nhật: 2026-09-26
- Giai đoạn: phạm vi bài toán 01 đã được nhóm chọn; khảo sát 02 đã chọn hướng để chuẩn bị thí nghiệm.
- Thành viên: Quốc An (TV-A), Minh Hy (TV-B).

## Đã làm và đã chọn

- **T-004:** Quốc An xác nhận mình và Minh Hy chọn đề tài T-002: thiết bị kiểm tra thí sinh tại cửa phòng thi, có mã khai báo và xác minh mặt 1:1. [D-001](decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md) và [scope](../01-problem/T-004-scope.md) ghi lý do, phạm vi, nguồn xác nhận và giới hạn. T-003 của Minh Hy là đề xuất độc lập để so sánh, không là bài toán chính.
- **T-005 ở mức Survey:** [bộ tài liệu Quốc An](../02-survey/README.md) đã có phân rã S0–S11, yêu cầu/shortlist dataset theo stage, model family/candidate và thiết kế baseline/thí nghiệm. [T-007](../02-survey/T-007-selection.md) chọn hướng này làm cơ sở nghiên cứu vì khớp T-004; [D-002](decisions/T-007-D-002-chon-huong-khao-sat-t005.md) ghi quyết định. Khảo sát T-006 của Minh Hy vẫn được giữ làm nguồn đối chiếu.
- [PR #1](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1) chứa T-002/T-005 và hai quyết định nhóm T-004/T-007; [PR #2](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2) giữ đề xuất độc lập T-003/T-006 để đối chiếu. Hai quyết định đã được nhóm chốt theo xác nhận của Quốc An.

## Đợt việc tiếp theo đang làm

[T-008 — phân tích nghiệp vụ cửa phòng thi](../01-problem/T-008-requirements.md) đã được rà soát BA: có Core Decisions, As-Is còn thiếu bằng chứng, To-Be đề xuất, bảng scenario/rule/requirement và gates cho T-009. Tài liệu vẫn ở discovery, chưa freeze và chưa chọn kỳ thi/quy chế. T-009 được audit nguồn/khả dụng song song; các kết luận phụ thuộc định nghĩa attendance, bằng chứng xác minh, nguồn roster và authority phải chờ G9 tương ứng. T-010 chỉ khóa phép thử khi câu hỏi ảnh hưởng protocol/tiêu chí đã được xử lý. Task và phân công ở Sheet chung.

## Chưa có bằng chứng để chốt kỹ thuật cuối

T-005 **hoàn thiện phần phân tích/survey**, chưa hoàn tất việc kiểm tra tệp/quyền dùng dữ liệu và trọng số, pin preprocessing/weight, chọn main test và thiết bị, khóa split/metric/operating point, chạy baseline hoặc xác định bottleneck. Vì vậy shortlist dataset/model, threshold, hướng tối ưu và mobile stack vẫn là candidate/câu hỏi; chưa có kết quả benchmark hay pilot để tuyên bố giảm nhân sự. Dữ liệu công khai cho phần thị giác và fixture giả lập cho logic nghiệp vụ không thay thế đánh giá tại kỳ thi thật.

## Bước tiếp theo theo thứ tự

1. **Review văn bản quyết định và đặc tả nghiệp vụ:** Minh Hy review D-001/D-002, scope và selection; bổ sung ngày/nguồn buổi thống nhất nếu có. Hai người đặc tả kỳ thi mục tiêu, quy chế, actor, luồng lượt vào, trạng thái/ngoại lệ, quyền xử lý và sửa sai. Ghi biên bản riêng trước khi xem điều gì là thầy xác nhận.
2. **Cổng B0 trước thí nghiệm:** kiểm tra file, annotation, quyền dùng dataset/weight, khả năng chạy và preprocessing; chọn protocol reference/probe 1:1, manifest/split dev–test–external không rò rỉ, thiết bị đo và metric FMR/FNMR cùng retry/manual, latency. Đặt acceptance criteria theo rủi ro nghiệp vụ trước khi xem test.
3. **Baseline rồi quyết định điểm tối ưu:** chỉ giữ candidate vượt cổng B0, chạy đối chứng cùng dữ liệu/split/thiết bị, phân tích lỗi theo stage và tác động đầu-cuối. Sau đó mới chọn bottleneck, biến/search space/objective và phép thử cải thiện/ablation. Final technical decision phụ thuộc kết quả này.

**Task, người phụ trách và trạng thái chi tiết:** [Google Sheet chung](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0). Trang này tóm tắt tiến độ và việc kế tiếp, không sao chép bảng task.
