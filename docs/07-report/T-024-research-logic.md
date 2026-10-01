# T-024 — Mạch nghiên cứu: từ bài toán cửa phòng thi đến cải thiện S4/S8 và bàn giao app

Ngày tổng hợp: **2026-10-01**. Đây là tài liệu tổng hợp nguồn đã có, không phải một experiment mới hay quyết định thay model. Dùng để chuẩn bị báo cáo 10–12 phút và làm nguồn viết báo cáo DATN. Khi số liệu có khác biệt, ưu tiên protocol, raw output và report của run tương ứng.

## 1. Tóm tắt điều nhóm đã làm

Nhóm chọn bài toán thiết bị tại cửa phòng thi hỗ trợ kiểm tra thí sinh đã khai hồ sơ. Hướng chính là **claim hồ sơ → xác minh người với hồ sơ theo 1:1**, kết hợp kiểm tra ca/phòng và ghi nhận check-in. Sau khảo sát có giới hạn, nhóm chạy baseline B0 trước, phân tích failure rồi mới nghiên cứu hai cải thiện:

1. **S4 — selective target selection:** thay nhánh multi-face luôn unresolved bằng phương pháp chọn candidate có kiểm soát theo similarity và margin, được so với B0 và forced-selection P1.
2. **S8 — verification decision:** kiểm failure truyền từ S4 sang S8, thiết kế benchmark có genuine/ordinary impostor/S4-derived hard negative, rồi chọn operating point nghiên cứu bằng development và xác nhận trên evaluation khóa.

Không có model mới được train/fine-tune. Cải thiện hiện tại thuộc **cách sử dụng embedding và decision rule**. Evidence giữ MobileFaceNet làm baseline hữu ích; chưa buộc mở nhánh encoder mới. T-024 đã chốt policy demo và bàn giao để Hy build app, sau đó mới freeze bài test end-to-end cuối.

**Chưa có:** kết quả app/camera cửa phòng thi thật; bằng chứng giảm số nhân sự; false-accept cap được chấp nhận; cấu hình production-ready; so sánh đầy đủ app B0 với app tối ưu trên một benchmark duy nhất.

## 2. Nguyên tắc xuyên suốt

```text
Business Problem → Problem Decomposition → Stage Requirements
→ Data / Technical Requirements → Survey → Candidate Selection
→ Experiment → Evidence → Technical Decision → Implementation
```

Trong mỗi vòng nghiên cứu:

```text
Observation → Question → Protocol → Evidence → Decision → Why next
```

Survey chỉ chọn **candidate đáng thử**. Final technical decision cần evidence experiment. Không sửa business requirement để fit candidate; không tune evaluation; không tìm lý do sau khi đã chọn.

## 3. T-002/T-004: vì sao chọn bài toán này?

### Vấn đề và hướng đề xuất

Ở cửa phòng thi cần đối chiếu người đến với hồ sơ, ca và phòng; ghi nhận đến/check-in và xử lý ngoại lệ. Nhóm đề xuất thiết bị hỗ trợ bước đầu vào để giảm thao tác đối chiếu thường lệ và tạo ghi nhận có thể truy vết. Đây là **mục tiêu**, chưa phải hiệu quả thực địa đã đo.

Nhóm An và Hy thống nhất hướng đề xuất T-002 qua [D-001](../00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md). Bài toán attendance lớp học/nhận diện 1:N không được tự động chuyển thành bài toán chính. Sau đó [D-002](../00-project/decisions/T-007-D-002-chon-huong-khao-sat-t005.md) chọn T-005 làm hướng survey phù hợp.

### Vì sao thiết bị ở cửa?

Điểm vào phòng là nơi có thể tổ chức một lượt tương tác: khai mã → kiểm hồ sơ → kiểm người → ghi nhận. Nó liên kết được kết quả với room/session, đồng thời vẫn có người có thẩm quyền xử lý ngoại lệ. Thiết bị không tự có quyền quyết định mọi vấn đề thi cử.

### Bước tiếp theo tồn tại vì sao?

Muốn biết dùng AI ở đâu phải làm rõ nghiệp vụ, dữ liệu và quyền quyết định trước. Vì vậy cần T-008, rồi phân rã kỹ thuật; không bắt đầu bằng tên model.

