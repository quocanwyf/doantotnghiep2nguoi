# T-010 — Khóa giao thức baseline trước khi chạy

**Ngày thiết kế:** 2026-09-26. **Người thực hiện:** Quốc An. **Trạng thái:** dự thảo để Minh Hy review; chưa khóa dữ liệu/tiêu chí chấp nhận, chưa chạy baseline, chưa xem kết quả so sánh và chưa chọn model cuối.

## 1. Mục tiêu và ranh giới

T-010 chuyển capability/rủi ro nghiệp vụ từ T-008 và các candidate đủ điều kiện từ T-009 thành một **protocol có thể chạy lại** cho T-011. Mục tiêu là khóa câu hỏi, dữ liệu, split, preprocessing, biến kiểm soát, metric, thiết bị và cách ghi nhận kết quả **trước khi xem benchmark**.

T-010 không chứng minh model nào tốt hơn, không tối ưu threshold trên test set, không tự đặt acceptance target chưa được nhóm chốt và không thay đổi yêu cầu nghiệp vụ để làm một candidate kỹ thuật trở nên phù hợp.

Đầu vào hiện tại:
- T-008 ở PR #3 vẫn đang được Minh Hy review; capability/TQ từ đó là baseline tạm thời và phải đối chiếu lại trước khi khóa protocol.
- T-009 ở PR #5 đã audit B0 một số dataset/weight; smoke runtime chỉ chứng minh khả dụng file/runtime, không phải accuracy.

### Trace từ nghiệp vụ tới phép thử

