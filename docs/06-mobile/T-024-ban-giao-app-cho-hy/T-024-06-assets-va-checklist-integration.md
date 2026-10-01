# T-024 — 06. Assets, dữ liệu demo và checklist integration

## 1. Hy nhận gì và còn cần gì?

| Thành phần | Trong Git / cách nhận | Trạng thái |
| --- | --- | --- |
| Bộ MD bàn giao, policy/decision, report, script | Folder này và các link trong file 05. | Có trong branch/PR #19. |
| buffalo_sc + hai ONNX | Nguồn tác giả hoặc An trao riêng; kiểm hash ở file 05/A-002. | Chưa xác nhận gửi/nhận. |
| XQLFW/BFW, ảnh reference/scene, manifest identity, embedding, raw per-sample | Ngoài Git; [external-assets](../../00-project/external-assets.md) A-001/A-006/A-007. | Chỉ nhận khi cần audit/replay; không đính ảnh/identity vào PR. |
| Roster và reference mapping cho demo app | Hy dựng records giả, dùng nguồn ảnh sẵn có hợp lệ và liên kết ngoài Git. | Cần chuẩn bị; không coi benchmark là danh sách thí sinh thật. |
| App/AI adapter, API/build/package | Hy implement từ contract và code tham chiếu. | Bộ này chưa tạo module/service chạy sẵn. |

Không cần tải mọi dataset benchmark để xây app. Bắt đầu UI/business bằng mã/hồ sơ giả và AI fixtures ghi rõ nguồn; khi nối AI thật cần đúng weight và reference/observation phù hợp. T-024 không giao thu ảnh/video mới hoặc nhờ tình nguyện viên. Camera có thể được tích hợp như nguồn input của app; test được duyệt hiện tại vẫn existing/replay/fixture, chưa phải một đợt thu dữ liệu mới.

## 2. Dữ liệu nghiệp vụ tối thiểu

- **Context:** exam/session/room, intake lifecycle, mốc giờ và policy version.
- **Registration:** mã khai báo → hồ sơ duy nhất, assignment, eligibility/source version, reference asset/version.
- **Attempt:** claim/context, arrival time, status/flags/reasons, captures/recoveries/counters, output AI liên kết đúng observation.
- **Check-in:** effective record, nguồn AUTO/HUMAN, confirmed write, record gốc nếu duplicate/correction.
- **Authority/audit:** actor/role/delegation/scope, action/reason/evidence, thời gian, trước/sau, policy/data/AIConfig version.

Đây là business data needs, không chốt database schema/technology. Lưu ảnh/embedding chỉ khi có nhu cầu/quyền/retention rõ; không coi lưu toàn video là điều kiện audit mặc định.

## 3. Checklist build — làm tới đâu note tới đó

1. Có landing/input SBD và màn hình hồ sơ/context đã resolve; lookup mơ hồ route manual.
2. Có workflow outcomes, policy version và role scope; UI mock có nhãn FIXTURE, không báo AI accuracy.
3. Có nguồn observation + adapter load/hash guard; reference đúng record, detect/alignment/embedding nhất quán.
4. Có single-face dispatcher được ghi rõ và multi-face P2 giữ nguyên; S4 unresolved → S8 NOT_RUN.
5. Có S8 research config/version, score provenance; không gắn AI_VERIFIED thành PASS trực tiếp.
6. Có global/reason retry counters, resume không reset; recovery không thành evidence mới.
7. Có final business-check, auto true/false, confirmed write và duplicate protection.
8. Có manual/READY routing, authority checks, fallback/correction audit; HUMAN không sửa AI.
9. Chạy end-to-end ở chế độ development/replay; lưu cách chạy/build, input cần nhận, cấu hình và giới hạn trong task app.
10. App ổn rồi mới chốt [test-profile checklist](../../01-problem/T-024-test-profile-preparation.md), freeze trước test cuối và report.

Không tạo thêm task nghiên cứu threshold/model chỉ để hoàn tất checklist này. Nếu adapter chưa support một case, ghi chưa implement và route rõ; không bịa kết quả test hoặc đếm fixture là output model.

## 4. Kiểm cuối app theo D-007

**Workflow:** không duplicate effective check-in; không PASS khi business unresolved/write unknown; không vượt 3 captures; retry/resume đúng; không vượt quyền; HUMAN giữ AI history; auto flag false không tự PASS; audit truy được phiên bản/actor/reason/outcome. Vi phạm mandatory invariant → workflow FAIL trong các case đã test.

**AI/risk:** báo attempt-level genuine accept/not verified/unresolved, S4 no-select/false-select, S8 accept/reject trên candidate sai, effective false check-in, retry/manual/hold. Một non-target được accept ở bất kỳ capture nào thì attempt có AI false acceptance; confirmed wrong write là lỗi effective check-in riêng. Human check-in và fixtures không tính thành AI success.

Cap false accept vẫn TBD nên chỉ kết luận workflow đạt/không đạt và observed errors trong phạm vi test; chưa kết luận AI safe/deployment-ready. Replay đã xem không là holdout mới. Freeze input/GT/ExamPolicy/retry/AIConfig/model/P2/S8/auto mode/cases/metrics/exclusions/acceptance/code trước test cuối; chỉnh sau kết quả phải là version/evaluation khác.

## 5. Những quyết định nhỏ còn cần cho app

Hy ghi nơi chạy AI và stack, account/delegation, manual evidence method, demo roster/reference source, nguồn clock/early window, timeout/retention, criteria quality thực sự có và single-face dispatch. Những thứ này không cần kéo dài thành một phase discovery mới; chọn và note trong lúc build. Nhánh có TBD chưa resolve không tự auto-approve. Trước test cuối, chỉ khóa những binding thuộc scope test và báo rõ nhánh chưa làm.