## 4. T-008: business baseline và giới hạn quyền

T-008 là generic exam-entry reference workflow, không mô hình hóa một kỳ thi thực địa đã xác minh. Baseline nghiên cứu được chấp nhận trong [D-003](../00-project/decisions/T-008-D-003-chap-nhan-baseline-nghien-cuu.md); chi tiết vận hành app được phát triển tiếp qua T-024/Hy.

Các concept cần giữ riêng:

| Concept | Ý nghĩa |
| --- | --- |
| Claim/SBD | Chọn hồ sơ/reference cần kiểm; chưa chứng minh danh tính |
| Attempt | Một lượt xử lý có thể gồm nhiều capture theo ngân sách |
| Check-in | Ghi nhận được xác nhận, không đồng nghĩa đã vào phòng |
| Entry authorization | Quyền cho vào, phụ thuộc policy/thẩm quyền |
| Attendance | Kết quả dự thi/hiện diện theo định nghĩa ca; không suy ra tự động từ check-in |
| AI verdict | Kết quả kỹ thuật; không trực tiếp cấp mọi quyền nghiệp vụ |
| Human decision | Quyết định có thẩm quyền, lưu riêng; không sửa lịch sử AI |

Generic core gồm roster, room/session, attempt, verification, review, duplicate, fallback, reconciliation, correction và audit. Các giá trị late/retry/authority/attendance/retention thuộc **ExamPolicy**; model/detector/threshold thuộc **AIConfig**. Một phần policy demo đã được nhóm chốt ở T-024, không được gọi là quy chế thi thật.

Nguồn: [T-008 requirements](../01-problem/T-008-requirements.md), [bộ bàn giao Hy](../06-mobile/T-024-ban-giao-app-cho-hy/T-024-README.md).

## 5. Phân rã pipeline: bước nào cần model?

Nguồn phân rã: [T-005 task decomposition](../02-survey/T-005-quoc-an-task-decomposition.md). ID stage là phân rã chức năng, **không ép thứ tự thực thi tăng dần theo số**.

| Stage | Input → công việc → output | Loại xử lý / điều cần quan tâm |
| --- | --- | --- |
| S0 Reference preparation | Roster + ảnh nguồn → xác nhận reference → record/version hợp lệ | Data/authority; có thể dùng detector/encoder hỗ trợ |
| S1 Candidate lookup | SBD/claim → resolve hồ sơ → một record hoặc lỗi | Query/rule; không cần student classifier |
| S2 Capture | Camera → thu frame → ảnh + thời gian | Camera/API; không phải ML |
| S3 Face detection | Ảnh → phát hiện mặt/landmark → bbox/landmarks | CV model; bỏ sót/false extra detection/scale ảnh |
| S4 Subject selection | Reference + các mặt → chọn candidate hoặc unresolved | B0 rule; P2 dùng embedding score + margin; nghiên cứu chính |
| S5 Quality | Candidate/frame → kiểm dùng được → continue/retry | Rule hoặc capability cần khảo sát; chưa giả định mọi gate đã implement |
| S6 Alignment | Landmarks + mặt → chuẩn hóa hình học → crop encoder | Geometry; không cần một model mới nếu dùng landmark S3 |
| S7 Embedding | Crop → encode → vector đặc trưng | Face encoder pretrained; cost và representation |
| S8a Similarity | Reference/candidate embeddings → cosine → score | Phép tính xác định, không phải classifier mới |
| S8b Verification rule | Score + rule đã khóa → verdict | Calibration/decision; nghiên cứu risk và trade-off |
| S9 Business checks | Record/session/room/policy → điều kiện nghiệp vụ | Rule/query; pre-check và final-check |
| S10 Recording/audit | Quyết định + write → confirmed check-in + audit | Consistency/thẩm quyền; attendance vẫn tách riêng |
| S11 Optional PAD | Evidence chống giả mạo nếu scope yêu cầu | Chưa có bằng chứng triển khai; cosine không chứng minh liveness |

### Thứ tự thực thi với P2 hiện tại

