# T-016 — So sánh B0/P1/P2 và phân tích lỗi S4 từ output T-015

**Ngày:** 2026-09-28. **Người thực hiện:** Quốc An (Codex hỗ trợ); Minh Hy review theo Sheet. **Trạng thái:** phân tích mô tả đã chạy trên output khóa, chưa chốt cấu hình cuối. **Nguồn:** [T-014 protocol](../04-optimization/T-014-method-protocol.md), [T-015 run](../04-optimization/T-015-proposed-run.md), [script replay T-016](../../scripts/t016_analyze_s4.py). Đây là proxy XQLFW cho **chọn mặt S4**, không phải lượt check-in hoặc phép đo xác minh 1:1 S8.

## 1. Câu hỏi, nguồn và điều kiện so sánh

T-008 cần chọn đúng người tương ứng hồ sơ đã khai trước khi xác minh 1:1. B0/A0 từ chối kết luận nếu detector thấy nhiều mặt. T-015 thử P1 (ép chọn top cosine) và P2 (chọn nếu `s1 ≥ τ` và `s1 − s2 ≥ δ`, nếu không unresolved). T-016 chỉ đọc lại **development raw, evaluation raw, manifest nhãn/scene và cấu hình P2 đã khóa**; không chạy model, đổi ground truth, thay split hoặc tìm ngưỡng mới.

Script replay kiểm SHA-256 của năm file private trước khi tính bảng: development raw `ff1f98c1…269fbd`, evaluation raw `bfb45235…9d1209`, P2 config `a63f64d7…ff7980d`, label `747f9f08…a9ce333785`, scene `ae80423e…5b769c74`. Hash đầy đủ và vị trí file ở [handoff T-015](../handoffs/T-015-s4-proxy-run.md). Cấu hình giữ nguyên `τ=0,14789717107158995`, `δ=0,07647264965285691`. Detector, encoder, crop, ảnh và CPU runner giống nhau giữa B0/P1/P2; chỉ quy tắc S4 thay đổi. Các kết luận **conditional on** tập tự xác nhận và box detector đã chọn.

Đơn vị chấm: *scene + reference*. Có 64 scene/split trước audit; development dùng được 43 present, 37 absent; evaluation 41 present, 35 absent. Trên evaluation, 23 present và 29 absent không vào mẫu chấm vì `AMBIGUOUS`/reference/audit conflict; không chọn sample theo lỗi model. Tất cả 41+35 trial dùng cảnh có ≥2 detection; **không có lát cắt single-face** trong T-015. Hai reference của một scene có tương quan, không coi 76 trial là 76 scene độc lập.

## 2. Kết quả paired trên cùng evaluation

| Target-present, N=41 | Chọn đúng | Chọn sai người | Chưa kết luận |
|---|---:|---:|---:|
| B0/A0 | 0 | 0 | 41 |
| P1 top-1 | 40 | 1 | 0 |
| P2 selective | 35 | 0 | 6 |

| Target-absent, N=35 | Không chọn mặt | Chọn một mặt sai |
|---|---:|---:|
| B0/A0 | 35 | 0 |
| P1 top-1 | 0 | 35 |
| P2 selective | 33 | 2 |

P2 so với B0 chuyển **35/41** present từ unresolved sang chọn đúng, nhưng chuyển **2/35** absent từ không chọn sang chọn một mặt. P2 so với P1 tránh ca chọn sai present duy nhất và tránh **33/35** false-selection absent; đổi lại **5** present mà P1 chọn đúng trở thành unresolved (ca thứ sáu là ca P1 chọn sai). P2 đúng present **35/41 = 85,4%** (Wilson 95%: 71,6–93,1%); false-selection absent **2/35 = 5,7%** (1,6–18,6%). `0/41` wrong-target present của P2 vẫn có giới hạn trên Wilson khoảng **8,6%**, không chứng minh tỷ lệ lỗi bằng 0. Trong số present đã được chọn, wrong-target là **1/41** với P1 và **0/35** với P2; B0 không chọn nên tỷ số này không xác định. Những con số này không thể cộng thành “accuracy hệ thống”.

