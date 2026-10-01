# D-007 — Duyệt Group 4: workflow acceptance và AI/risk evaluation

- **Trạng thái:** Approved for demo profile — Group 4. Bốn group policy chính của T-024 đã chốt theo D-004–D-007; test profile cụ thể chưa freeze và test chưa chạy.
- **Ngày/người chốt:** 2026-10-01, Quốc An.
- **Nguồn:** xác nhận trực tiếp trong cuộc trò chuyện: “duyệt Group 4 theo hướng này”, kèm hai loại acceptance, attempt-level reporting, phạm vi replay/fixture và yêu cầu freeze trước kết quả. Không ghi nhận thêm phê duyệt của Minh Hy/thầy hoặc quy chế kỳ thi thật.

## Context → question → decision

[T-023](../../05-evaluation/T-023-encoder-evaluation-result.md) còn 8/38 hard negative accept trong controlled proxy. [D-004](T-024-D-004-duyet-default-demo.md), [D-005](T-024-D-005-auto-checkin-co-dieu-kien.md), [D-006](T-024-D-006-manual-authority.md) đã chốt defaults và authority, nhưng policy không tự sửa lỗi nhận dạng. Câu hỏi là: khi false-accept cap chưa được định nghĩa, test demo có thể kết luận điều gì?

**Quyết định:** Group 4 approves a frozen end-to-end demo evaluation with hard workflow invariants and full attempt-level AI error reporting. Workflow correctness has explicit pass/fail criteria. Because an acceptable false-accept risk cap has not been defined, AI identity risk is reported descriptively rather than declared acceptable/safe. Manual outcomes remain separate from AI success. The evaluation uses pre-frozen existing/replay inputs and simulated business cases and does not constitute evidence of real exam-door camera performance.

## A. Workflow acceptance — PASS/FAIL rõ

Các invariant dưới là bắt buộc trong những scenario được định nghĩa trước test. **Vi phạm bất kỳ invariant nào → workflow test FAIL.** Case chưa được thực thi ghi NOT_RUN, không tính là đã đạt. “Workflow PASS” là kết quả kiểm thử, khác outcome PASS/check-in của một attempt.

| ID | Invariant / expected behavior |
| --- | --- |
| WI-001 | Không có duplicate effective check-in; re-entry không tạo check-in/PASS thứ hai. |
| WI-002 | Không PASS khi business condition/exception chưa giải quyết; final-check dùng dữ liệu/policy còn hiệu lực. |
| WI-003 | Không PASS khi write chưa confirmed; reconcile trước lần ghi tiếp khi kết quả write chưa rõ. |
| WI-004 | Mọi capture chịu `max_capture_attempts=3` toàn attempt. |
| WI-005 | Retry/recovery đúng reason budget; recovery cùng input không tạo evidence mới hoặc mở thêm capture. |
| WI-006 | Nhập lại cùng SBD/resume/reconnect active attempt không reset counters. |
| WI-007 | Actor chỉ thực hiện hành động trong quyền/scope; manual identity đủ quyền + approved evidence method + scope phòng/ca. |
| WI-008 | MANUAL/HUMAN không sửa verdict/score/history AI và không được tính thành AI success. |
| WI-009 | SYSTEM_HOLD, duplicate, re-entry, eligibility blocked và ngoại lệ đi đúng route đã duyệt; thiếu evidence/quyền không tự thành success. |
| WI-010 | `auto_checkin_enabled=false` không tự PASS; chờ authorized confirmation, final recheck và write thành công. |
| WI-011 | Audit truy được attempt/capture, policy version, AIConfig version, actor/quyền/scope, reason và outcome; nhánh ghi/correction giữ liên kết trước/sau. |

WI-002 kiểm điều kiện nghiệp vụ và rule hiện hành; nếu AI trả ACCEPT sai theo ground truth nhưng business/final-check hợp lệ, đây là lỗi identity thuộc phần B, không tự đổi thành lỗi business flow. Nếu cả hai loại lỗi xảy ra thì báo cả hai.

## B. AI/risk evaluation — mô tả số liệu, chưa có safety PASS/FAIL

**False-accept cap = TBD:** test vẫn chạy được. Chỉ được kết luận workflow đạt/không đạt và mức lỗi quan sát được; chưa được kết luận AI đạt mức rủi ro chấp nhận được, đủ an toàn, deployment-ready hoặc đạt false-accept requirement.

- **Genuine:** accept, not verified, unresolved; lưu đường đi S4/S8 và outcome cuối.
- **Non-target/impostor/hard-negative có nhãn đáng tin:** rejected/no-select, false-selected, S8 accepted, effective false check-in. Giữ riêng các tầng, không gộp no-select với S8 reject hoặc S4 wrong selection với S8 false accept.
- **Operational:** retries, manual, system hold và runtime nếu được đo; báo attempt, capture và unique source/identity counts riêng.
- **Attempt-level:** một attempt có capture impostor bị S8 ACCEPT thì ghi một attempt có AI false acceptance, dù các capture trước bị reject. Chỉ khi check-in sai được ghi confirmed mới thêm effective false check-in; business có thể chặn ghi mà không xóa lỗi S8. Dùng mẫu số đúng nhóm/điều kiện, không trung bình frame rejection để che attempt acceptance.
- **HUMAN:** giữ nguồn quyết định và verdict AI riêng, không dùng manual approval sửa ground truth hoặc làm đẹp số AI. Fixture giả lập AI verdict phục vụ workflow không nằm trong mẫu số đo chất lượng nhận dạng.

Giữ trace từng failure: `S4 wrong selection → S8 false accept → final business-check OK → auto-check-in → write confirmed → effective false check-in`. Nếu bị chặn, ghi stage/reason đã chặn. Ground truth không đủ thì AMBIGUOUS/không chấm identity, vẫn báo coverage và lý do; không tự gán background thành impostor.

## Freeze → test → kết luận → version tiếp theo

Phạm vi được duyệt: **existing data + replay/fixture + simulated business states**; không thu ảnh/video mới. Freeze trước test: dataset/input manifest, ground truth, ExamPolicy/retry budget, AIConfig/model/hash/detector, S4 parameters, S8 operating point, auto-check-in mode, scenario list/expected results, metrics/mẫu số, exclusions, acceptance rules và code/runtime version.

Sau khi xem kết quả, thay threshold/retry/policy/input/rule tạo **config/version mới và một evaluation độc lập khác**; không gọi là cùng evaluation hoặc thay kết quả cũ. Không dùng evaluation để tune. Replay dữ liệu đã xem phải ghi là replay/integration evidence, không là holdout chưa từng xem hay hiệu năng camera cửa phòng thi thật.

Có false acceptance không tự đồng nghĩa workflow fail hoặc đồ án fail; phải báo đúng lỗi và phạm vi. Ví dụ kết luận được phép: workflow đạt các scenario đã chạy; AI false acceptance X/Y, effective false check-in Z/Y, retry/manual rate có mẫu số rõ. Không biến việc chưa có cap thành tuyên bố đã đạt cap.

**Bước tiếp tồn tại vì:** policy/rules đã chốt, nhưng cần bind thành input/config/scenario/expected result cụ thể để test có thể tái lập. [Bản chuẩn bị test profile](../../01-problem/T-024-test-profile-preparation.md) ghi phần đề xuất và các binding cần khóa; D-007 không tự duyệt một ngưỡng demo số hoặc tuyên bố test đã chạy.