```text
Claim → lookup → reference A + business pre-check
Camera → S3 detect → S6/S7 cho từng face → score với reference A
→ S4/P2 chọn theo score + margin
→ S8 kiểm selected score theo verification rule
→ final business-check → confirmed write → PASS hoặc route khác
```

P2 cần embedding của các mặt **trước khi** chọn target. S8 hiện dùng cùng representation/cosine; không được vẽ hai model độc lập nếu thực tế chỉ reuse một signal. P2 runner có nhánh dưới hai score trả unresolved; adapter app kết hợp single-face B0 và multi-face P2 cần được hiện thực rõ, không mặc định đã có app chạy.

### Cấu hình nghiên cứu tham chiếu, không phải freeze demo

| Thành phần | Cấu hình / nơi lấy bằng chứng |
| --- | --- |
| Model pack | `buffalo_sc`; SCRFD `det_500m.onnx`, MobileFaceNet `w600k_mbf.onnx`; file và SHA-256 theo external-assets/bộ bàn giao, không có checkpoint mới |
| Detection | Input 640×640, detector threshold 0,5; CPU runner theo run tương ứng |
| Alignment / encoder | 5 landmarks, InsightFace `norm_crop` 112×112; vector 512 chiều, L2 normalization, cosine |
| S4 | P2 τ/δ từ development T-015, giữ nguyên qua T-017/T-020/T-023 |
| S8 | T-020 θ_old≈0,122254; T-022 research0,15; T-023 research0,23. Mỗi ngưỡng gắn protocol riêng, không gọi cả ba là deployment configs |
| Reproducibility | Protocol/freeze gốc giữ manifest, seed, code/model/data hashes, GT, split và raw private output reference; bảng tổng hợp không thay thế run record |

Có thêm phép thử chi phí [X-012-I](../03-baseline/runs/T-012-X-012-I-conditional-embedding.md): đưa A0 trước recognition trên cùng input/model/runner, giữ outcome B0, tổng inference394,72→358,95 giây và bỏ1.993 recognition vô ích. Đây là evidence phụ về compute, **không giải quyết target selection** và không phải latency check-in. Hai cải thiện chính trong bài trình bày vẫn là S4 và S8.

## 6. T-009/T-010: chọn candidate vừa đủ rồi thiết kế phép đo

### Data requirement → candidate dữ liệu

| Nhu cầu | Evidence cần | Nguồn đã dùng | Không chứng minh được |
| --- | --- | --- | --- |
| S3 detection | Bbox/GT detection, kích thước mặt | WIDER FACE validation | Identity hay toàn nghiệp vụ check-in |
| S8 1:1/quality stress | Pair cùng/khác identity + split | XQLFW | Camera cửa phòng thật; identity mọi background face |
| S4 target selection | Reference + scene + target point/absent GT | Pilot/holdout XQLFW có audit | Identity đầy đủ của background, nhãn người gõ SBD thực địa |
| S8 hard negative chắc identity | Source ID rõ, controlled present/absent | XQLFW controlled; BFW controlled two-panel | Natural scene/camera thật; tần suất lỗi tự nhiên |
| Business workflow | Expected scenario/policy/authority | Fixture/replay/simulated states | Hiệu quả AI trên camera thật |

Nguồn/weight/quyền sử dụng, nhãn và file đã audit trong [T-009 source register](../02-survey/T-009-source-register.md) và [external assets](../00-project/external-assets.md). Dữ liệu public không đồng nghĩa tự do mọi cách dùng; không commit mặt, identity cá nhân hay checkpoint. Tập phát hiện mặt không được dùng làm bằng chứng verification.

### Problem → model family → candidate → baseline

S3 cần detector mặt có landmark để alignment. Nhóm khảo sát/đo SCRFD, YuNet, BlazeFace. S7 cần encoder mặt pretrained; MobileFaceNet là baseline nhẹ, R50 là reference mạnh hơn/cost cao hơn. Candidate khảo sát không phải tất cả đã được chạy đầy đủ.

E1 dự án trên 3.226 ảnh WIDER val/39.112 GT hợp lệ ghi AP YuNet **0,648304**, SCRFD **0,547370**, BlazeFace **0,136009**. Đây là **protocol dự án, không AP chính thức WIDER**. Không chọn model chỉ vì một AP cao nhất: interface landmark, weight, deployment/cost và benchmark kế tiếp cũng cần xét.