[T-008 PR #3](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/3) còn là bản chờ review; ID dưới đây là **mapping tạm thời**. T-008 nêu capability xác minh người đang làm thủ tục, không tự quy định phải dùng thị giác máy tính. E1/E2 xuất hiện vì [D-001](../00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md) và [T-007](../02-survey/T-007-selection.md) chọn hướng khảo sát 1:1 của T-005. Nếu capability T-008 đổi sau review, mapping và phép thử tương ứng phải được xem lại.

| Nhánh | Nguồn nghiệp vụ ở T-008 dự thảo | Uncertainty từ T-005/T-009 | Bằng chứng T-011 được phép tạo |
|---|---|---|---|
| E1 detection | TQ-002, FR-006; RISK-001/002 | S3: các detector có bbox/landmark và runtime khác nhau; S4 chưa có nhãn target | Chất lượng phát hiện trên ảnh nguyên khung và chi phí component; không kết luận chọn đúng người |
| E2 verification | TQ-002/003, FR-006/009; RISK-001/002 | S7–S8: score genuine/impostor, ảnh kém, preprocessing/weight khác nhau | FMR/FNMR và vùng không chắc trên protocol có nhãn; không suy thành quyền cho vào |
| E3 workflow fixture | TQ-001, TQ-003–007; FR-001–018; RISK-003–005/007–009 | Policy/authority, lượt trùng, fallback, attendance và correction chưa có bằng chứng software | Pass/fail theo invariant và profile giả lập được duyệt; không là accuracy thị giác |
| M1 vận hành | TQ-008, FR-019, NFR-001/002; RISK-006/007 | Chưa biết tải đến, thời gian review và thiết bị đích | Thời gian component/attempt theo điều kiện đo; chỉ đo hàng chờ hoặc giảm công nếu có baseline thực địa |

Một kết quả chỉ trả lời nhánh và đơn vị đo đã ghi. Không cộng AP detection, FMR verification và số case fixture đạt thành một điểm “accuracy hệ thống”.

## 2. Câu hỏi thí nghiệm

### E1 — Detection component
**Câu hỏi / giả thuyết:** trên cùng ảnh nguyên khung và thiết bị, ba detector có đánh đổi chất lượng–chi phí khác nhau; chưa giả định ứng viên nào thắng. So YuNet, BlazeFace full-range và SCRFD-500MF để kiểm chứng.

- **Biến thay đổi:** detector candidate.
- **Giữ cố định:** frame/split, annotation chuẩn, thiết bị, warm-up, số lần lặp, phạm vi latency và quy tắc match prediction–ground truth. Resize/preprocessing đúng mỗi detector phải pin; mọi biến thể resize chung là phép thử riêng.
- **Metric:** metric chuẩn của dataset khi phù hợp (ví dụ precision/recall/AP), error slices nếu nhãn cho phép, latency và resource.
- **Đơn vị:** frame ảnh nguyên khung; đánh giá theo bbox ground truth và quy tắc match/ignore của tập đã chọn. Nếu tập chỉ có bbox, không báo landmark accuracy.
- **Giới hạn:** kết quả E1 không tự chứng minh end-to-end verification hoặc target selection S4. Ba detector chỉ được so sau khi cùng xử lý được một manifest ảnh, tọa độ/resize được quy về cùng hệ tọa độ và output hợp lệ trên ảnh thật (không chỉ blank-frame smoke).

### E2 — 1:1 face verification
**Câu hỏi / giả thuyết:** với cùng cặp reference/probe và split hợp lệ, các encoder đủ điều kiện có thể khác nhau về tách genuine/impostor và chi phí; chưa giả định encoder nào thắng.

Pool ban đầu:
- MobileFaceNet từ `buffalo_sc`: đã qua file/runtime gate ở T-009.
- EdgeFace XS, AdaFace R18, R50: chỉ được đưa vào run nếu hoàn tất weight/runtime/preprocessing gate trước khi freeze.

- **Biến thay đổi:** encoder/weight candidate.
- **Giữ cố định:** reference/probe protocol, split, thiết bị và procedure đo.
- **Preprocessing:** mỗi candidate dùng alignment/color/normalization đúng implementation/weight đã pin; không ép một crop tùy tiện cho mọi model.
- **Metric:** ROC, FMR/FNMR theo threshold, TAR tại các FMR được protocol cho phép báo cáo, EER khi phù hợp.
- **Quy tắc threshold:** chọn/tune trên dev; test chỉ dùng để đánh giá sau khi config và operating point đã khóa. Ghi số genuine/impostor attempts, số identity, khoảng tin cậy và phạm vi FMR dữ liệu có thể ước lượng; không nội suy operating point cực thấp từ vài nghìn cặp.
- **Điều kiện so sánh:** hiện chỉ MobileFaceNet vượt runtime smoke T-009; một encoder không tạo được kết luận A tốt hơn B. EdgeFace/AdaFace/R50 phải có weight ID, quyền, checksum, chạy ảnh hợp lệ và preprocessing được pin trước khi vào cùng protocol. Mỗi encoder phải công bố crop/align riêng; nếu khác nhau, kết quả bao gồm ảnh hưởng preprocessing và không quy toàn bộ chênh lệch cho backbone.

### E3 — Uncertain / retry / manual-review behavior
**Câu hỏi / giả thuyết:** với một policy profile được duyệt, workflow có giữ đúng invariant và chuyển tới người có quyền khi bằng chứng thiếu/không chắc không? Fixture phải có khả năng bác bỏ giả thuyết bằng expected outcome.

Đây là test logic/policy bằng fixture, không phải benchmark model. Case tối thiểu:
- không thấy mặt;
- nhiều mặt nhưng chưa xác định được target;
- bằng chứng xác minh chưa đủ để kết luận theo profile thử (nếu có vùng uncertain thì dùng vùng đó);
- record/ca/phòng không khớp;
- yêu cầu thử lại khi RetryPolicy không còn cho phép tiếp tục hoặc chưa được cấu hình;
- chuyển manual review;
- authority xác nhận/từ chối theo T-008.

Mỗi fixture phải nêu policy profile, trạng thái trước, attempt mới, actor/quyền, expected state sau, audit event và ID SC/BR/FR/TQ. Tách bốn kết quả: **attempt**, **check-in hiệu lực**, **entry authorization** (nếu trong scope) và **attendance sau đối soát**. Situation flag như late/wrong-room không thay lifecycle state; override và correction là hai hành động khác. Giá trị policy theo kỳ thi và quyền cụ thể còn TBD; fixture chỉ dùng profile giả lập đã được nhóm duyệt, không tạo quy chế thi mặc định.

Kết quả E3 là expected state/outcome pass/fail, không phải face-recognition accuracy. Test fixture có thể thiết kế trước khi có dữ liệu ảnh; pass/fail chỉ được báo khi có implementation thực để chạy.

### M1 — Đo vận hành theo đúng phạm vi

Ghi riêng thời gian xử lý tự động mỗi attempt, thời gian chờ để có ảnh dùng được, số retry và thời gian chờ/xử lý của nhánh manual nếu thật sự quan sát được. E1/E2 có latency component; phép đo attempt cần cùng điểm bắt đầu/kết thúc và gồm cả preprocessing, inference, hậu xử lý, lookup và ghi nhận khi các phần đó đã tồn tại. Chưa có profile lượng đến và As-Is của một kỳ thi cụ thể nên **không thể** suy số người giảm, độ dài hàng chờ thực tế hoặc throughput giờ cao điểm chỉ từ model latency. Thiết bị đích chưa chốt: mọi số đo trên PC phải ghi là proxy.

## 3. Data gate trước khi khóa dataset

Không dataset nào được gọi là `main test`, `dev` hay `external` cho đến khi:
1. file ảnh/annotation thực tải và parse được;
2. quyền/điều kiện sử dụng của ảnh, annotation và protocol được ghi rõ;
3. schema nhãn đáp ứng đúng câu hỏi thí nghiệm;
4. manifest có identity/session/frame information đủ để kiểm leakage;
5. protocol pairs/path thực sự trỏ tới file tồn tại;
6. artifact có version/checksum;
7. domain gap và capability không đo được được ghi rõ.

Candidate từ T-009:
- detection: ưu tiên kiểm WIDER FACE; FDDB là external/dự phòng nếu cần và phải có quy tắc ellipse riêng;
- verification: XQLFW có file pairs đã kiểm, nhưng archive ảnh/path/rights chưa đủ để khóa làm main test;
- external portal/video: ChokePoint chỉ dùng nếu archive/rights/label mapping được xác minh;
- LFW chỉ smoke/reference, không dùng làm bằng chứng triển khai cửa phòng thi.

### Kết quả kiểm thêm XQLFW trong T-010 (2026-09-26)

[Trang tải của tác giả](https://martlgap.github.io/xqlfw/pages/download.html) công bố archive và protocol; [repo tác giả](https://github.com/Martlgap/xqlfw) tách phần mã đánh giá. Archive xqlfw.zip tải vào thư mục tạm **ngoài Git**: 195.229.543 byte, SHA-256 1AF459679FBA23A12F4D83C82A81523EB930A4AEC759EEBEFCBDDE69A678962C. Kiểm ZIP CRC không thấy lỗi; có 13.233 ảnh JPG trong 5.749 thư mục identity. File pairs đã được T-009 pin hash; 6.000 dòng tham chiếu 7.263 ảnh khác nhau và **không thiếu path** khi đối chiếu với archive. Không trích xuất hay commit ảnh/định danh.

Header protocol là 10 fold × 300 genuine + 300 impostor. Kiểm trực tiếp cho thấy mọi cặp fold đều có ít nhất một identity trùng (45/45 cặp fold). Vì vậy protocol chính thức có thể dùng như **benchmark cặp ảnh** theo fold, nhưng không được gọi là dev/test identity-disjoint. Nếu muốn đánh giá unseen identity, phải thiết kế manifest **mới** theo identity, bỏ cặp bắc qua split, báo số cặp/identity còn lại và không gọi kết quả đó là protocol XQLFW chính thức. Hai cách đánh giá không được trộn khi chọn threshold hoặc diễn giải kết quả.

Tác giả cho tải dữ liệu công khai, nhưng archive chỉ có ảnh JPG; [MIT của repo mã](https://github.com/Martlgap/xqlfw/blob/main/LICENSE) không tự xác nhận quyền sử dụng ảnh gốc/ảnh dẫn xuất LFW cho toàn bộ mục đích. Do quyền ảnh chưa được ghi rõ ở mức cần cho đồ án và domain ảnh web/crop khác camera phòng thi, **XQLFW vẫn chưa vượt toàn bộ data gate** và chưa được chọn làm main test. Cần ghi phạm vi sử dụng được xác nhận trước khi chạy; nếu không xác nhận được, chọn nguồn khác và ghi lý do.

| Vai trò cần khóa | Candidate hiện có | Bằng chứng đã có | Thiếu trước freeze | Trạng thái |
|---|---|---|---|---|
| E1 dev/test detection | WIDER FACE từ T-009 | Nguồn và schema công bố | Archive ảnh/nhãn, quyền, manifest/split, cách chấm | Chưa chọn |
| E2 main verification | Chưa chọn | XQLFW đã kiểm pairs + archive nhưng là tập stress khác miền | Quyền ảnh, protocol đúng mục tiêu unseen identity hoặc tập khác, split/target | Chưa chọn |
| E2 external stress | XQLFW có điều kiện | 6.000 pairs có ảnh, ZIP nguyên vẹn; official folds trùng identity | Quyền ảnh, vai trò external và ngưỡng phát triển từ tập độc lập | Có điều kiện |
| Portal/video external | ChokePoint có điều kiện | Protocol và quyền nghiên cứu phi thương mại công bố | File/nhãn/reference-probe thực, chi phí lưu trữ | Có điều kiện |
| E3 workflow | Fixture giả lập từ T-008 dự thảo | Scenario/BR/FR/TQ và state semantics | Review T-008, profile policy, expected outcome có người duyệt | Có thể thiết kế, chưa chấm |
| M1 thiết bị | PC tham chiếu; thiết bị đích TBD | Runtime smoke T-009 trên PC | Thông số thiết bị, tải đến, điểm bắt/kết thúc thời gian | Chưa khóa |

Nếu không candidate nào vượt data gate, protocol phải ghi **blocked by data evidence**, không chọn dataset chỉ vì dễ tải.

## 4. Split và chống leakage

### Detection
- ưu tiên split chính thức;
- không để frame gần nhau cùng sequence rơi vào cả dev và test nếu gây leakage;
- subset tự tạo phải có manifest bất biến và quy tắc lấy mẫu.

### Verification
- **Giao thức chính thức:** giữ đúng fold/pairs của tác giả; dev chỉ gồm fold được chỉ định trước, fold held-out không được dùng tune. XQLFW chính thức có identity overlap giữa các fold, nên báo là pair-fold evaluation, không là unseen-identity test.
- **Giao thức tự tạo nếu thật sự cần unseen identity:** gán identity vào dev/test trước khi lập cặp, loại cặp nối qua hai phía; pin seed và manifest, báo số identity/cặp genuine/impostor của mỗi phần và lý do còn đủ/không đủ để ước lượng FMR. Không gọi đây là kết quả benchmark chính thức của tác giả.
- Chỉ chọn một protocol chính cho câu hỏi E2 **trước** khi nhìn score; protocol còn lại nếu dùng phải ghi vai trò external/sensitivity rõ. Không dùng cùng cặp hoặc identity test để tune rồi tuyên bố unseen.
- Kiểm overlap với identity huấn luyện weight nếu nguồn công bố cho phép; nếu không chứng minh được, ghi giới hạn.
- Threshold/config chỉ chọn trên dev, locked test chạy sau freeze, external set không dùng tuning.

### Workflow fixture
- fixture nghiệp vụ tách khỏi dữ liệu mặt;
- mỗi case có input state, policy config, expected transition/outcome và trace về T-008.

## 5. Preprocessing và điều kiện so sánh

Fair comparison không có nghĩa mọi model phải dùng cùng preprocessing. Mỗi run phải pin:
- model/weight source;
- checksum;
- input size;
- color order;
- normalization;
- detector score/NMS threshold nếu có;
- landmark/alignment rule;
- similarity/distance function và chiều score;
- runtime/library version.

Sau khi freeze, không sửa preprocessing dựa trên test result; nếu cần thay đổi phải mở revision/experiment mới.

## 6. Metric và acceptance criteria

| Experiment | Metric chính | Metric phụ | Acceptance target |
|---|---|---|---|
| E1 detector | metric chuẩn dataset / recall/AP phù hợp | latency, resource, error slices | TBD từ rủi ro và thiết bị |
| E2 verification | FMR/FNMR, ROC/TAR@FMR | EER, latency/resource | TBD từ rủi ro T-008 |
| E3 workflow | expected outcome pass/fail theo từng invariant/fixture | số ca retry/manual/unresolved; audit đầy đủ hay thiếu | Theo profile đã được duyệt; chưa có profile thì chưa chấm pass/fail phần phụ thuộc |
| M1 vận hành | thời gian attempt thường lệ, review và fallback **đo riêng** khi có luồng tương ứng | median/tail latency, RAM, số lượt đến và thời gian chờ nếu quan sát được | TBD theo tải và thiết bị; không suy giảm nhân lực từ latency model |

**Định nghĩa E2:** FMR = số impostor attempts được chấp nhận / tổng impostor attempts hợp lệ; FNMR = số genuine attempts bị từ chối / tổng genuine attempts hợp lệ tại cùng operating point. Các lượt inconclusive/retry/manual phải được báo **riêng** cùng coverage; không lặng lẽ tính thành match hoặc non-match. Báo denominator, số identity, khoảng tin cậy và số attempt tối thiểu có thể hỗ trợ operating point được yêu cầu. Nếu target FMR nhỏ hơn khả năng ước lượng từ dữ liệu, kết luận là **không đủ bằng chứng**.

**Quy tắc acceptance:** trước khi mở locked test, nhóm phải duyệt nguồn của FMR/FNMR target, giới hạn retry/manual, điều kiện thời gian/tài nguyên trên thiết bị và outcome policy. Nếu chưa có các giá trị đó, vẫn có thể khóa cách thu **số liệu mô tả** cho baseline khám phá, nhưng không ghi đạt/không đạt yêu cầu nghiệp vụ hoặc chọn model cuối. Không chọn target sau khi xem test; thay đổi target phải ghi revision và dùng test chưa bị nhìn để xác nhận.

## 7. Thiết bị và cách đo

Nếu target hardware chưa chốt, tách:
- **reference environment** để tái lập baseline;
- **target environment** chỉ thêm khi nhóm xác nhận thiết bị triển khai.

Với latency/resource:
- ghi CPU/GPU, RAM, OS, runtime version;
- warm-up trước đo;
- cùng procedure và cùng scope thời gian giữa candidate;
- báo median và percentile phù hợp;
- model-only và end-to-end latency phải được phân biệt nếu đo cả hai.

## 8. Reproducibility manifest cho T-011

Mỗi run phải ghi:
- `experiment_id`;
- commit SHA;
- dataset version/checksum;
- manifest/split version;
- weight checksum;
- preprocessing config;
- seed nếu có randomness;
- package/runtime versions;
- hardware;
- raw predictions/results lưu cục bộ có kiểm soát; trong Git chỉ đưa tổng hợp đã loại định danh/ảnh/embedding;
- metric summary;
- deviation log.

Không âm thầm thay dataset, weight, threshold hoặc preprocessing giữa các run.

## 9. Freeze gate trước T-011

T-010 chỉ được coi là **locked** khi:
1. T-008 đã review đủ để không còn thay đổi capability trực tiếp ảnh hưởng experiment, hoặc điểm mở đã được ghi rõ;
2. dataset cho từng run vượt data gate;
3. weight/preprocessing được pin;
4. split/manifest đóng băng;
5. metric và procedure đo được chốt;
6. acceptance target và policy profile có nguồn/người duyệt; nếu còn TBD, chỉ được khóa **protocol đo mô tả**, không khóa kết luận pass/fail hay final technical decision;
7. Minh Hy review protocol **trước khi nhóm xem baseline**.

**Trạng thái hiện tại: CHƯA FROZEN.** T-008/T-009 còn draft, chưa có main dataset vượt toàn bộ gate, chưa có target hardware hoặc target rủi ro nghiệp vụ. T-011 không được trình bày như locked comparative baseline. Có thể chuẩn bị code/fixture và kiểm thử khả dụng không nhìn test score; run mô tả sau này phải ghi rõ scope và limitation.

Mọi thay đổi sau freeze phải có revision/experiment mới và lý do.

## 10. Bàn giao cho T-011

T-011 nhận:
- danh sách run được phép chạy;
- manifest/split đã khóa;
- config per candidate;
- metric/procedure;
- environment/measurement procedure;
- expected artifacts/naming;
- danh sách TBD/limitation không được suy diễn.

T-011 chỉ tạo **evidence thực nghiệm**; chưa chọn final model/pipeline.

## 11. Điểm đang mở

- T-008 PR #3 chưa review xong.
- Main detection và main verification dataset chưa vượt đầy đủ file/label/rights/domain gate. XQLFW đã kiểm archive/pairs nhưng quyền ảnh còn cần xác nhận; 10 fold chính thức trùng identity, không chứng minh unseen identity.
- Target hardware, tải đến và As-Is vận hành chưa xác nhận; PC chỉ là môi trường tham chiếu.
- Policy profile/authority và acceptance target nghiệp vụ cho FMR/FNMR, retry/manual, latency chưa được nhóm duyệt.
- EdgeFace/AdaFace/R50 chưa qua runtime/preprocessing gate tương đương MobileFaceNet; E2 hiện chưa có so sánh nhiều encoder hợp lệ.

Chuỗi trace: **T-008 capability/risk → T-009 candidate audit → T-010 protocol được review/khóa khi đủ gate → T-011 baseline evidence → T-012 phân tích lỗi/chọn câu hỏi experiment → experiment và review → final technical decision**.
