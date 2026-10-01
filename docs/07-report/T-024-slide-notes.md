# T-024 — Ghi chú báo cáo 10–12 phút

16 slide chính, 2 phụ lục. Tổng thời gian dự kiến: 705 giây. Notes dưới đây cũng được nhúng vào PowerPoint. Nội dung là gợi ý lời nói, không cần đọc nguyên văn.

## Slide 1 — Từ bài toán cửa phòng thi đến cải thiện S4 và S8

Thời gian dự kiến: 25 giây.

Tụi em bắt đầu từ bài toán kiểm tra thí sinh tại cửa phòng thi. Sau khi khảo sát và chạy baseline, tụi em phân tích lỗi để nghiên cứu hai cải thiện: chọn đúng target trong cảnh nhiều mặt và ra quyết định verification. Báo cáo hôm nay tập trung mạch nghiên cứu, số liệu và giới hạn; chưa tuyên bố đã triển khai an toàn ở kỳ thi thật.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/07-report/T-024-research-logic.md

## Slide 2 — Thiết bị ở cửa phục vụ vấn đề gì?

Thời gian dự kiến: 40 giây.

Ở cửa phòng cần đối chiếu người đến với hồ sơ, ca và phòng rồi ghi nhận. Thiết bị tại đây giúp tổ chức một lượt tương tác có context rõ và hỗ trợ giảm thao tác thường lệ. Đây là mục tiêu đề tài, chưa phải mức giảm nhân sự đã đo. Nhóm thống nhất đề xuất T-002 qua D-001; không chọn AI rồi mới tìm bài toán.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md

## Slide 3 — Khai SBD không đồng nghĩa xác minh danh tính

Thời gian dự kiến: 40 giây.

SBD chỉ giúp chọn hồ sơ/reference cần kiểm; không tự chứng minh danh tính. Bài toán AI là so candidate với reference đã khai theo 1:1, không phân loại toàn bộ sinh viên. Một attempt có thể có nhiều capture. Check-in không đồng nghĩa đã vào phòng hay đã dự thi. Human decision được lưu riêng, không sửa verdict AI.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/01-problem/T-008-requirements.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/00-project/decisions/T-008-D-003-chap-nhan-baseline-nghien-cuu.md

## Slide 4 — Pipeline: model chỉ nằm ở capability cần model

Thời gian dự kiến: 55 giây.

Đây là luồng thực thi với P2: lookup và business pre-check, capture ảnh, detector xuất bbox/landmarks, align và encode các mặt, rồi tính cosine với reference. S4 dùng score và margin để chọn; S8 áp rule verification cho selected score; app còn phải final business-check và confirmed write. P2 cần embedding trước selection; các ID stage là phân rã chức năng, không phải thứ tự số bắt buộc. Quality/PAD chưa được coi là đã triển khai đầy đủ.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/02-survey/T-005-quoc-an-task-decomposition.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/03-baseline/T-012-B0-pipeline-choice.md

## Slide 5 — Dataset được gắn đúng câu hỏi cần đo

Thời gian dự kiến: 40 giây.

Tụi em gắn dataset với từng câu hỏi: WIDER cho detection; XQLFW cho pair verification và target pilot/holdout có audit; BFW known identities để dựng controlled hard-negative proxy. Không dataset nào chứng minh toàn bộ check-in. Claim được mô phỏng bằng reference input. Nguồn và quyền dùng được ghi riêng; ảnh mặt và weights không đưa vào Git.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/02-survey/T-009-source-register.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/00-project/external-assets.md

## Slide 6 — Chọn baseline vừa đủ, rồi chạy trước khi tối ưu

Thời gian dự kiến: 40 giây.

B0 dùng SCRFD 500MF có landmarks phù hợp alignment và MobileFaceNet nhẹ; R50 làm reference mạnh hơn nhưng cost cao hơn. Project AP detection cao nhất không tự động chọn cấu hình toàn pipeline tốt nhất. Nhóm giữ một baseline ổn định để xem lỗi trước khi cải thiện. Không train/fine-tune model mới.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/03-baseline/T-012-B0-pipeline-choice.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/03-baseline/T-010-protocol.md