B0 khóa **SCRFD 500MF + MobileFaceNet + alignment + cosine**. Không tuyên bố đây là model thắng mọi benchmark. [T-012 B0 choice](../03-baseline/T-012-B0-pipeline-choice.md) ghi rationale/alternative. So encoder cùng intersection 3.666 pair cho thấy R50 ít FA/FR hơn (61/59 so với MobileFaceNet 114/108 với SCRFD), nhưng chưa có target-device requirement buộc thay encoder.

T-010 đặt câu hỏi/split/metrics trước run, giữ detection metrics, pair FMR/FNMR, coverage và timing theo đúng đơn vị. E3 là khung fixture, **không phải app đã chạy**. Nguồn: [T-010 protocol](../03-baseline/T-010-protocol.md), [T-011 summary](../03-baseline/T-011-baseline-summary.md).

## 7. B0 đã chạy trước: thấy gì và vì sao nghiên cứu S4?

Trên E2 XQLFW, 6.000 pair có **4.215 pair chấm được / 1.785 unresolved**. Trong pair chấm được: genuine 2.046, FR 125 (FNMR khoảng **6,11%**); impostor 2.169, FA 133 (FMR khoảng **6,13%**). Đây là pair-level evidence, không attempt-level FAR cửa phòng.

Audit 7.263 ảnh: **6.064 single detection / 291 no detection / 908 multiple detections**. 908 là detector trả nhiều box, **không tự động là 908 ảnh nhiều người**. Cần phân biệt false extra detection và true multi-face bằng audit.

B0 unresolved khi nhiều mặt. Vì trước cửa phòng có thể có nhiều thí sinh, câu hỏi hợp lý là: **đã biết claimed reference A, có thể chọn đúng mặt A trong scene nhiều mặt và không chọn nếu A absent không?** Dataset không cần nhãn ai gõ mã trong một kỳ thi; reference claim được mô phỏng làm input. Ground truth cần chỉ ra target thuộc reference hay absent.

Nguồn: [T-012 diagnosis](../03-baseline/T-012-B0-freeze-and-stage-diagnosis.md), [T-012 error analysis](../03-baseline/T-012-error-analysis.md). Chưa suy nguyên nhân rejection là ánh sáng/góc mặt nếu không có evidence; chưa optimize tùy ý.

## 8. T-013–T-017: cải thiện 1 — S4 target selection

### Observation → question → alternatives

**B0:** multi-face → unresolved. **P1:** chọn score lớn nhất, không abstention theo τ/δ. **P2:** selective selection chỉ khi top score và chênh lệch top–second cùng đủ điều kiện.

```text
P2 select ⇔ top_score ≥ τ AND (top_score − second_score) ≥ δ
τ = 0.14789717107158995; δ = 0.07647264965285691
```

Development T-015 tìm 81×81 = **6.561 tổ hợp** hai biến. Chỉ giữ cấu hình không wrong-selection present và không false-selection absent trên development; maximize correct selection rồi tie-break theo τ/δ như code. Đây là tìm kiếm hữu hạn có protocol, không chọn ngẫu nhiên hay tuyên bố dùng GA/PSO.

### Ground truth và clean confirmation

T-013 self-confirm đối chiếu source identity, ảnh và R50 cross-check phụ; model không phải GT duy nhất. T-014 khóa present/absent, identity split, AMBIGUOUS/exclusion. T-015 có sai khác labeling (point từ detector box), T-016 ghi hạn chế và sinh T-017 clean confirmation: target point trên ảnh gốc trước khi nối detector box, không dùng score P1/P2 sửa GT; holdout mới loại identity/sample cũ theo protocol.

T-017 64 scene audit: 57 clear, 5 ambiguous, 2 false-extra; xây **49 present và 41 absent proxy trials usable**. Không có independent human reviewer; self-confirm là limitation. Known source identity tách theo protocol, nhưng background không có đủ identity để bảo đảm toàn bộ người nền disjoint.

### Kết quả riêng S4 — cùng T-017 input, detector, encoder, rule