P1 false-select **35/35 absent theo định nghĩa thuật toán**: đầu vào luôn có ≥2 detection và P1 luôn lấy top-1 dù top-score thấp/âm; đây là rủi ro của ép chọn, chưa phải false acceptance ở S8. B0 luôn unresolved trên present vì điều kiện nhánh, không cho biết B0 trên mọi lượt camera. `NO_FACE_SELECTED` khi absent là kết quả S4 trên proxy, không tự xác nhận vắng thi.

**Lát cắt số mặt của P2:** present 2 mặt 29 đúng/5 unresolved (N=34), 3 mặt 4/1 (N=5), 4 mặt 2/0 (N=2). Absent 2 mặt 28 không chọn/1 false-select (N=29), 3 mặt 3/1 (N=4), 4 mặt 2/0 (N=2). Mẫu 3–4 mặt quá ít để kết luận xu hướng theo số mặt.

## 3. Hai điều kiện P2 làm gì — mô tả, không chọn rule mới

| Split/nhóm | N | Qua `τ` | Qua `δ` | Qua cả hai = P2 chọn |
|---|---:|---:|---:|---:|
| Development present | 43 | 40 | 41 | 40 |
| Development absent | 37 | 1 | 14 | 0 |
| Evaluation present | 41 | 38 | 37 | 35 |
| Evaluation absent | 35 | 2 | 12 | 2 |

Ở development, một absent có top-score vừa qua `τ` (`development-050`: 0,15278) nhưng gap chỉ 0,02149 nên `δ` ngăn chọn; bởi vậy 0/37 absent được P2 chọn khi tune. Ở evaluation, hai absent qua **cả hai** điều kiện nên P2 vẫn chọn sai. Trong 41 present evaluation, ba trial rớt score, bốn rớt margin, trong đó một trial rớt cả hai: tổng cộng sáu unresolved. Margin ngăn P1 chọn sai ở `evaluation-014`, đồng thời giữ unresolved hai trial P1 chọn đúng là `evaluation-030/032`. Đây là phân rã **điều kiện đã khóa**, không là phép thử thêm candidate score-only/gap-only hoặc căn cứ để sửa `τ,δ` sau evaluation.

## 4. Từng sample trọng yếu trên evaluation

`top` là cosine lớn nhất; `gap` là top trừ top-2. Box/score lấy từ raw đã khóa. `GT` là box mục tiêu được self-confirm, `NONE` cho target-absent. Số làm tròn chỉ để trình bày; replay dùng đủ precision.

| Sample / loại | Mặt | GT | P1 | P2 | Top | Gap | Quan sát trực tiếp và nhóm lỗi |
|---|---:|---:|---|---|---:|---:|---|
| `evaluation-009` present | 2 | 1 | Đúng 1 | Unresolved | 0,0526 | 0,0100 | Rớt cả `τ` và `δ`; ảnh reference nhìn mờ. |
| `evaluation-014` present | 2 | 0 | **Sai 1** | Unresolved | 0,1634 | 0,0401 | MBF xếp box 1 trên GT 0, R50 audit xếp GT 0; margin chặn chọn sai. Reference mờ; chưa chứng minh đó là nguyên nhân. |
| `evaluation-018` present | 2 | 1 | Đúng 1 | Unresolved | 0,1065 | 0,1012 | Chỉ rớt `τ`; reference mờ. |
| `evaluation-030` present | 2 | 0 | Đúng 0 | Unresolved | 0,2892 | 0,0467 | Chỉ rớt `δ`: hai score gần nhau 0,2892/0,2425; scene nhìn mờ. |
| `evaluation-032` present | 2 | 0 | Đúng 0 | Unresolved | 0,2151 | 0,0273 | Chỉ rớt `δ`: hai score gần nhau 0,2151/0,1878; reference mờ. |
| `evaluation-047` present | 3 | 0 | Đúng 0 | Unresolved | 0,1417 | 0,1312 | Chỉ rớt `τ` 0,0062; reference mờ. |
| `evaluation-025` absent | 3 | NONE | Sai 2 | **Sai 2** | 0,2360 | 0,1820 | Qua cả hai gate; mặt box 2 nhỏ/nhìn mờ trong scene. Label absent chỉ self-confirm. |
| `evaluation-053` absent | 2 | NONE | Sai 1 | **Sai 1** | 0,1948 | 0,1739 | Qua cả hai gate; mặt box 1 nhỏ hơn mặt chính và cúi/không rõ. Label absent chỉ self-confirm. |

