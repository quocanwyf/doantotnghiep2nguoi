# D-005 — Duyệt Group 2: auto-check-in có điều kiện trong demo

- **Trạng thái:** Approved for demo profile — Group 2; Group 1 theo [D-004](T-024-D-004-duyet-default-demo.md), toàn T-024 chưa freeze.
- **Ngày/người chốt:** 2026-09-30, Quốc An.
- **Nguồn:** xác nhận trực tiếp trong cuộc trò chuyện: “mình chốt Group 2 theo phương án auto-check-in có điều kiện”, kèm yêu cầu flag quyền và mode chờ xác nhận. Không tự ghi nhận phê duyệt thêm của Minh Hy/thầy hoặc quyền vận hành kỳ thi thật.

## Vấn đề, phương án và lý do

Nếu mọi lượt đều cần người bấm xác nhận cuối, demo chủ yếu đề xuất kết quả và chưa đạt mục tiêu giảm thao tác đối chiếu thủ công ở ca bình thường. Chọn **auto-check-in có điều kiện**, giữ mode xác nhận có thẩm quyền bằng config, không thay pipeline AI.

**Auto-check-in là quyền của demo profile, không phải hệ quả mặc định của `AI_VERIFIED`.**

## Quyết định

Decision Engine chỉ tự ghi khi tất cả đều đúng:

1. Business pre-check OK.
2. AI_VERIFIED theo AIConfig của lượt.
3. Final business-check OK, policy/data/reference/context còn hợp lệ.
4. Không duplicate, không exception chưa giải quyết.
5. `auto_checkin_enabled=true` trong profile đã được duyệt.

Sau đó **ghi check-in thành công mới PASS**. Write chưa biết thành công → SYSTEM_HOLD/reconcile; không ghi tiếp một kết quả mới hoặc hiển thị PASS sớm.

- **Mode demo được duyệt:** `auto_checkin_enabled=true` cho profile được phê duyệt; ca bình thường không cần người xác nhận mỗi lượt.
- **Mode thận trọng:** `auto_checkin_enabled=false`; cùng pipeline và các kiểm tra đạt → `READY_FOR_CONFIRMATION`, chưa có effective check-in. Người có quyền xác nhận → final recheck → ghi thành công → PASS. Chưa có người xác nhận thì giữ pending, không tự PASS.
- Flag thiếu/không hợp lệ hoặc profile không đáng tin → SYSTEM_HOLD; không suy quyền từ score. Quyền chỉnh flag thuộc policy/profile đã duyệt, không là quyền đổi model/threshold.

Nhánh không đủ điều kiện giữ nguyên: AI chưa verified → RETRY/MANUAL; business mơ hồ → MANUAL; data/policy lỗi → SYSTEM_HOLD; duplicate/re-entry → MANUAL; write chưa rõ → SYSTEM_HOLD.

## Tác động, audit và giới hạn

Workflow phải support `READY_FOR_CONFIRMATION` riêng với exception MANUAL. Ghi mode/flag và policy version, actor/system đưa quyết định, evidence, thời điểm final recheck và kết quả write. Xác nhận sau khi chờ phải dùng context/reference đúng lượt và dữ liệu còn hiệu lực; không bỏ qua các điều kiện mới phát sinh.

PASS chỉ là check-in confirmed, không tự cấp quyền vào phòng/attendance. Group 2 không cấp sẵn quyền override/late/re-entry/correction cho một role cụ thể; những quyền đó thuộc Group 3. Không đổi AIConfig, không chọn threshold demo hay chứng minh đạt false-accept cap. Mode/config chỉ có hiệu lực vận hành sau khi profile/test scope được freeze theo các phần còn lại.

**Bước tiếp:** Group 3 — ai nhận MANUAL/READY_FOR_CONFIRMATION, quyền xử lý từng case và escalation; sau đó Group 4 — risk/test acceptance. Không thay quyết định Group 1 hoặc sửa kết quả nghiên cứu trước.

**Cập nhật kế tiếp ngày 2026-09-30:** Quốc An đã duyệt Group 3 tại [D-006](T-024-D-006-manual-authority.md). Quyết định đó bổ sung role/scope/evidence guards và route HUMAN riêng, không thay điều kiện auto-check-in của D-005; hiện tiếp tục Group 4 risk/test acceptance.