| Method | Present correct / wrong / unresolved (N=49) | Absent no-select / false-select (N=41) |
| --- | --- | --- |
| B0 | 0 / 0 / 49 | 41 / 0 |
| P1 | 49 / 0 / 0 | 0 / 41 |
| P2 | 46 / 0 / 3 | 39 / 2 |

P2 phục hồi **46/49 present (93,9%)** so với B0 unresolved toàn bộ trong tập multi-face này; đổi lại **2/41 absent bị false selection (4,9%)**. P1 phục hồi present nhưng ép chọn toàn bộ absent. Không gọi 2/41 là FAR thật.

**Decision:** selective S4 hữu ích ở mức nghiên cứu, chưa khóa deployment. **Why next:** S4 chọn sai rồi S8 có chặn được không? Nguồn: [T-014](../04-optimization/T-014-method-protocol.md), [T-015](../04-optimization/T-015-proposed-run.md), [T-016](../05-evaluation/T-016-comparison-ablation.md), [T-017](../05-evaluation/T-017-clean-confirmation.md), [code tuning](../../scripts/t015_s4_run.py).

## 9. T-020: kiểm failure S4 → S8, không giả định hai stage bảo vệ nhau

T-020 replay output đã khóa T-017. S8 **reuse selected-box cosine score**, không encode lại crop/reference mới. Threshold lịch sử **θ_old = 0,122254** thấp hơn score condition P2 **τ = 0,147897**. Vì vậy trong replay này, đã vượt P2 score condition thì cũng vượt S8 threshold.

| Trial absent | Face P2 chọn | Score | Margin | S8 tại θ_old |
| --- | --- | --- | --- | --- |
| holdout-010 | Box 3, non-target/background theo proxy GT | 0,238723 | 0,124619 | ACCEPT |
| holdout-018 | Box 0, non-target/background theo proxy GT | 0,156472 | 0,166434 | ACCEPT |

Không gán một identity B cụ thể cho background khi nguồn không có nhãn chắc. Không khẳng định vì sao similarity non-target cao. Cặp được so vẫn là claimed reference với selected face; evidence không chỉ ra một lỗi đổi reference để giải thích hai accept này.

```text
S4 false selection → cùng selected cosine cao
→ S8 rule thấp hơn τ → proxy acceptance
```

**Finding:** hai stage không tạo signal độc lập; replay decision barrier không chặn hai false selections. **Why T-021 exists:** cần đánh giá risk verification và separation genuine/ordinary/hard negatives, không chỉ tăng threshold để sửa đúng hai ca đã thấy.

Nguồn: [T-020 protocol](../05-evaluation/T-020-s4-s8-protocol.md), [T-020 report](../05-evaluation/T-020-s4-s8-integration.md), [decision logic](../05-evaluation/DECISION_LOGIC.md).

## 10. T-021–T-023: cải thiện 2 — S8 decision và encoder adequacy

### Câu hỏi và phép thử

S8 cần accept genuine và reject impostor, đặc biệt các non-target S4 dễ chọn do score cao. Tách ba nhóm:

- **Genuine:** reference/candidate cùng source identity.
- **Ordinary impostor:** khác identity thông thường.
- **S4-derived hard negative:** target-absent scene đã có GT identity độc lập; P2 thực sự chọn non-target. Đây là conditional subset, không đổi GT bằng score.

FMR = accepted negative pairs / valid negative pairs; FNMR = rejected genuine pairs / valid genuine pairs. Hard-negative FMR cần mẫu số riêng; pipeline-level absent denominator là toàn absent scenes.

Ground truth khóa trước score, identity-disjoint development/evaluation trong nguồn known identities, exclusion giữ nguyên, chỉ tune development; evaluation chạy một lần sau freeze. Controlled two-panel scenes là **synthetic proxy**, không ảnh cửa phòng thật. Pretraining overlap không được kiểm toán toàn bộ, nên identity-disjoint nội bộ không chứng minh encoder chưa từng gặp identity trong pretrain.

### Vì sao T-022 chưa đủ, phải có T-023?

