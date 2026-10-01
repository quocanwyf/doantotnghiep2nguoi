# D-006 — Duyệt Group 3: quyền xử lý thủ công theo ba tầng

- **Trạng thái:** Approved for demo profile — Group 3; kế tiếp [D-004](T-024-D-004-duyet-default-demo.md) và [D-005](T-024-D-005-auto-checkin-co-dieu-kien.md). Toàn T-024 chưa freeze; Group 4 risk/test acceptance còn mở.
- **Ngày/người chốt:** 2026-09-30, Quốc An.
- **Nguồn:** xác nhận trực tiếp trong cuộc trò chuyện: “mình chốt Group 3 theo mô hình 3 tầng hiện tại”, kèm ranh giới quyền và ba điều kiện cho manual identity verification. Không ghi nhận thêm phê duyệt của Minh Hy/thầy hay thẩm quyền tại một kỳ thi thật.

## Context → question → alternatives → decision

Group 1 chuyển ngoại lệ sang MANUAL; Group 2 có nhánh READY_FOR_CONFIRMATION. App cần biết ai được quyết định từng case. Dồn mọi ngoại lệ lên Exam Admin có thể làm MANUAL thành nút thắt, trong khi giao quyền không giới hạn cho operator sẽ làm mất ranh giới authority. Quốc An duyệt ba tầng, cho cán bộ phòng giải quyết việc cục bộ trong quyền được ủy quyền và giữ việc dữ liệu/policy/correction/lifecycle ở admin.

| Role | Quyền đã duyệt ở mức demo profile | Ranh giới |
| --- | --- | --- |
| OPERATOR | Hướng dẫn, retry/resume trong budget, redirect theo nguồn và route case. | Không quyết định identity, late exception, re-entry, sửa record hoặc PASS. |
| AUTHORIZED_ROOM_STAFF | Xác nhận READY_FOR_CONFIRMATION; manual identity verification theo ba điều kiện dưới; late quá 15 phút khi intake còn mở; re-entry/duplicate cục bộ nếu profile đã cấp quyền. | Trong scope phòng/ca và quyền được ủy quyền. Không sửa dữ liệu nguồn, blocked eligibility, mở ca đã đóng hoặc correction check-in đã ghi. |
| EXAM_ADMIN | Xử lý roster/reference mâu thuẫn, sai registration, blocked eligibility, closed-session exception, write chưa rõ, correction, reconciliation/fallback, role/policy administration. | Cần căn cứ/thẩm quyền nguồn; không tự biến thông tin chưa rõ thành success hoặc sửa verdict AI. |

**Manual identity verification chỉ được thực hiện khi đồng thời có:**

1. Role được cấp quyền này.
2. Evidence method được policy duyệt.
3. Case nằm trong scope phòng/ca của actor.

Thiếu một điều kiện → **ESCALATE**; thiếu evidence đáng tin thì giữ pending, không “thấy giống là cho qua”. D-006 duyệt capability/quyền có điều kiện, chưa tự chọn loại giấy tờ hoặc evidence method cụ thể.

- **Late:** ≤15 phút và intake mở theo Group 1; >15 phút nhưng intake mở thì Room Staff có quyền exception được xử lý, nếu không chuyển Admin. Ca đã đóng thuộc Admin/lifecycle policy, không mở lại bằng quyền late.
- **Re-entry/duplicate:** giữ check-in cũ, xử lý yêu cầu quay lại riêng, không tạo PASS/check-in thứ hai. Vượt policy hoặc cần sửa record → Admin.
- **Data/fallback:** Room Staff không dùng manual identity để bỏ qua registration/eligibility/policy mâu thuẫn. Admin điều phối phục hồi và đối soát; biên nhận fallback tạm chưa tự là effective PASS.

## Human decision ≠ AI verdict

Human có thể đưa quyết định **HUMAN độc lập** từ evidence được duyệt, nhưng không sửa `NOT_VERIFIED` thành `AI_VERIFIED`, không sửa score/threshold hoặc lịch sử AI. Ví dụ S8 vẫn NOT_VERIFIED; sau manual identity hợp lệ, business/final checks và authority đều đủ, không duplicate, ghi thành công thì có **manual-approved check-in**, với decision source HUMAN. Lượt này không được tính thành AI success.

READY_FOR_CONFIRMATION là xác nhận lượt đã đạt, khác manual verification của một exception. Mọi route ghi mới vẫn phải final recheck và xác nhận write; quyền manual không cho vượt SYSTEM_HOLD hoặc ghi thêm check-in trùng.

## Audit → tác động tiếp theo

Lưu actor, role/quyền được dùng, scope phòng/ca, timestamp, reason/evidence method, policy/data/AIConfig version, verdict AI gốc, quyết định HUMAN riêng và kết quả trước/sau. Correction giữ lịch sử; không sửa ground truth/output nghiên cứu sau khi xem kết quả.

App dùng [business-policy mục 3.1](../../01-problem/T-024-business-policy.md#31-group-3--manual-authority-đã-duyệt) làm contract. Trước dùng nhánh thực tế phải gán người/tài khoản, delegation và evidence method đã duyệt; timeout/retention còn theo trạng thái riêng. Không có người nhận thì pending/escalate, không auto-approve.

**Vì sao Group 4 tồn tại:** quyền quyết định đã rõ, nhưng quyền không chứng minh chất lượng identity verification. T-023 vẫn có 8/38 hard negative accept trong proxy. Cần chốt risk/test acceptance trước freeze/test; không tự đặt false-accept cap, retune S8, mở experiment model hoặc merge PR từ D-006.

**Cập nhật kế tiếp 2026-10-01:** Quốc An duyệt Group 4 tại [D-007](T-024-D-007-workflow-va-risk-evaluation.md), tách workflow PASS/FAIL với observed AI risk khi cap TBD. Quyền D-006 giữ nguyên; tiếp theo bind/freeze test profile, không sửa kết quả AI cũ.
