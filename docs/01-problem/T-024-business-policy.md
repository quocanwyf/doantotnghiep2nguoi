# T-024 — Business policy, tình huống và quyền cấu hình

**Trạng thái:** Group 1/2 **Approved for demo profile** ngày 2026-09-30 theo [D-004](../00-project/decisions/T-024-D-004-duyet-default-demo.md)/[D-005](../00-project/decisions/T-024-D-005-auto-checkin-co-dieu-kien.md); toàn profile chưa freeze. Group 3 ở mục 3.1 là **đề xuất để Quốc An review**, chưa cấp quyền cho role. Kế thừa [T-008](T-008-requirements.md); đọc [quy trình tổng](T-024-demo-decision-policy.md) và [AI/retry](T-024-ai-rule-and-retry.md) trước triển khai.

## 1. Pre-session và cấu hình

Trước intake: xác định kỳ thi/ca/phòng của thiết bị; roster/registration và reference mapping có nguồn/phiên bản; policy/AIConfig đúng profile; người có quyền nhận MANUAL/fallback; trạng thái sẵn sàng. Thiếu context/policy/data đáng tin → SYSTEM_HOLD, không tự ghi PASS.

Config là **cách xử lý theo quy định**, không phải dữ liệu identity hay eligibility. Room/session assignment có thể được người có quyền sửa ở nguồn nhưng không phải operator đổi tham số để bỏ qua sai phòng/ca.

| Policy/key | Default demo (trạng thái theo đoạn dưới) | Có thể chỉnh / người duyệt |
| --- | --- | --- |
| TimePolicy.early_checkin_minutes | TBD; số 30 trong nguồn chỉ là ví dụ | Người quản lý profile duyệt cửa sổ và mốc thời gian. |
| TimePolicy.late_allowed_minutes | 15 phút | Có; không hard-code hoặc gán quy chế kỳ thi thật. |
| TimePolicy.late_within_limit_action | CONTINUE_WITH_LATE_FLAG | Có trong quyền được duyệt. |
| TimePolicy.late_after_limit_action | MANUAL | Có; CHECK_IN_NOT_ALLOWED là lựa chọn cần duyệt riêng. |
| EligibilityPolicy.actions | ELIGIBLE → CONTINUE; CANCELLED/SUSPENDED/DISQUALIFIED → CHECK_IN_NOT_ALLOWED; trạng thái chưa rõ → MANUAL | Chỉ trong quyền và ràng buộc kỳ thi; không chỉnh trạng thái nguồn bằng policy. |
| DuplicatePolicy.active_attempt | RESUME | Không reset evidence/retry; một effective check-in. |
| DuplicatePolicy.already_checked_in | MANUAL / route re-entry | Có; không tạo check-in thành công thứ hai. |
| ReEntryPolicy.action | MANUAL | Có; ALLOW_WITH_VERIFICATION/BLOCK chỉ là lựa chọn tương lai, chưa bật. |
| ReferencePolicy.missing/unusable | MANUAL | Có thể đổi route trong quyền; không bỏ xác minh rồi gắn nhãn AI_VERIFIED. |
| RetryPolicy | Xem bảng duy nhất ở tài liệu AI | Người quản lý demo/operational profile duyệt; version lại và kiểm tác động toàn lượt. |
| DecisionPolicy.auto_checkin_enabled | true trong demo profile được duyệt; hỗ trợ false → READY_FOR_CONFIRMATION | Approved Group 2; thay mode cần quyền/version của profile, không đổi AIConfig. Role cụ thể ở Group 3. |
| ManualPolicy.receiver/timeout/action | TBD | Gán role/quyền trước dùng branch; timeout không tự thành success. |
| DataPolicy.roster/policy_unavailable | SYSTEM_HOLD | Fallback thủ công cần actor/quyền và đối soát. |
| EvidencePolicy.retention/access | TBD | Quyền đọc/lưu phù hợp phạm vi dữ liệu được duyệt. |

**Đã duyệt Group 1:** late 15 phút + intake còn mở → LATE/CONTINUE; quá 15 phút → MANUAL; ca đóng theo lifecycle riêng; already checked-in/re-entry → MANUAL, không duplicate; eligibility mapping, missing/unusable reference → MANUAL; policy/roster unreliable → SYSTEM_HOLD; retry keys đã duyệt ở bảng duy nhất trong tài liệu AI. Early window vẫn TBD. Các mục manual/retention/authority và chi tiết ngoài phạm vi xác nhận không tự được duyệt theo Group 1. Không dùng placeholder/TBD để tiếp tục branch tự động phụ thuộc chúng.

