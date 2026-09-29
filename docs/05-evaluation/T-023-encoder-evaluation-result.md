# T-023 — Holdout kiểm nhu cầu thay hoặc fine-tune MobileFaceNet

## Câu hỏi và điều kiện

**Câu hỏi duy nhất:** evidence mới có buộc nhóm rời MobileFaceNet hiện tại để thay/fine-tune encoder không? [Protocol](../04-optimization/T-023-encoder-assessment-protocol.md) dùng BFW nguồn tác giả và controlled two-panel scene, [ground truth](T-023-evaluation-freeze.md) có trước MobileFaceNet score. Development/evaluation tách identity nội bộ; **không dùng T-022 evaluation** để tạo nhãn, tune, chọn model hay θ. Bản freeze code/data/rule SHA-256 `ca43678f6fab121129f18698f7a737d8f37f46e099f72d6166ab1985f940ab19`, commit trước run `cf62da87fdfc4d6000855b62da556780325f8339`. Chạy holdout **một lượt**; raw private SHA-256 `997e47b17dacefd5fca3615566096b397013583f1188e42f2bd7ba4dd399c484`, summary `30382141513182b193e6e0d723dbf1eca0dfea4622c76617c197807710ca4392`. Không sửa GT, P2, source, code scoring hay θ sau run.

## Mẫu số và S4

BFW fold 4–5 có 60 anchor, 296 identity xuất hiện trong source của group, không giao 404 identity development. Từ 300 scene evaluation đã khóa, **60 present + 238 absent usable**, 2 absent challenge `AMBIGUOUS` trước score; 240 genuine + 240 ordinary pair usable. P2 chọn đúng 55/60 present, unresolved 5, wrong present 0. Trên 238 absent, P2 no-select 200, false-select 38: **3/120 random** và **35/118 challenge**. Hard negatives này thuộc **29 anchor**; đạt điều kiện nghiên cứu đã đặt trước `≥20` trial/anchor và selected genuine `≥50`. Challenge được làm giàu bằng score SENet50 từ nguồn nên tỷ lệ false-select của proxy **không** đại diện tỷ lệ ngoài cửa phòng.

## Phân bố cosine chưa dùng để đổi ngưỡng

| Nhóm evaluation | n | min | p05 | median | p95 | max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Genuine pair | 240 | -0,0758 | 0,1431 | 0,4598 | 0,6915 | 0,8343 |
| Ordinary impostor pair | 240 | -0,2020 | -0,1017 | 0,0051 | 0,1217 | 0,2450 |
| Genuine được P2 chọn đúng | 55 | 0,2391 | 0,3071 | 0,5065 | 0,6972 | 0,7856 |
| Hard negative P2 chọn | 38 | 0,1490 | 0,1499 | 0,1887 | 0,2508 | 0,3069 |

Selected genuine và hard-negative score giao nhau ở `0,2391–0,3069` (3/55 selected genuine và 6/38 hard negative trong khoảng). Overlap có thật; score thông thường của hard negative cao hơn ordinary impostor rõ, nên ordinary FMR thấp không đủ chứng minh pipeline an toàn. Hai phân bố vẫn cho một vùng trade-off kiểm được; không kết luận threshold luôn bất lực.

## Kết quả tại rule đã khóa trước evaluation

`θ_research=0,23` được chọn **chỉ từ development** theo rule: trong grid 0,01, giữ selected-genuine accept `≥95%`, giảm hard-negative accept; hòa thì ưu tiên genuine-pair FNMR, ordinary FMR rồi θ nhỏ hơn. `0,15` là mốc lịch sử và `0,25` stress point, không dùng holdout để chọn lại.

| θ | Genuine FNMR | Ordinary FMR | Selected genuine accept | Hard-negative accept | Pipeline absent: no-select / S8 reject / S8 accept |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0,15 (lịch sử) | 14/240 | 3/240 | 55/55 | 36/38 | 200 / 2 / 36 |
| **0,23 (primary research)** | **21/240** | **1/240** | **55/55** | **8/38** | **200 / 30 / 8** |
| 0,25 (stress) | 26/240 | 0/240 | 54/55 | 3/38 | 200 / 35 / 3 |