Sáu present unresolved chia thành: **score-only 2** (`018/047`), **margin-only 3** (`014/030/032`), **cả hai 1** (`009`). Cả sáu có GT box trong scene, và detector tạo lại box ổn định theo audit; không có bằng chứng **detector miss target** trong sáu trial này. `evaluation-014` là một lỗi **ranking/selection theo embedding MBF** trên nhãn hiện có. Các quan sát mờ, góc mặt, box nhỏ ở contact sheet là tín hiệu điều tra chất lượng ảnh; chưa có quality metric hoặc thí nghiệm kiểm soát nên **không gán chúng là nguyên nhân đã chứng minh**. Không đổi ground truth vì R50/MBF bất đồng.

## 5. Vì sao hai absent false-selection đáng chú ý

| Phân bố absent | Top-score min / median / max | Gap min / median / max |
|---|---|---|
| Development (N=37) | −0,0474 / 0,0318 / **0,1528** | 0,0005 / 0,0636 / 0,2001 |
| Evaluation (N=35) | −0,0543 / 0,0495 / **0,2360** | 0,0066 / 0,0610 / **0,1820** |

`evaluation-025` có top/gap **0,2360/0,1820**, `evaluation-053` **0,1948/0,1739**. Chúng là **hai top-score lớn nhất và hai gap lớn nhất của absent evaluation**; cả hai top-score vượt max absent development 0,1528. Điểm của chúng cũng nằm trong vùng score của present, nên hai gate không tách hoàn toàn present/absent trên dữ liệu chưa xem. Điều này giải thích **về mặt quyết định** vì sao P2 chọn sai: cả score và margin đều vượt ngưỡng đã khóa; không chứng minh nguyên nhân ảnh/model hoặc một thay đổi phân bố tổng thể từ mẫu nhỏ.

Kiểm ảnh audit và R50 trước candidate không phát hiện target absent hiện diện: R50 max của hai absent là khoảng 0,140 và 0,006, thấp hơn positive anchor cùng scene khoảng 0,361 và 0,427. Tuy vậy XQLFW không gán đủ identity người nền; self-confirm không chứng minh tuyệt đối rằng reference absent không là người nền. Do đó gọi đây là **false-selection theo proxy label đã khóa**, không gọi là false accept của S8 hay lỗi truy cập phòng thi.

## 6. Phân nhóm failure mode và chi phí

| Nhóm | Evidence T-015/T-016 | Điều chưa xác định |
|---|---|---|
| Quy tắc B0 tránh rủi ro bằng abstain | 41/41 present unresolved, 35/35 absent không chọn trên cảnh nhiều detection | Coverage và throughput trên phân bố camera thật. |
| P1 ép chọn khi target vắng | 35/35 absent false-selection; một present chọn sai | Verification S8 có chặn được selection sai hay không. |
| P2 score thấp / similarity gần nhau | 3 present rớt score, 4 rớt margin, 1 trùng; 2 absent qua cả hai | Quality ảnh, encoder hay cơ chế crop gây score/gap đó; cần phép đo riêng. |
| Detector/scene preparation | Mọi present được chấm có GT box; 1/64 scene development là extra detection, 9 visual ambiguous mỗi split; reference nhiều detection cũng bị loại | Không đo recall detector trên mọi người/cảnh; không thể quy lỗi S4 cho detector ở tám trial trọng yếu. |
| Label/protocol | Một người self-confirm; R50 chỉ cross-check, target center nhập từ box đã chọn; background identity thiếu nhãn | Tỷ lệ sai nhãn thật và sai khác này làm đổi bao nhiêu outcome. |