T-022 research θ=0,15 do nhóm duyệt; evaluation 30 present/30 absent, P2 26 correct present/4 unresolved, **không có hard negative được P2 chọn** ở absent. Selected genuine 26/26 accept; all-genuine FNMR 33/355, ordinary FMR 2/131. Hard-negative N=0 nghĩa là **không đo được**, không phải chứng minh chặn tất cả hard negatives. Vì vậy T-023 đặt câu hỏi encoder có cần thay/fine-tune trên benchmark độc lập BFW, không retune T-022 evaluation.

### Protocol T-023 và rule nghiên cứu

BFW known source identity dựng present/absent hai panel; random + challenge-enriched sampling. SENet50 source scores phục vụ sampling, không phải GT và không thay MobileFaceNet. Development/evaluation identities tách (404/296); ambiguous giữ riêng trước score model đánh giá.

Development research rule: trên grid threshold 0,01, giữ selected-genuine acceptance ≥95%, giảm số hard-negative accept, tie-break theo genuine FNMR, ordinary FMR rồi threshold thấp hơn. Rule chọn **θ_research=0,23**, freeze trước evaluation. Đây là constraint nghiên cứu, **không false-accept cap nghiệp vụ/optimal deployment threshold**.

### Kết quả riêng S8 — cùng holdout BFW, P2 fixed

Evaluation: 60 present, 238 absent usable (2 ambiguous absent excluded trước score); 240 genuine pairs; 240 ordinary-impostor pairs. P2 present **55 correct / 0 wrong / 5 unresolved**; absent **200 no-select / 38 false-select**. Hard-negative subset =38 selected pairs, qua 29 anchors.

| S8 point | All-genuine reject / 240 (FNMR) | Ordinary accept / 240 (FMR) | Selected genuine accept / 55 | Hard negative accept / 38 |
| --- | --- | --- | --- | --- |
| 0,15 historical reference | 14 (5,83%) | 3 (1,25%) | 55 | 36 (94,74%) |
| **0,23 research** | **21 (8,75%)** | **1 (0,42%)** | **55** | **8 (21,05%)** |
| 0,25 stress point | 26 (10,83%) | 0 (0%) | 54 | 3 (7,89%) |

θ=0,23 chặn **30/38 hard negatives**, so với 2/38 tại 0,15, giữ 55/55 selected genuine. Trade-off: all-genuine reject tăng 14→21/240. 55 selected genuine là subset có điều kiện; không dùng 55/55 để nói FNMR toàn genuine bằng 0. 0,25 vẫn chỉ stress point, không chọn lại từ evaluation.

**Finding:** MobileFaceNet có useful separation, còn overlap và 8 accept. **Decision:** giữ encoder baseline; không tự mở fine-tuning/model search tiếp. Điều này không chứng minh an toàn hay ngưỡng demo triển khai đã đạt risk requirement.

Nguồn: [T-021](../05-evaluation/T-021-s8-risk-protocol.md), [T-022 evaluation](../05-evaluation/T-022-s8-evaluation-result.md), [T-023 protocol](../04-optimization/T-023-encoder-assessment-protocol.md), [development](../05-evaluation/T-023-development-analysis.md), [freeze](../05-evaluation/T-023-evaluation-freeze.md), [evaluation](../05-evaluation/T-023-encoder-evaluation-result.md).

## 11. Kết quả kết hợp S4 → S8: mức thứ ba, không trộn với app

Giữ P2 và dataset T-023 fixed, chỉ so S8 points đã công bố:

| Point | Present accepted / 60 | Present unresolved / 60 | Absent no-select / 238 | False-select → S8 reject / 238 | False-select → S8 accept / 238 |
| --- | --- | --- | --- | --- | --- |
| 0,15 | 55 | 5 | 200 | 2 | 36 |
| **0,23** | **55** | **5** | **200** | **30** | **8** |
| 0,25 | 54 | 5 (+1 selected genuine reject) | 200 | 35 | 3 |

Tại 0,23, proxy absent acceptance **8/238 (3,36%)** so với **36/238 (15,13%)** tại 0,15. Cùng denominator, input và P2; cải thiện **28/238** cases. Không gọi đây là real-world FAR hay effective false check-in vì chưa nối business/write app.

### Ba bảng kết quả dùng để trình bày

1. **S4 riêng:** T-017 B0/P1/P2, target-present và target-absent.
2. **S8 riêng:** T-023 genuine/ordinary/hard-negative, nhiều operating points đã khóa.
3. **S4→S8 kết hợp:** T-023 P2 fixed, absent flow và present success.