**Đã duyệt Group 2:** auto-check-in là quyền của profile, không tự suy từ AI_VERIFIED. True + mọi business/final checks đạt, không duplicate/exception unresolved → ghi thành công → PASS. False + lượt đạt → READY_FOR_CONFIRMATION; người được ủy quyền xác nhận, recheck sau chờ và ghi thành công mới PASS. Profile/flag lỗi → SYSTEM_HOLD; không mặc định bật quyền khi thiếu config.

## 2. Case matrix trước camera

Trong bảng, “config” là hành động/route có thể cấu hình; dữ liệu nguồn vẫn phải có thẩm quyền. `CONTINUE` nghĩa tiếp tục kiểm các điều kiện còn lại, không bỏ qua condition khác.

| ID | Tình huống | Hành động theo profile (phạm vi duyệt ở mục 1) | Config / nguồn |
| --- | --- | --- | --- |
| BP-ID01 | Mã trống/sai format | Yêu cầu sửa input; chưa camera. | Format theo loại identifier chọn cho demo, TBD. |
| BP-ID02 | Không tìm thấy registration | Nhập lại hoặc SUPPORT/MANUAL; không tự tạo hồ sơ. | Lookup từ roster hiệu lực; support route configurable. |
| BP-ID03 | Nhiều hồ sơ không phân biệt được | MANUAL; cần resolve một claimed record. | Context/metadata nguồn, không dùng AI để hợp thức mapping mơ hồ. |
| BP-ID04 | Một registration được resolve | CONTINUE. | Mã là claim, chưa chứng minh người thật là identity đó. |
| BP-ID05 | Người dùng báo hồ sơ hiển thị sai | Sửa claim hoặc MANUAL; không tái dùng evidence của reference cũ. | UI confirmation theo demo scope; input correction không tính AI retry. |
| BP-R01 | Đúng phòng | CONTINUE. | Assignment nguồn. |
| BP-R02 | Sai phòng và biết phòng đúng | REDIRECT, chưa camera. | RoomPolicy cho routing; không tự sửa assignment. |
| BP-R03 | Assignment phòng mâu thuẫn | MANUAL. | Người có quyền sửa nguồn, audit. |
| BP-R04 | Context phòng thiết bị sai | SYSTEM_HOLD. | Người có quyền cấu hình lại context. |
| BP-S01 | Đúng ca, intake đang mở | CONTINUE. | Session lifecycle + policy hiệu lực. |
| BP-S02 | Chưa đến cửa sổ của ca | INFO/WAIT. | Early/arrival window configurable. |
| BP-S03 | Intake/ca đã đóng hoặc ca đã kết thúc | Không tự mở lại; MANUAL hoặc CHECK_IN_NOT_ALLOWED theo lifecycle policy. | **Không chỉ chuyển sang LatePolicy**; reopen cần quyền. |
| BP-S04 | Không đăng ký ca/môn này | CHECK_IN_NOT_ALLOWED; tranh chấp → người có quyền. | Registration nguồn; exception authority. |
| BP-S05 | Dữ liệu ca không rõ/mâu thuẫn | MANUAL/SYSTEM_HOLD. | Độ tin cậy nguồn và phạm vi lỗi. |
| BP-T01 | Trong cửa sổ đến hợp lệ | CONTINUE. | Arrival window theo ca; mốc/clock dùng cho demo TBD. |
| BP-T02 | Muộn trong giới hạn demo khi intake còn mở | Gắn LATE flag, CONTINUE các kiểm khác. | Approved Group 1: 0 < late ≤ 15 phút. |
| BP-T03 | Vượt giới hạn muộn | MANUAL. | Có thể duyệt hành động khác; không mặc định cấm thi. |
| BP-E01 | ELIGIBLE | CONTINUE. | Status từ nguồn có thẩm quyền. |
| BP-E02 | CANCELLED/SUSPENDED/DISQUALIFIED | CHECK_IN_NOT_ALLOWED theo policy; tranh chấp có route riêng. | AI không tạo/đổi status hoặc quyền override. |
| BP-E03 | PENDING/UNDER_REVIEW/UNKNOWN/conflict | MANUAL; không coi là ELIGIBLE. | Routing configurable, status không tự đoán. |
| BP-D01 | Đang có active attempt | Resume cùng lượt, giữ retry counters. | Duplicate invariant, không mở vô hạn attempt song song. |
| BP-D02 | Đang có manual case | Resume/link case, giữ unresolved tới khi người có quyền xử lý. | Receiver/routing configurable. |
| BP-D03 | Đã có effective check-in | ALREADY_CHECKED_IN; route MANUAL/re-entry, không ghi lần hai. | Duplicate/ReEntryPolicy. |
| BP-RE01 | Có yêu cầu quay lại/rời rồi vào lại | MANUAL trong demo; giữ check-in cũ. | Không suy đã rời từ việc mất mặt trong camera; entry/exit cần evidence riêng nếu trong scope. |
| BP-REF01 | Reference đúng mapping và dùng được | CONTINUE sang camera khi mọi business check đủ. | Nguồn/version reference. |
| BP-REF02 | Reference thiếu/corrupt/unusable/mapping không chắc | MANUAL; không camera-retry để chữa dữ liệu nguồn. | ReferencePolicy + người sửa dữ liệu. |
| BP-REF03 | Có nhiều reference | Chỉ dùng khi đã có quy tắc chọn reference được freeze; chưa có → MANUAL. | Không chọn reference theo score evaluation. |
| BP-SYS01 | Roster/data cần cho quyết định không truy cập được | SYSTEM_HOLD hoặc fallback được ủy quyền. | Không mặc định offline cache luôn hợp lệ. |
| BP-SYS02 | Data quá cũ/không biết hiệu lực, không đáng tin để quyết định | SYSTEM_HOLD; fallback có người xử lý chỉ theo quyền được duyệt. | Freshness/validity rule TBD; không đặt số tùy ý. |
| BP-SYS03 | Policy thiếu hoặc context/config sai | SYSTEM_HOLD. | Chỉ profile hợp lệ được phép chạy. |
| BP-SYS04 | Không biết lần ghi đã thành công chưa | Reconcile trước lần ghi tiếp; không báo PASS sớm. | Một effective check-in, giữ attempt/write evidence. |
| BP-SYS05 | Policy/roster đổi trong attempt | Final recheck và log version trước/sau; cần quyền thì MANUAL. | Không âm thầm áp policy mới lên kết quả cũ. |