Chi phí giữ điều kiện T-015: trên CPU runner tham chiếu, scene decode+detect median/p95 **44,13/51,97 ms**; reference decode+detect **41,85/53,80 ms**; scene embedding **22,75/34,43 ms mỗi mặt** (169 lượt), reference embedding **26,81/38,05 ms**. Quyết định P1/P2 sau score lần lượt median **0,0058/0,0012 ms**; chi phí chính của P1/P2 là embeddings, không phải so hai số. Không cộng các median thành latency đầu-cuối, không coi 76 reference-trial là 76 scene độc lập, và không suy ra tốc độ thiết bị cửa phòng.

## 7. Độ tin cậy của phép so và quyết định T-016

**Điều vẫn kiểm được:** raw/split/nhãn/config có hash; P1/P2 chạy cùng input/encoder/detector; tham số P2 được khóa trên development trước một lượt evaluation. Trên tập box/nhãn *đã chấp nhận*, paired counts và điều kiện gate có thể tái tính bằng [script replay](../../scripts/t016_analyze_s4.py). Sai khác gán nhãn không thay đổi phép tính từ raw.

**Điều không thể bảo đảm:** T-014 yêu cầu ghi điểm tâm mục tiêu trên ảnh gốc rồi nối box duy nhất. T-015 lấy điểm tâm từ **box đã nhận diện trực quan**. Vì vậy bước nối target với detector box không độc lập; nếu box thiếu, lệch hoặc chồng nhau, quy trình có nguy cơ chỉ giữ ca thuận lợi cho detector và làm yếu ground truth. R50/ảnh gốc giảm rủi ro nhầm nhưng không thay reviewer độc lập; identity người nền không đầy đủ làm yếu nhãn absent. Không thể định lượng bias chỉ từ raw hiện có. Các ca bị loại (evaluation 23/64 present, 29/64 absent) cũng làm kết quả conditional on ca dễ xác nhận. Chỉ có **một lượt evaluation**, nên Wilson theo sample không đại diện độ biến thiên giữa các lần chạy. Đây là giới hạn **trực tiếp của kết luận S4**, không được sửa nhãn sau khi biết P1/P2.

**Kết luận lựa chọn:** evidence đủ để giữ **selective S4 là hướng ứng viên** vì giải quyết 35/41 present mà B0 bỏ ngỏ và giảm 33 absent false-selection so với P1. Evidence **chưa đủ để chốt P2 với `τ,δ` này làm pipeline cuối**: vẫn 2/35 absent false-selection, khoảng tin cậy rộng, proxy self-confirm và sai khác nhãn. Chưa có căn cứ kết luận phải bỏ thiết kế S4 hoặc đổi model; cần xác nhận sạch trước quyết định triển khai. T-017 hiện là task tổng hợp quyết định trên Sheet nên không nên viết “final” từ T-015/T-016 này.

**Đề xuất task rerun riêng trước quyết định T-017, chưa thực hiện:** lập protocol version mới *trước khi xem score mới*; chọn cố định từ identity/scene XQLFW **chưa dùng trong T-015**, tách khỏi pilot và giữ identity-disjoint; ghi điểm mặt mục tiêu trực tiếp trên ảnh gốc trước khi hiện box/score, sau đó kiểm nối một box duy nhất, metadata và R50 phụ trợ. Pre-register target-present/absent, số ca tối thiểu, denominator, trường hợp ambiguous và cách kiểm background identity trong giới hạn dữ liệu có sẵn. Giữ B0/P1/P2 và `τ,δ` hiện tại như cấu hình **frozen confirmatory**; chạy một lượt holdout mới, không hiệu chỉnh theo kết quả. Nếu không có nguồn đủ nhãn absent/identity, báo limitation hoặc not runnable. Không thay thế T-015, không coi rerun tương lai là sửa lỗi trên evaluation đã mở.
