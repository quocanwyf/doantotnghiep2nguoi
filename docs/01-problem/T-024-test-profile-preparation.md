# T-024 — Chuẩn bị test profile sau khi chốt policy

**Trạng thái:** DRAFT cho bước freeze kế tiếp, chưa là evaluation freeze và chưa có kết quả test. **Ngày:** 2026-10-01. **Owner:** Quốc An theo task T-024. [D-007](../00-project/decisions/T-024-D-007-workflow-va-risk-evaluation.md) đã chốt cách acceptance; các đề xuất input/operating point dưới đây cần được khóa cụ thể trước chạy.

## 1. Hai loại đầu vào và phạm vi kết luận

1. **Workflow fixtures:** business states, quyền actor, lỗi write và chuỗi output AI được giả lập, khai báo trước. Dùng để kiểm WI-001–WI-011; không tính verdict giả lập vào FMR/FNMR/AI accuracy.
2. **AI-output replay:** đề xuất dùng toàn bộ scene usable của [T-023 đã freeze](../05-evaluation/T-023-evaluation-freeze.md), nối output S4/S8 với business states giả lập và workflow runner. Đầu vào cũ đã được xem; đây là kiểm tích hợp/replay, không phải một holdout mới để đánh giá encoder hoặc tune. Có thể kiểm lại inference khi đã bind model/input/code, nhưng phải ghi recompute hay reuse, không thay reference/crop/score âm thầm.

T-023 có 60 target-present, 238 target-absent usable và 2 absent AMBIGUOUS ở evaluation; đây là **số nguồn**, chưa là mẫu số test mới. Proposed replay giữ toàn bộ usable, không chỉ 8 hard-negative accept hoặc các case dễ. AMBIGUOUS giữ riêng, không ép identity label. Không tạo video/capture mới hoặc gọi ảnh lặp là evidence độc lập.

## 2. Config/input cần khóa

| Thành phần | Đề xuất / binding trước test | Trạng thái |
| --- | --- | --- |
| ExamPolicy | D-004–D-007; late 15 phút khi intake mở, retry budgets đã duyệt, authority ba tầng. Cụ thể hóa fixture context/roster/reference/clock và delegation. | Policy approved; fixture/version/hash chưa khóa. |
| AIConfig | Baseline nghiên cứu hiện tại theo T-023: model pack `buffalo_sc`, MobileFaceNet và detector/config đã freeze ở nguồn. | Chưa freeze bản test này; phải kiểm hash/version thực tế. |
| S4/P2 | Kế thừa `τ=0.14789717107158995`, `δ=0.07647264965285691` từ freeze T-023, không retune. | Proposed inheritance; cần ghi trong freeze record. |
| S8 operating point | **Đề xuất `θ=0.23` làm research/reference point của replay**, vì đã có rule/evidence T-023; không chọn lại bằng output test và không gọi deployment threshold. S8 hiện vẫn reuse cùng cosine selected box. | Proposed, chưa duyệt/freeze operating point cho test này. |
| Auto-check-in | Hai config được khai báo trước: true cho luồng demo thường; false để kiểm READY_FOR_CONFIRMATION. | Mode capability approved; mỗi case phải chỉ rõ mode/version. |
| Input/ground truth | Scene IDs, identity labels/mapping, raw S4/S8 output và hash từ nguồn; dựng attempt manifest liên kết capture sequence, business states và expected workflow outcome. | Chưa có manifest test mới; cần audit/khóa trước chạy. |
| Workflow runner | Mã/version thực thi decision/retry/write/audit, simulated actor/evidence fixtures và runtime/device. | Cần bind; tài liệu này chưa chứng minh runner đã triển khai. |
| Auxiliary capability | Early window, quality/temporal, timeout/retention và retry phụ chỉ đưa vào scope nếu đã bind rule/capability phù hợp. | Chưa tự duyệt giá trị TBD hoặc coi capability đã có. |

Hash nguồn tham chiếu nằm ở freeze T-023; freeze test mới phải kiểm và lưu hash input/GT/config/code thực sự dùng. Không ghi giá trị placeholder như một hash đã xác minh.

## 3. Scenario / expected result trước test

Bảng này là **đề xuất case list để hiện thực hóa và freeze**. Case parameters, sequence, actor, fixture/replay IDs phải được ghi trong manifest; chưa đủ binding → NOT_RUN, không báo workflow đạt toàn bộ.

