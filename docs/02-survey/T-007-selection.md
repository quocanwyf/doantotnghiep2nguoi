# T-007 — Chọn hướng khảo sát để đưa vào thí nghiệm

**Nguồn quyết định:** [D-001 chọn bài toán cửa phòng thi](../00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md) và [D-002 chọn hướng T-005](../00-project/decisions/T-007-D-002-chon-huong-khao-sat-t005.md). Quốc An xác nhận ngày 2026-09-25 rằng nhóm đã chốt T-004 theo T-002 và T-007 theo T-005. Quyết định T-007 đã chốt ở cấp nhóm; văn bản có thể được rà soát trong PR.

## Câu hỏi cần quyết ở Survey

Với lượt kiểm tra **có mã khai báo, một hồ sơ tham chiếu, xác minh 1:1 và kiểm tra phòng/ca/giờ**, hướng khảo sát nào tạo được candidate và phép thử đúng bài toán? Quyết định ở đây chỉ xác định **hướng và candidate đáng thử**, không xác định hệ thống cuối dùng dataset/model nào.

## Đối chiếu hai đề xuất theo requirement đã chọn

- [T-005 của Quốc An](README.md) xuất phát từ bài toán cửa phòng thi: S0–S11 tách truy vấn, camera, chọn người mục tiêu, detection, quality, embedding, verification 1:1, rule nghiệp vụ và audit. Bộ dữ liệu được phân theo annotation/vai trò; model được khảo sát từ task → family → candidate; B0–B4 nêu câu hỏi, metric và đối chứng trước khi có kết quả.
- [T-006 của Minh Hy](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2) xuất phát từ điểm danh lớp từng người nhưng **nhận dạng 1:N** trong gallery của phiên học; đề xuất MobileFaceNet, baseline B0/B1 và nhánh ROI/TPE sau pilot. Quy trình, dữ liệu người tham gia và FPIR/FNIR của 1:N không thay trực tiếp cho claim 1:1, roster phòng/ca và FMR/FNMR của T-002. Các nguyên tắc về tách split, random-search đối chứng, pilot để chứng minh bottleneck và đo thiết bị vẫn hữu ích.

**Lý do chọn T-005:** nó khớp D-001 ở loại bài toán, input/output từng stage và ranh giới ML–database–business logic. Chọn T-006 làm hướng chính sẽ đổi lại problem formulation đã chốt hoặc buộc chuyển metric/candidate từ 1:N sang 1:1 mà chưa có khảo sát tương ứng.

## T-005 đã hoàn thiện tới đâu?

**Hoàn thiện ở mức tài liệu Survey có thể review và dùng để thiết kế baseline:**

1. [Phân rã task](T-005-quoc-an-task-decomposition.md): S0–S11, input/output, điều kiện lỗi và stage nào cần model.
2. [Khảo sát dataset](T-005-quoc-an-datasets.md): criteria/annotation/vai trò theo stage, candidate, quyền dùng và gap nhãn người mục tiêu trong cảnh nhiều mặt.
3. [Khảo sát model](T-005-quoc-an-models.md): yêu cầu → family → shortlist có điều kiện; tách architecture, loss, weight và pipeline.
4. [Thiết kế thí nghiệm](T-005-quoc-an-experiments.md): baseline plan, B0–B4, metric, split, error analysis, bottleneck gate và ablation. [Logic quyết định](DECISION_LOGIC.md) nối bốn tài liệu này với bài toán nghiệp vụ.

**Chưa hoàn thiện ở mức thực nghiệm/triển khai:** chưa tải và xác minh toàn bộ tệp/quyền/weight, chưa chọn main test và thiết bị, chưa khóa operating point/acceptance criteria, chưa chạy baseline, chưa biết bottleneck. Vì vậy chưa có final dataset, model, threshold, optimization hay bằng chứng giảm nhân sự.

## Quyết định T-007 và bước kiểm chứng tiếp theo

Dùng T-005 làm cơ sở để (1) kiểm tra khả dụng/giấy phép và chốt manifest dữ liệu; (2) chọn một main verification protocol 1:1 cùng external tests theo gap; (3) lọc candidate detector/encoder bằng gate đã nêu; (4) chốt cùng split, metric, thiết bị và tiêu chí chấp nhận trước test; (5) chạy baseline, phân tích lỗi rồi mới chọn optimization target. Khi một candidate vượt qua gate, đó vẫn là **candidate đem thí nghiệm**. Final technical decision chỉ được ghi sau kết quả thí nghiệm trên cùng điều kiện và review của nhóm.