Nhiều điều kiện có thể cùng tồn tại: lưu tất cả flag/reason; điều kiện chưa giải quyết không được một condition CONTINUE khác ghi đè. Hướng dẫn phòng/ca lấy từ dữ liệu hiệu lực; AI không cần giải quyết các bước lookup/rule này.

## 3. Final-check, manual và correction

Sau AI_VERIFIED, kiểm registration/context/eligibility/policy còn hiệu lực, duplicate và quyền auto-check-in. Arrival timestamp của lượt đến giữ riêng với thời gian xử lý để retry/queue không tự làm đổi sự kiện đến; cách xác lập mốc và late rule phải nằm trong profile.

- Đủ điều kiện và `auto_checkin_enabled=true` trong profile đã duyệt → ghi một effective check-in, xác nhận commit rồi PASS.
- Đủ điều kiện nhưng flag false → READY_FOR_CONFIRMATION. Xác nhận từ actor được ủy quyền → recheck context/evidence/business/duplicate sau chờ → ghi thành công → PASS. Chưa được xác nhận thì giữ pending, không ghi check-in tự động.
- Chưa đủ dữ liệu/thẩm quyền hoặc có tranh chấp → MANUAL/SYSTEM_HOLD, không silently success.
- **Manual/override:** người được ủy quyền xử lý ngoại lệ đang có; lưu actor/quyền, thời gian, reason, evidence và outcome. Không giả rằng operator có mọi quyền.
- **Correction:** sửa kết quả đã ghi khi có evidence mới; lưu trước/sau và liên kết bản cũ, không xóa lịch sử hoặc viết lại output nghiên cứu.
- **Fallback:** khi automation/device hỏng, người có quyền ghi biên nhận tạm với context/candidate hoặc unresolved claim, thời gian và reason. Sau phục hồi phải reconcile điện tử/thủ công trước sync; không auto-confirm nếu chưa resolve identity/duplicate.
- **End session:** đóng routine intake, tập hợp pending/fallback, đối soát; attendance theo định nghĩa riêng. Thiếu evidence → UNDETERMINED, không tự absent chỉ vì chưa PASS. Reopen/correction phải có quyền và audit.