| Case | Input/condition cần dựng trước | Expected workflow / invariant |
| --- | --- | --- |
| TC-001 | Business OK, AI_VERIFIED, auto=true, write confirmed. | Một effective check-in/PASS; WI-001/002/003/011. |
| TC-002 | Cùng điều kiện, auto=false, chưa có confirmation. | READY_FOR_CONFIRMATION, không effective check-in; WI-010/011. |
| TC-003 | READY được actor có quyền confirm; business còn hiệu lực. | Recheck rồi confirmed write mới PASS; WI-002/003/007/010. |
| TC-004 | Business/policy/roster đổi hoặc exception phát sinh trước write. | Final-check chặn ghi, route đúng; không PASS từ evidence cũ; WI-002/009/011. |
| TC-005 | Write timeout/unknown rồi resume/reconcile. | SYSTEM_HOLD; không PASS sớm, không ghi trùng; WI-001/003/009. |
| TC-006 | Đã tiêu budget; nhập lại cùng SBD/resume/reconnect. | Giữ active attempt/counters, không có retry mới do reset; WI-004/005/006. |
| TC-007 | No-face lặp; hoặc no-face → poor-quality → S4 unresolved. | Tối đa 3 capture toàn attempt; hết budget → MANUAL, không cộng reason budgets; WI-004/005. |
| TC-008 | Processing lỗi trên capture 3; recovery cùng input; recovery budget cạn. | Chỉ phục hồi trong budget/input còn hợp lệ; không capture 4/đổi verdict cũ; WI-004/005/011. |
| TC-009 | S8 NOT_VERIFIED → một capture bổ sung → vẫn NOT_VERIFIED. | MANUAL sau reason budget; không dùng global cap để cấp thêm S8 retry; WI-005/009. |
| TC-010 | Operator cố confirm identity/late/re-entry/correction. | Hành động không được thực hiện, route người có quyền; WI-007/009. |
| TC-011 | Manual identity thiếu quyền, thiếu approved method hoặc ngoài scope; kiểm từng biến thể. | ESCALATE/pending, không manual-approved check-in; WI-007/009. |
| TC-012 | S8 NOT_VERIFIED; HUMAN đủ guard/evidence; business hợp lệ. | Manual-approved check-in sau write; giữ raw AI verdict, nguồn HUMAN; WI-003/007/008/011. |
| TC-013 | Late ≤15 phút/intake mở; >15 phút/intake mở có/không delegation; intake đã đóng. | Trong giới hạn tiếp tục; quá giới hạn đúng room staff/Admin; closed không mở bằng late authority; WI-002/007/009. |
| TC-014 | Duplicate/re-entry; giữ check-in cũ. | MANUAL/re-entry đúng quyền, không PASS/check-in thứ hai; correction vượt room scope sang Admin; WI-001/007/009. |
| TC-015 | Eligibility blocked, wrong room/session hoặc hồ sơ chưa resolve. | Đúng CHECK_IN_NOT_ALLOWED/REDIRECT/MANUAL theo case; AI accept không bỏ qua business; WI-002/009. |
| TC-016 | Policy/roster unreliable hoặc reference mapping conflict; fallback rồi reconcile. | Hold/route Admin, biên nhận tạm không tự effective PASS; WI-002/003/007/009/011. |
| TC-017 | Fixture S4 chọn non-target, S8 accept, business OK, auto=true, write confirmed. | Workflow theo rule tạo check-in; flag identity error và effective false check-in **giả lập**, không giấu bằng manual hoặc gọi workflow fail chỉ vì model verdict giả lập sai. WI-008/011; không vào mẫu số AI. |
| TC-018 | AI-output replay có source GT đã khóa; cùng inputs/rules cho mọi usable scene. | Báo từng stage/attempt và điểm business chặn/cho ghi; quality nhận dạng lấy từ output thật, không đặt trước “AI phải đúng”. |

TC-007–009 là kiểm ngân sách bằng fixture, không phải video temporal đã kiểm. Ví dụ chuỗi ba capture ending accept phải hợp lệ với từng reason budget; ba lần S8 NOT_VERIFIED liên tiếp không được cấp ba cơ hội chỉ vì global cap bằng 3.

## 4. Mẫu số và báo cáo attempt-level

- Workflow: tổng case/biến thể đã freeze, PASS/FAIL/NOT_RUN; bất kỳ mandatory invariant vi phạm → workflow FAIL. Không suy “mọi case đã đạt” từ một case happy path.
- Genuine/reference-target: accept, not verified, unresolved; tách S4 đúng/sai/unresolved và candidate-pair GT. Target có trong scene không chứng minh selected box là genuine.
- Target-absent/non-target: no-select, false-selected, S8 reject/accept và effective false check-in; giữ cả mẫu số toàn attempt và subset tới S8/hard negatives.
- Mỗi attempt lưu `any_impostor_s8_accept` và `effective_false_checkin` riêng. Có S8 false accept nhưng business chặn ghi thì vẫn báo lỗi S8; write confirmed sai mới tính effective false check-in proxy.
- Retry/manual/hold: số attempt từng đi qua nhánh và outcome cuối; các cột “ever visited” có thể overlap, không cộng như nhóm terminal độc lập. Báo capture/recovery counts, unique source/identity counts và runtime measured/replayed tách riêng.
- Mỗi AI false acceptance được tính một lần ở attempt, kể cả trước đó reject; không lấy tỷ lệ frame reject để thay attempt error. Ảnh lặp hoặc output replay không tạo quan sát danh tính độc lập.
- Pair FMR/FNMR nếu báo thêm phải có mẫu số pair riêng, không thay denominator bằng số scene/attempt. Manual decisions, fixtures và AMBIGUOUS không trộn vào metric AI có GT.

## 5. Freeze record và raw trace bắt buộc

Trước run: khóa hash/version của manifest/GT/exclusions, ExamPolicy/retry, AIConfig/model/detector/P2/S8/auto mode, scenario/expected results, metric/acceptance và code/runtime. Attempt manifest định nghĩa input sequence, cách dừng khi terminal, claim/reference, simulated business state và nguồn fixture/replay; không tạo sequence bằng cách chọn score sau khi chạy.

Raw trace phải nối `attempt_id → capture_index/source_sample → S4 selected/GT → S8 score/verdict/rule → final business-check → actor/decision source → write status/effective record → audit`. File có identity/ảnh/embedding/raw nhạy cảm giữ ngoài Git theo [external-assets](../00-project/external-assets.md); báo cáo Git chỉ dùng ID ẩn danh và aggregate phù hợp.

Sau freeze mới chạy test. Thay code/config/input sau kết quả tạo version/evaluation độc lập khác, giữ kết quả cũ; không tune trên test này. Kết luận: workflow đạt/không đạt trong scope đã chạy + observed AI/pipeline errors với mẫu số; cap TBD nên chưa kết luận AI safe hoặc deployment-ready.