Không nhân 46/49 của XQLFW với 55/55 của BFW để tạo accuracy. Không nói đã có so sánh toàn bộ original-B0-app với proposed-app nếu chưa chạy cùng benchmark/conditions. T-020 cung cấp so sánh tích hợp lịch sử trên cùng T-017 input, nhưng không thay được phép thử app end-to-end cuối.

## 12. T-024: từ evidence sang policy và implementation

8/38 hard-negative accept còn lại không tự biến mất nhờ policy. Chính vì vậy cần tách AI verdict khỏi authority nghiệp vụ và báo số lỗi trung thực. Các quyết định nhóm đã duyệt:

| Decision | Nội dung |
| --- | --- |
| [D-004](../00-project/decisions/T-024-D-004-duyet-default-demo.md) | Default demo late ≤15 phút khi intake mở; retry theo reason nhưng mọi capture chịu global cap=3; closed-session riêng; early window TBD |
| [D-005](../00-project/decisions/T-024-D-005-auto-checkin-co-dieu-kien.md) | Auto-check-in chỉ khi profile bật + business pre/final OK + AI verified + không unresolved/duplicate + confirmed write; mode tắt chờ xác nhận |
| [D-006](../00-project/decisions/T-024-D-006-manual-authority.md) | Operator routing; Room Staff được ủy quyền xử lý manual identity/late/re-entry trong scope; Admin data/policy/correction/lifecycle; HUMAN không rewrite AI |
| [D-007](../00-project/decisions/T-024-D-007-workflow-va-risk-evaluation.md) | Workflow invariants có pass/fail; AI risk báo attempt-level, cap TBD nên chưa kết luận acceptable/safe; input replay/fixture |
| [D-008](../00-project/decisions/T-024-D-008-ban-giao-va-build-app.md) | **Build app → integrate → chạy end-to-end → freeze final-test config → test/report**; checklist test không block build app |

Outcome app: CONTINUE, RETRY, MANUAL, READY_FOR_CONFIRMATION, PASS, SYSTEM_HOLD. PASS chỉ check-in confirmed. Impostor thử 3 capture rồi 1 lần accept thì attempt đó là false acceptance, không lấy tỷ lệ frame reject che lỗi attempt.

Hy chủ trì T-018 app, T-019 integration theo Sheet. Nguồn bàn giao: [T-024 app context](../06-mobile/T-024-ban-giao-app-cho-hy/T-024-README.md), gồm role, workflow/policy, AI interface/config và model/assets cần trao ngoài Git. Chưa chứng minh Hy đã nhận đủ weight hay app tích hợp chạy được.

AIConfig hiện tại làm cấu hình nghiên cứu tham chiếu. T-024 không thay model/P2 hay retune S8; operating point end-to-end demo phải freeze trước test, không tuning từ chính test đó. Chỉ dùng dữ liệu sẵn có/replay theo phạm vi nhóm; không yêu cầu thu một dataset kỳ thi mới để hoàn thành DATN.

## 13. Traceability: tại sao task tiếp theo tồn tại?

| Observation / business need | Question | Protocol / task | Finding | Decision / next step |
| --- | --- | --- | --- | --- |
| Kiểm ở cửa cần gắn người với hồ sơ, room/session | Capability nào cần AI/rule? | T-008, T-005/T-007 | Claim lookup ≠ identity verification | Survey đúng task, không student classifier |
| Chưa có baseline project | Candidate nào chạy được, bằng chứng gì? | T-009/T-010/T-011/T-012 | B0 usable, multi-detection gây unresolved | Nghiên cứu S4 với GT thay vì optimize tùy ý |
| B0 multi-face unresolved | Có chọn target và abstain absent được không? | T-013–T-017 | P2 46/49 correct; 2/41 absent false-select | Kiểm S8 có chặn hai false selections |
| P2 vẫn false-select | S8 có evidence barrier sau S4? | T-020 replay/audit | Reuse cosine; θ_old<τ; hai case vẫn accept | T-021 verification risk/separation |
| Ordinary impostor không đại diện hard negative | Same encoder có operating region hữu ích? | T-022/T-023 | T-022 hard N=0; T-023 chặn 30/38, còn8 | Giữ encoder; không tự fine-tune; policy/app |
| AI không hoàn hảo, cần demo hoạt động đúng | Hệ thống được tự quyết định đến đâu? | T-024 | 4 policy groups + app-first approved | Hy build/integrate; final frozen test sau app |