### 3.1. Group 3 — đề xuất manual authority để duyệt

**PROPOSED, chưa là quyền đã được cấp.** Đề xuất ba role nghiệp vụ; tên role mô tả quyền, chưa gán cho An/Hy hoặc nhân sự kỳ thi thật. Một người demo có thể giữ nhiều role nếu được cấp rõ, nhưng log phải ghi actor và quyền dùng ở từng quyết định.

| Role đề xuất | Nhận/xem | Được xử lý trong đề xuất | Phải escalate / không tự làm |
| --- | --- | --- | --- |
| OPERATOR — người vận hành thiết bị | Case của phòng/ca được giao, MANUAL/READY pending | Hướng dẫn nhập lại mã/đứng camera, redirect theo roster, resume/recovery trong budget, gửi case cho người có quyền. | Không tự confirm PASS, duyệt late/re-entry, đổi roster/reference/eligibility, sửa check-in hoặc giảm threshold. |
| AUTHORIZED_ROOM_STAFF — cán bộ phòng được ủy quyền | Case của phòng/ca được giao, evidence cần thiết | Confirm READY_FOR_CONFIRMATION; xác minh thủ công khi AI chưa verified/unavailable theo evidence policy; duyệt late/re-entry **chỉ trong phạm vi được profile ủy quyền**; resolve duplicate bằng record hiện hành, không ghi lần hai. | Mâu thuẫn identity/reference/roster, status blocked, ca đóng, không đủ evidence/quyền, correction bản ghi đã chốt, write chưa rõ → EXAM_ADMIN. |
| EXAM_ADMIN — người quản lý profile/dữ liệu | Case được escalate và dữ liệu trong quyền quản lý | Gán quyền/role; duyệt policy/mode theo version; xử lý dữ liệu nguồn với căn cứ có thẩm quyền; duyệt correction/reconciliation và exception vượt quyền phòng khi có rule/evidence phù hợp. | Không biến chưa rõ thành success, sửa verdict AI/score, tùy ý đổi model/threshold hoặc xóa lịch sử. Không có căn cứ/thẩm quyền nguồn thì giữ pending và chuyển chủ thể có thẩm quyền. |

| Case / source | Người nhận đầu tiên | Người quyết định đề xuất | Điều kiện / giới hạn |
| --- | --- | --- | --- |
| Lượt đạt, flag false (D-005) | OPERATOR route | AUTHORIZED_ROOM_STAFF | Confirm thường, không là AI override; final recheck và write thành công mới PASS. |
| AI unresolved/not verified, exhausted retry (AI-S406/S803) | OPERATOR route | AUTHORIZED_ROOM_STAFF nếu có quyền manual identity verification | Evidence thủ công theo policy, business vẫn phải hợp lệ; thiếu evidence → pending/escalate, không buộc PASS. |
| Late trong 15 phút/intake mở (BP-T02) | Luồng bình thường | System theo Group 1/2 | Không cần human approve late riêng nếu mọi điều kiện khác đạt. |
| Late quá 15 phút nhưng intake còn mở (BP-T03) | OPERATOR route | AUTHORIZED_ROOM_STAFF **nếu được cấp quyền late exception**, nếu không EXAM_ADMIN | Ghi lý do/authority; không dùng quyền late để tự mở ca đóng hoặc bỏ identity verification. |
| Duplicate/re-entry (BP-D03/RE01) | OPERATOR route | AUTHORIZED_ROOM_STAFF trong quyền re-entry của profile | Giữ effective check-in cũ; ghi xử lý yêu cầu quay lại riêng. Không suy attendance/entry-exit từ detector hoặc tạo PASS record thứ hai. |
| Không tìm được hồ sơ duy nhất/reference sai/thiếu (BP-ID02/03, REF02) | OPERATOR route | EXAM_ADMIN cho sửa nguồn; cán bộ phòng chỉ manual-verify nếu có evidence/quyền thay thế được duyệt | Không tự tạo registration/identity hoặc chọn reference theo score. |
| CANCELLED/SUSPENDED/DISQUALIFIED, wrong session/ca đóng (BP-E02/S03/S04) | OPERATOR route | EXAM_ADMIN hoặc chủ thể có thẩm quyền nguồn | Cán bộ phòng không override trạng thái/quyền; cần giải quyết theo dữ liệu/policy/lifecycle, không chỉ bấm approve. |
| Policy/roster unreliable, config lỗi, write chưa rõ (BP-SYS01–05) | OPERATOR route | EXAM_ADMIN điều phối phục hồi/đối soát | Giữ SYSTEM_HOLD cho nhánh tự động. Fallback được ủy quyền có thể ghi biên nhận tạm; chưa resolve/reconcile thì không effective PASS. |
| Incorrect check-in/absence phát hiện sau (T-008 correction) | Cán bộ phòng báo evidence | EXAM_ADMIN trong correction authority | Ghi trước/sau/reason/actor; giữ lịch sử, đối soát attendance riêng, không sửa output nghiên cứu. |