Tại mốc primary, genuine-pair FNMR = **8,75%**, ordinary-impostor FMR = **0,42%**; hard-negative accept có điều kiện = **8/38 = 21,1%**. Tám trial được accept thuộc tám anchor khác nhau và đều ở stratum challenge. So mốc 0,15, S8 chặn thêm 28/38 hard negative nhưng genuine pair bị reject thêm 7/240; trên selected genuine, holdout vẫn accept 55/55. Không gọi 8/38 là real-world FAR hay 8/238 là tỷ lệ check-in sai. S8 tái dùng cùng cosine P2; đây chỉ là tác dụng rule score, **không** là hàng rào nhận dạng độc lập.

## Tám ca còn lọt ở θ=0,23

ID chỉ là mã trial proxy; ảnh/identity không đưa vào Git. Nhãn absent xuất phát BFW source trước score và đã qua self-review; không dùng output model để sửa nhãn sau run.

| Trial | Cosine được chọn | P2 margin | S8 |
| --- | ---: | ---: | --- |
| `f4-009-4` | 0,253824 | 0,310173 | accept |
| `f4-011-4` | 0,247768 | 0,299039 | accept |
| `f4-018-3` | 0,235610 | 0,143622 | accept |
| `f5-001-3` | 0,248488 | 0,144740 | accept |
| `f5-005-4` | 0,249615 | 0,146215 | accept |
| `f5-007-4` | 0,250229 | 0,293399 | accept |
| `f5-024-3` | 0,233463 | 0,212606 | accept |
| `f5-029-3` | 0,306908 | 0,303361 | accept |

Hai scene absent challenge khác (`f4-007-3`, `f5-029-4`) đã được gắn `AMBIGUOUS` **trước score** do nghi ngờ quan hệ identity giữa reference/panel, không nhập mẫu số 238. Rà lại hình của vài ca accept sau run chỉ dùng để diễn giải, không thay exclusion/GT.

## Đối chiếu development → holdout và quyết định T-023

Development có 41 hard negative/30 anchor và 57 selected genuine; tại θ=0,23, hard accept **11/41**, selected genuine **55/57**, genuine pair reject **25/239**, ordinary accept **0/240**. Holdout có **8/38**, **55/55**, **21/240**, **1/240** tương ứng. Hướng trade-off lặp: ngưỡng nghiên cứu cao hơn 0,15 giảm mạnh hard accept, nhưng tăng genuine FNMR; vẫn còn hard accept.

**Quyết định nghiên cứu:** giữ MobileFaceNet làm baseline/ứng viên hiện tại. Tập holdout độc lập có đủ hard negative cho thấy một operating region hữu ích, nên **chưa có bằng chứng buộc phải thay hoặc fine-tune encoder**. Đồng thời 8/38 hard negative vẫn qua S8 ở θ primary: **chưa đủ căn cứ chốt auto-accept, model hay ngưỡng triển khai**. Business false-accept cap của demo còn `TBD`. Nếu sau này cần mức rủi ro thấp hơn vùng trade-off này cho phép, hãy mở task mới với risk requirement và benchmark/split riêng rồi mới so encoder hoặc fine-tuning; không dùng holdout T-023 để chọn/tune model tiếp.

## Giới hạn

BFW lấy ảnh khuôn mặt web/VGGFace2, scene hai panel là synthetic proxy, không có camera cửa phòng, claim–actor hay tần suất người nền thật. Challenge dùng SENet50 score để chọn non-target giống mặt; đây là **conditional stress test**, không mẫu ngẫu nhiên của cửa thi. Metadata danh tính do nguồn cấp; một người rà contact sheet, không có reviewer độc lập và không rà từng pair thường bằng mắt. Tồn tại khả năng nhãn nguồn sai hoặc identity/ảnh web trùng với dữ liệu train MobileFaceNet, chưa audit hết. Nhiều trial cùng anchor phụ thuộc nhau. CPU runtime scoring holdout khoảng **38,7 s cho 1.002 source face và 298 scene**, không là latency một lượt check-in hay thiết bị đích.