## 14. Giới hạn và điều cần nói với thầy

- Đây là component/proxy research trên dữ liệu sẵn có; synthetic benchmark kiểm câu hỏi hẹp, không mô phỏng đầy đủ camera cửa phòng.
- GT self-confirm không có reviewer độc lập; source identity và visual audit hỗ trợ, model cross-check không là GT duy nhất. T-015 có sai khác labeling được sửa bằng run mới T-017, không sửa kết quả cũ.
- Identity disjoint áp dụng cho source identities được biết; pretraining overlap và một số background không audit đầy đủ.
- Challenge enrichment làm hard-negative benchmark khó có chủ đích; tỷ lệ lỗi không ước lượng tần suất tự nhiên.
- Sample/anchor hữu hạn, có dependency giữa trials; không biến point estimate thành bảo đảm an toàn.
- Không có target-device end-to-end latency hoặc hiệu quả giảm nhân sự đã đo. Timing component trong môi trường khác không ghép thành cải thiện latency app.
- Chưa có PAD/liveness evidence; xác minh mặt đúng ảnh không đủ chứng minh chống giả mạo.
- Risk cap TBD; θ=0,23 là research point, không threshold triển khai đã chứng minh.

## 15. Câu hỏi thầy có thể hỏi

**Đóng góp của nhóm nếu không train model?** Phân rã nghiệp vụ đúng task, dựng/audit benchmark target-present/absent, selective S4 score+margin, phát hiện dependency S4/S8, protocol risk-aware S8 và comparison có freeze/split. Đóng góp là phương pháp/pipeline/decision và evidence, không claim phát minh encoder.

**Vì sao không chọn R50 ngay?** R50 có reference results tốt hơn ở phép pair nhưng cost lớn; evidence MobileFaceNet vẫn hữu ích. Chưa có requirement/experiment buộc thay. Giữ một baseline ổn định để phân tích stage trước.

**Threshold có chọn bừa không?** S4 chọn hai biến trên development theo rule; S8 có research rule development được duyệt trước evaluation. Có trade-off và stress point, không dùng holdout chọn lại.

**S8 dùng cùng score có vô ích không?** Không có signal độc lập. Nhưng decision threshold khác có thể chặn một phần selected impostors nếu separation tồn tại; T-023 chặn30/38 là evidence hữu ích, còn8/38 là giới hạn.

**Hai optimize cải thiện toàn hệ thống bao nhiêu?** S4 có bảng B0/P1/P2 T-017; S8 và combined có bảng T-023. Chưa có một phép thử app original-B0 vs full-proposed cùng benchmark để đưa một con số tổng duy nhất.

**Có dùng train data làm test không?** Development/evaluation known IDs được tách trong project; không dùng evaluation tune. Nhưng chưa kiểm đầy đủ overlap với pretraining weights nên không tuyên bố tuyệt đối chưa thấy identity trước đó.

**Có thể auto-check-in thật chưa?** Demo profile có quyền auto-check-in có điều kiện; chưa chứng minh real-world acceptable risk. Workflow có pass/fail riêng, AI báo lỗi attempt-level; MANUAL/HOLD không che AI failure.

## 16. Cách dùng tài liệu và slide

- Slide chính nói mạch logic và ba nhóm kết quả, khoảng10–12 phút; phụ lục trả lời câu hỏi và nguồn.
- [Lời nói/nguồn theo slide](T-024-slide-notes.md) giữ giải thích dài; slide không nhồi toàn report.
- PowerPoint `T-024-report-slides.pptx` giữ chart/table/diagram editable và speaker notes.
- Khi bổ sung kết quả app, thêm một mục mới có config/hash, dataset/fixture, expected outcomes và attempt-level metrics. Không ghi đè evidence cũ hoặc gọi test sau chỉnh config là cùng evaluation.