## Slide 7 — B0 chạy được, nhưng coverage còn thiếu

Thời gian dự kiến: 45 giây.

Trên 6.000 XQLFW pairs, B0 chấm được 4.215 và unresolved 1.785. FNMR 125/2.046 và FMR 133/2.169 chỉ tính trên valid pairs. Trong image audit, 908 ảnh có nhiều detections chưa chắc đều là nhiều người. Nhánh unresolved multi-face tạo câu hỏi S4: đã khai A, có chọn đúng A và không chọn khi A absent không?

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/03-baseline/T-012-B0-freeze-and-stage-diagnosis.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/03-baseline/T-011-baseline-summary.md

## Slide 8 — S4: từ unresolved sang selective selection

Thời gian dự kiến: 45 giây.

B0 multi-face luôn unresolved. P1 luôn chọn score cao nhất. P2 chỉ chọn khi top score và margin cùng vượt ngưỡng. Hai biến được tìm trên development qua 6.561 tổ hợp theo rule đặt trước. T-015 có sai khác labeling nên T-017 dùng clean confirmation: ghi target point trên ảnh gốc trước bbox mapping, không lấy score P1/P2 để sửa ground truth. Self-confirm vẫn là limitation, không có reviewer độc lập.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/04-optimization/T-014-method-protocol.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-017-clean-confirmation.md

## Slide 9 — S4 target-present: P2 phục hồi 46/49 lượt

Thời gian dự kiến: 40 giây.

Trên cùng 49 target-present proxy trials của T-017, B0 unresolved toàn bộ; P1 chọn đúng 49; P2 chọn đúng 46 và unresolved 3, không wrong selection. P2 phục hồi 93,9% số present trong benchmark này. Đây là selection result, chưa phải verification accept hay check-in success.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-017-clean-confirmation.md

## Slide 10 — S4 target-absent: P1 ép chọn, P2 biết abstain

Thời gian dự kiến: 40 giây.

Trên 41 target-absent trials, B0 không chọn 41; P1 ép chọn sai cả 41; P2 không chọn 39 nhưng vẫn chọn sai 2. Selective S4 đem lại utility cho present và giảm lỗi so với forced selection, nhưng còn trade-off. Không gọi 2/41 là FAR. Từ hai false selections này, câu hỏi tiếp là S8 có chặn được không?

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-017-clean-confirmation.md

## Slide 11 — T-020: S8 chưa tạo barrier sau S4

Thời gian dự kiến: 50 giây.

T-020 replay selected-box cosine đã khóa của T-017, không recompute crop/reference mới. P2 yêu cầu score ít nhất 0,147897, nhưng S8 lịch sử accept từ 0,122254. Vì vậy cả hai selected non-target đều accept: holdout-010 score 0,238723 và holdout-018 score 0,156472. Không có nhãn chắc để gán một identity B cụ thể cho background, và chưa biết vì sao score cao. Hai threshold không tự tạo hai signal độc lập. Điều này dẫn sang T-021 về risk và separation.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-020-s4-s8-integration.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-021-s8-risk-protocol.md

## Slide 12 — S8: khóa GT, split và rule trước evaluation

Thời gian dự kiến: 50 giây.

T-021 tách genuine, ordinary impostor và S4-derived hard negative. Ground truth phải có trước score; hard-negative subset chỉ gồm non-target được P2 chọn trên scene absent đã khóa nhãn. T-022 evaluation không có hard negative được chọn nên không đo được khả năng chặn nhóm này. T-023 dùng BFW holdout độc lập. Rule development trên grid 0,01 giữ selected-genuine accept ít nhất 95%, giảm hard accept và tie-break đã định trước; chọn 0,23 rồi freeze. Business risk cap vẫn TBD, không gọi đây là deployment optimum.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-022-s8-evaluation-result.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/04-optimization/T-023-encoder-assessment-protocol.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-023-development-analysis.md

## Slide 13 — S8: chặn thêm hard negatives, có trade-off

