# D-002 — Dùng khảo sát T-005 làm hướng nghiên cứu của nhóm

- **Trạng thái:** Nhóm đã chốt T-007 theo T-005, theo xác nhận của Quốc An về quyết định chung với Minh Hy. Đây là **survey decision**, chưa phải final technical decision.
- **Ngày ghi nhận:** 2026-09-25.
- **Người chốt/xác nhận:** Quốc An và Minh Hy, theo xác nhận trực tiếp của Quốc An rằng nhóm đã chốt T-004 theo T-002 và T-007 theo T-005. Chưa có biên bản buổi chốt riêng trong repo.
- **Nguồn:** xác nhận của Quốc An trong trao đổi ngày 2026-09-25; [D-001](D-001-chon-bai-toan-cua-phong-thi.md), [khảo sát T-005](../../02-survey/README.md) và [khảo sát độc lập T-006](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2).

## Vấn đề và phương án

Sau khi chọn nghiệp vụ tại cửa phòng thi có mã khai báo và xác minh 1:1, nhóm cần một hướng khảo sát phục vụ đúng các stage và rủi ro của use case đó. T-005 phân rã S0–S11, suy yêu cầu dữ liệu/model theo stage và thiết kế thí nghiệm B0–B4 cho 1:1. T-006 phát triển từ điểm danh lớp 1:N, ảnh/người tự thu và hướng ROI/TPE có điều kiện.

## Lựa chọn và lý do

Chọn **T-005 làm khung khảo sát chính cho bước thí nghiệm** vì nó trực tiếp suy ra từ D-001: mã → một hồ sơ → chọn đúng người trước camera → verification 1:1 → kiểm tra phòng/ca/giờ → ghi nhận. T-005 tách ML khỏi rule/database và chỉ đưa dataset/model vào shortlist có điều kiện sau khi nêu requirement. Phương án T-006 trả lời một business use case khác; các nguyên tắc chung về split, đối chứng và đo tài nguyên vẫn có thể tham khảo, nhưng không chuyển nguyên metric 1:N, dataset, model hoặc ROI/TPE sang bài toán phòng thi.

## Phạm vi của quyết định Survey

- **Dữ liệu:** theo tiêu chí/shortlist từng stage của T-005; dùng nguồn công khai cho nghiên cứu thị giác và fixture giả lập cho nghiệp vụ. Chưa chọn main dataset hay khẳng định đủ nhãn cho S4 người mục tiêu.
- **Baseline và phép đo:** theo cấu trúc B0–B4 của T-005; verification 1:1 cần FMR/FNMR tại operating point có nguồn, cùng tỷ lệ retry/manual, lỗi nghiệp vụ và latency/tài nguyên khi có thiết bị. Chưa có baseline chạy thật, threshold hay acceptance criteria định lượng được chốt.
- **Model/candidate:** các family và shortlist T-005 là ứng viên **để kiểm tra khả dụng và benchmark**, không là detector/encoder triển khai cuối.
- **Optimization:** chưa chọn bottleneck, search space/objective hoặc thuật toán. Chỉ chọn sau baseline và phân tích lỗi có nhãn; không chọn ROI/TPE trước để rồi tìm bằng chứng biện minh.

## Bằng chứng, giới hạn và ảnh hưởng

Căn cứ hiện là sự phù hợp logic giữa use case và khảo sát, chưa phải kết quả thực nghiệm. [Bản so sánh T-007](../../02-survey/selection.md) ghi mức hoàn thiện T-005 và việc còn phải kiểm chứng. Bước sau: xác minh tệp/quyền/trọng số, khóa protocol/split/metric/thiết bị, chạy baseline và quyết định kỹ thuật cuối từ kết quả. Minh Hy có thể rà soát cách ghi văn bản này trong PR; việc rà soát không làm thay đổi trạng thái quyết định nhóm đã chốt. Chưa có xác nhận của thầy.
