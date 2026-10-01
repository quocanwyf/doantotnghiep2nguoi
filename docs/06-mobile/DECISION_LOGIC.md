# Logic & Decision Rationale — 06 Mobile / Integration

## T-024 → bàn giao app: vì sao bước tiếp theo là implement

**Context / observation:** B0 multi-face unresolved dẫn tới selective S4/P2; T-020 phát hiện selected cosine cao sai có thể qua cả S4/S8. T-021–T-023 kiểm hard-negative risk và encoder separation. T-023 có operating region hữu ích nhưng còn 8/38 hard-negative accept tại θ nghiên cứu 0.23; chưa có evidence buộc thay/fine-tune MobileFaceNet. T-024 D-004–D-007 đã chốt default demo, auto authority, manual authority và cách báo test.

**Question:** làm sao biến AI research configuration và policy đã chốt thành ứng dụng hoạt động end-to-end? Có cần tiếp tục ngồi freeze toàn bộ test trước khi app tồn tại không?

**Requirements / alternatives:** app phải resolve hồ sơ/context, giữ authority/retry, nối đúng reference–observation–S4–S8, final-check và confirmed write/audit. Có thể tiếp tục chuẩn bị test chi tiết trước hoặc bắt đầu integration từ contract hiện có. Test freeze cần trước test chính thức; không phải trước mọi thao tác phát triển app.

**Decision / source:** Quốc An yêu cầu ngày 2026-10-01 chuyển sang app/integration và chuẩn bị một bộ MD cho Hy; [D-008](../00-project/decisions/T-024-D-008-ban-giao-va-build-app.md) ghi quyết định. [Bộ bàn giao](T-024-ban-giao-app-cho-hy/T-024-README.md) là đầu vào triển khai. Hy chọn UI/stack/chi tiết nghiệp vụ và ghi quyết định; An giữ/bàn giao mốc AI hiện tại. Không mở model/fine-tune hoặc retune từ holdout cũ.

**Why / what this affects next:** đủ business contract và AI evidence để dựng app → UI/business mock → adapter/observation/S4/S8 → retry/manual/write/audit → end-to-end development → freeze cấu hình/input/case cho test cuối → workflow PASS/FAIL + observed attempt-level AI errors → integration/demo/report. [Test-profile preparation](../01-problem/T-024-test-profile-preparation.md) chỉ là checklist về sau. Cap TBD không cản build/test nhưng chưa có safety acceptance. Camera thực địa vẫn là giới hạn của kết luận.

**Implementation gap cần nói rõ:** code P2 nghiên cứu chỉ nhận ≥2 score; dispatcher single-face B0 + multi-face P2 được đề xuất trong bộ bàn giao, chưa là app API đã implement/freeze. Model pack vẫn là weight nghiên cứu, chưa xác nhận Hy đã nhận; contract DTO là đề xuất integration. Những lựa chọn này cần note theo output thực tế khi app được xây, không gọi tài liệu bàn giao là kết quả chạy app.