Thời gian dự kiến: 55 giây.

Trên T-023 frozen holdout, tại 0,23 S8 accept 55/55 selected genuine, reject 30/38 hard negatives và còn accept 8. So mốc 0,15, giảm hard accept từ 36 xuống 8 nhưng all-genuine reject tăng 14 lên 21/240. Ordinary FMR là 1/240. Selected genuine là subset có điều kiện, nên 55/55 không có nghĩa FNMR toàn genuine bằng 0. Điểm 0,25 là stress point đã công bố, không chọn lại từ evaluation.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-023-encoder-evaluation-result.md

## Slide 14 — Kết hợp S4 → S8: so cùng 238 absent scenes

Thời gian dự kiến: 50 giây.

Giữ P2 và toàn bộ 238 absent scenes T-023 fixed: tại 0,15 có 200 no-select, 2 selected rồi reject, 36 selected rồi accept. Tại 0,23 vẫn 200 no-select, nhưng 30 reject và 8 accept. Proxy absent acceptance giảm 36/238 xuống 8/238; present accept giữ 55/60, còn 5 unresolved. No-select không phải verification reject. Đây chưa phải effective false check-in của app và không ghép với tỷ lệ S4 XQLFW thành một accuracy tổng.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-023-encoder-evaluation-result.md

## Slide 15 — Đóng góp và kết luận đúng mức evidence

Thời gian dự kiến: 45 giây.

Hai cải thiện nằm ở selective selection và verification decision có protocol, không phải encoder mới. Evidence cho thấy MobileFaceNet có vùng phân tách hữu ích nhưng vẫn còn overlap và lỗi. Vì vậy nhóm giữ baseline, chưa có lý do buộc phải fine-tune. Synthetic data, self-confirm, pretraining overlap chưa audit toàn bộ và thiếu camera/thiết bị đích là các giới hạn. Chưa có một phép so full app B0 với full proposed trên cùng benchmark.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/DECISION_LOGIC.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/05-evaluation/T-023-encoder-evaluation-result.md

## Slide 16 — Bước tiếp theo: build app theo policy đã duyệt

Thời gian dự kiến: 45 giây.

T-024 đã duyệt default demo, auto-check-in có điều kiện, ba tầng authority và cách đánh giá workflow/risk. Mọi capture chịu global cap 3; HUMAN không sửa AI. Auto-PASS chỉ sau business pre/final checks, AI verified, không duplicate/unresolved và write confirmed. Hy build/integrate app trước, rồi mới freeze test profile và chạy test cuối. Workflow có pass/fail; AI báo attempt-level errors vì risk cap vẫn TBD. PASS chỉ là check-in confirmed.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/00-project/decisions/T-024-D-008-ban-giao-va-build-app.md
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/06-mobile/T-024-ban-giao-app-cho-hy/T-024-README.md

## Slide 17 — Nguồn để đối chiếu và viết báo cáo

Thời gian dự kiến: 0 giây.

Phụ lục này không cần đọc trong phần 10–12 phút. Master Markdown và notes từng slide có link nguồn; reports gốc giữ freeze/hash và raw-output reference. Deck không chứa ảnh mặt hay checkpoint. Dùng appendix để đối chiếu khi thầy hỏi protocol hoặc phạm vi kết luận.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/07-report/T-024-research-logic.md

## Slide 18 — Câu hỏi thầy có thể hỏi

Thời gian dự kiến: 0 giây.

Nếu thầy hỏi đóng góp: trả lời selection/decision/pipeline và phương pháp thí nghiệm, không claim train encoder. Threshold lấy từ development rule trước evaluation. S8 không có signal độc lập nhưng rule chặn được một phần lỗi. Có ba nhóm kết quả, chưa có full-app accuracy. Chưa gọi demo an toàn cho kỳ thi thật; cần final frozen integration test và risk requirement nếu triển khai.

Nguồn:
https://github.com/quocanwyf/doantotnghiep2nguoi/blob/codex/T-024-demo-policy/docs/07-report/T-024-research-logic.md