**“Override AI” trong đề xuất:** được người có quyền kết luận theo evidence thủ công khi automation không đủ, **không sửa AI NOT_VERIFIED thành AI_VERIFIED**, không thay crop/score/threshold. Lưu căn cứ xác minh `HUMAN` riêng với `AI`, giữ verdict AI gốc và rule/version. Đây là manual-authorized route cần Group 3 duyệt, không là auto-PASS qua flag Group 2.

Report test phải tách outcome manual/human-confirmation với outcome AI. Metric S8 giữ verdict thật của component: xác nhận của con người không biến S8 reject/unresolved thành S8 accept; lượt READY đã có S8 accept vẫn báo component theo output gốc. Không dùng xác nhận manual để sửa ground truth sau khi xem kết quả.

Mọi quyết định confirm/exception/correction cần actor, role/quyền, scope phòng/ca, thời gian, reason/evidence, policy/AIConfig/data version và kết quả trước/sau. Điều kiện nghiệp vụ mới phát sinh phải được recheck trước ghi. Technical maintainer có thể phục hồi camera/runtime trong quyền nhưng không tự có quyền duyệt danh tính/late hoặc đổi AIConfig frozen.

**Cần Quốc An chốt:** ba role có phù hợp không; quyền manual identity verification cho cán bộ phòng; phạm vi late/re-entry exception; correction/escalation ở admin; gán người/tài khoản và evidence/timeout cho case thực sự demo. Không có người nhận hoặc hết quyền thì giữ pending, không mặc định auto-approve. Quyền manual được duyệt cũng chưa chứng minh đáp ứng risk cap ở Group 4.

## 4. Audit/version và contract cho app

Tối thiểu liên kết attempt → registration/context → observation/S4/S8 → business decision → effective check-in hoặc manual/confirmation case. Lưu timestamp, actor/system/role/quyền, reason/flags, nguồn/version roster/reference, `policy_version`, `ai_config_version`, giá trị auto-check-in/mode, nguồn quyết định automatic/authorized confirmation/manual exception, counters retry, final recheck và trạng thái lần ghi. Policy đổi late 15 → 20 hoặc true → false tạo version mới; vẫn truy ra lượt cũ dùng policy nào.

Model/detector/threshold chỉ đổi qua AIConfig được đánh giá/version, không là quyền chỉnh nghiệp vụ hàng ngày. Không đưa identity/ảnh/embedding lên Git. Retention, quyền đọc và mức evidence được lưu còn TBD; chỉ giữ dữ liệu phục vụ điều tra/correction trong quyền đã duyệt.

Hy có thể triển khai business workflow/UI/manual/fallback theo contract này và hoàn thiện chi tiết app trong scope của mình; An giữ AI output/config contract. Nếu thay đổi input/reference/verification semantics thì hai phần phải rà lại contract. T-024 không chọn mobile stack, database hoặc backend architecture.

## 5. Cần duyệt trước freeze

Group 1/2 đã duyệt theo D-004/D-005. Tiếp theo duyệt đề xuất Group 3 ở mục 3.1, rồi Group 4 — risk/test acceptance. Trước freeze cũng cần mode/nguồn đầu vào, early window, reference/quality capability thực sự có, policy/data effectiveness, retention và fallback cho case đưa vào test.

Chưa cần thiết kế mọi màn hình/database để hoàn thành profile, nhưng branch sẽ chạy trong demo phải có outcome/owner/expected result rõ. Tham chiếu DP-01–DP-07 trong [tài liệu tổng](T-024-demo-decision-policy.md) để không tạo danh sách quyết định thứ hai.
