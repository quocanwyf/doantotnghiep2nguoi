# T-014 — Phương pháp S4 và protocol so với B0

**Trạng thái:** protocol nghiên cứu khóa trước run T-015; chưa có kết quả S4/proposed và chưa chọn cấu hình triển khai. **Người thực hiện:** Quốc An; Minh Hy review theo Sheet. **Đầu vào:** [B0 T-012](../03-baseline/T-012-B0-pipeline-choice.md), [lỗi và mốc B0](../03-baseline/T-012-B0-freeze-and-stage-diagnosis.md), [T-013 self-confirm](T-013-target-selection.md). **Phạm vi:** ảnh XQLFW có sẵn làm proxy học thuật, không là giao dịch phòng thi.

## 1. Câu hỏi và cơ sở chọn cách thử

T-008 cần nối hồ sơ đã khai với **đúng người trước camera** trước khi xác minh 1:1. B0 A0 trả `unresolved` khi detector thấy nhiều mặt; T-012 ghi 908/7.263 ảnh XQLFW nhiều detection, nhưng không coi tất cả là nhiều người thật. T-013 đã xem 24 cảnh pilot, loại ca mơ hồ và cho thấy có thể tạo nhãn proxy; **16 present và 13 absent self-confirm** chỉ dùng phát triển phương pháp, không là test.

**Question T-014:** trên cảnh nhiều người có nhãn proxy đủ nhất quán, liệu chọn mặt bằng độ giống với reference rồi từ chối kết luận khi không chắc có tạo thêm *correct target* so với A0, với bao nhiêu *wrong target*, *false selection when target absent* và chi phí tính toán?

Embeddings và khoảng cách là cách biểu diễn phù hợp để so ảnh cùng/khác người theo [FaceNet, CVPR 2015](https://www.cv-foundation.org/openaccess/content_cvpr_2015/html/Schroff_FaceNet_A_Unified_2015_CVPR_paper.html). Nhánh từ chối là một **lựa chọn thiết kế để đo risk–coverage**, không lấy kết quả của [SelectiveNet, ICML 2019](https://proceedings.mlr.press/v97/geifman19a.html) làm bằng chứng phương pháp này sẽ tốt hơn. [NIST FRTE 1:N](https://pages.nist.gov/frvt/html/frvt1N.html) tách tìm đúng người có mặt và chọn nhầm khi người không có mặt; metric T-014 được tự định nghĩa cho **ít mặt trong một cảnh**, không gọi là FPIR/FNIR theo protocol NIST.

## 2. Biến duy nhất và các đối chứng

Giữ nguyên nguồn JPG, SCRFD-500MF (640×640, detection threshold 0,5), 5 landmark/crop 112×112, MobileFaceNet trong `buffalo_sc`, L2/cosine và bước xác minh S8 của B0. B0 vẫn là cấu hình gốc, không thay bằng R50. S4 chỉ can thiệp nhánh **scene có ≥2 detection**; 0/1 detection phải cho cùng outcome/embedding như B0.

| Nhánh | S4 khi ≥2 detection | Vai trò |
|---|---|---|
| **B0/A0** | Không chọn mặt → `UNRESOLVED`. | Đối chứng gốc, sai chọn người bằng 0 nhưng coverage nhiều mặt bằng 0. |
| **P1 top-1** | Tính cosine giữa reference MBF và từng mặt; chọn score cao nhất, hòa điểm → `UNRESOLVED`. | Đối chứng chẩn đoán tác dụng của ép chọn, **không đề xuất triển khai** vì target-absent có thể bị chọn nhầm. |
| **P2 selective S4** | Sắp score `s1 ≥ s2`; chọn top-1 chỉ khi `s1 ≥ τ` **và** `s1 − s2 ≥ δ`; còn lại `UNRESOLVED`; **hòa top-score luôn unresolved**, kể cả khi `δ=0`. | Phương pháp đề xuất để thử. Hai biến `τ,δ` chỉ chọn từ development; không là policy cho phép vào phòng. |

P2 không xác nhận thí sinh được vào. Mặt đã chọn vẫn đi qua xác minh 1:1, kiểm ca/phòng và authority của app. `NONE/UNRESOLVED` khi target vắng hoặc ảnh khó **không đồng nghĩa absent attendance**.

## 3. Dữ liệu, split và nhãn

Nguồn chỉ là archive/pairs XQLFW đã pin ở [external assets A-001](../00-project/external-assets.md). [Script split T-014](../../scripts/t014_identity_split.py) kiểm hash, lấy 7.263 ảnh thuộc 6.000 pairs, loại 24 identity pilot rồi sắp toàn bộ identity theo SHA-256 của `T-014-identity-v1\0<identity>`; 70% đầu cho development, 30% còn lại cho evaluation. Manifest chi tiết chứa tên người/file ở Temp ngoài Git, SHA-256 `23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2`. Kết quả: **development 2.603 identity/5.018 ảnh**, **evaluation 1.116 identity/2.140 ảnh**; identity có genuine-reference khả dụng trước detect lần lượt 1.101 và 480. 24 pilot identity/105 ảnh không thuộc cả hai split; kiểm manifest thấy **0 identity giao nhau**. Official XQLFW pair-fold **không** dùng làm identity split.

**Khóa chọn scene trước khi chấm:** trong mỗi split, duyệt `scene_order` của manifest theo seed `T-014-scenes-v1`; chạy đúng SCRFD B0, lấy **64 scene đầu** có ≥2 detection, có genuine-reference khác ảnh và **tối đa một scene cho mỗi identity nguồn**. Không bù bằng scene chọn sau khi xem điểm S4/nhãn; nếu quét hết mà dưới 64 thì báo số thật. Với mỗi scene, `present_ref` là genuine neighbor đầu tiên theo SHA-256 của `T-014-present-v1\0<member>`; `absent_ref` là ảnh đầu tiên theo SHA-256 của `T-014-absent-v1\0<scene>\0<member>` trong cùng split nhưng identity folder khác. Không đổi reference sau khi xem ảnh/score; reference không dùng được → `AMBIGUOUS`. Mỗi scene tạo một thử present và một thử absent, nhưng hai thử **cùng scene**, không coi độc lập khi tổng hợp.

**Self-confirm trước candidate:** kiểm metadata nguồn/genuine pair/byte, xem ảnh gốc để phân biệt nhiều người thật, chỉ một target và người absent thực sự không thấy. Trên ảnh gốc ghi tâm mặt mục tiêu ở tọa độ chuẩn hóa 0–1, rồi nối vào **duy nhất một** box B0 chứa tâm đó; nếu nhiều/không box phù hợp, giữ `AMBIGUOUS` hoặc ghi `TARGET_MISSED_BY_DETECTOR`, không dùng score để chọn box. Ca absent ghi target `NONE`. Sau nhãn thị giác mới dùng **R50 audit-only** đã có ở T-011 làm tín hiệu embedding phụ. R50 chạy trên cùng box/landmark SCRFD B0, nhưng **không** là phương pháp S4 được so và không dùng trong P1/P2. T-011 đã pin hash [R50 A-003](../00-project/external-assets.md); smoke trên một cảnh pilot tạo 2 embedding/2 mặt 512 chiều. Với present, R50 phải xếp mặt đã chỉ đứng đầu; với absent, max score R50 phải thấp hơn positive anchor cùng scene. Đây là cùng kiểu quy tắc bảo thủ của [T-013](T-013-self-confirm-protocol.md), dùng weight khác MBF để tránh trường hợp nhãn đánh giá được lọc trực tiếp bằng **chính score của P1/P2**. Kết quả ảnh và R50 phải được ghi vào manifest riêng, hash/đóng dấu **trước khi mở điểm MBF của candidate**. Không dùng R50 score làm ground truth duy nhất; bất đồng, reference không đúng một mặt, ảnh mơ hồ hoặc box không ổn định → `AMBIGUOUS`, loại khỏi **mẫu số chấm target** nhưng vẫn báo trong 64 cảnh đã audit. Nếu người mục tiêu nhìn thấy nhưng không nằm trong box B0, ghi riêng `TARGET_MISSED_BY_DETECTOR` trong audit denominator; không âm thầm tính là S4 sai hoặc xóa khỏi báo cáo. Không thử R50 làm S4 candidate trên bộ nhãn này.

Split theo **identity folder đã biết**; người nền trong ảnh XQLFW không có nhãn danh tính đầy đủ, nên không thể chứng minh mọi người trong scene đều disjoint. Bước self-confirm có thể chọn thiên về ảnh dễ cho encoder dù dùng R50 khác MBF; mọi kết luận phải ghi giới hạn này. Không có người gán nhãn độc lập. Tập present/absent nhân tạo có tỷ lệ 1:1, không đại diện tần suất ở cửa phòng.

## 4. Tối ưu `τ,δ` chỉ trên development

Để không chọn một ngưỡng tùy ý rồi biện minh, T-015 sẽ tìm trên **toàn bộ các vùng quyết định khác nhau** của development: với `τ`, lấy `−∞`, `+∞` và trung điểm giữa các giá trị top-score MBF khác nhau; với `δ`, lấy `0`, `+∞` và trung điểm giữa các gap `s1−s2` khác nhau. Cùng một vùng cho cùng outcome trên development. Với tối đa 64 scene và hai reference/scene, mỗi trục có nhiều nhất 130 mốc, nên **tối đa 16.900 cấu hình**; duyệt hết, không dừng sớm, ghi số thực tế. Đây là tìm kiếm vét cạn tái lập được trên hai biến quyết định, không chọn PSO/GA chỉ để có tên thuật toán. Search chạy **offline trên development**; lúc inference P2 chỉ tính score các mặt, so hai điều kiện và có thể abstain. Không train/fine-tune model.

**Quy tắc chọn cấu hình:** trong các cấu hình có **0 wrong-target present** và **0 false selection absent** trên development, chọn cấu hình có nhiều correct-target present nhất; nếu hòa, chọn `τ` cao hơn rồi `δ` cao hơn. Cấu hình all-abstain luôn khả thi; nếu tối ưu chỉ cho all-abstain thì báo P2 không tạo lợi ích trong protocol này, không nới ràng buộc sau khi xem evaluation. Ràng buộc “0 lỗi trên development” là cách chọn bảo thủ cho phép thử, **không** là bảo đảm an toàn hay ngưỡng nghiệp vụ. Khóa `τ,δ`, code/hash và manifest nhãn rồi mới mở evaluation. Báo thêm đường đánh đổi correct/wrong/unresolved của development, nhưng chỉ cấu hình đã khóa được gọi là P2 trong kết luận evaluation.

## 5. Metric, điều kiện so và tiêu chí dừng

Đơn vị chấm là **scene + reference đã self-confirm**, không phải lượt thí sinh thực tế. Tính trên cùng input/nhãn cho A0, P1, P2:

| Nhóm | Mẫu số và outcome bắt buộc |
|---|---|
| Target-present nhiều mặt | `Np` ca hợp lệ: `correct target / wrong target / unresolved`; báo cả `correct/Np`, `wrong/Np`, `wrong/selected` khi selected >0. |
| Target-absent nhiều mặt | `Na` ca hợp lệ: `no face selected / false selection`; không gọi `no face selected` là xác nhận vắng thi. |
| Audit/coverage | Trong 64 scene dự kiến mỗi split: số multi thật, extra detection, visual ambiguous, metadata/reference/embedding conflict, số self-confirm present và absent. Không giấu ca bị loại để làm đẹp kết quả. |
| Chi phí | Median/p95 decode+detect, embedding từng face và quyết định S4 trên **cùng CPU runner**, ghi số mặt/scene, phiên bản mã/model/thiết bị và điều kiện cache. Không so thời gian này với run cũ khác tải máy. |

B0/A0 trên mọi scene nhiều detection trả `UNRESOLVED`; P1 kiểm mức rủi ro của ép chọn; P2 đo lợi ích/đánh đổi khi abstain. Report số đếm thô trước tỷ lệ, thêm Wilson 95% cho tỷ lệ từng nhóm; không gộp present và absent thành “accuracy hệ thống”. Với hai reference trên cùng scene, nếu ước lượng chênh lệch tổng hợp dùng bootstrap **theo scene**, không coi 2 dòng độc lập. Downstream S8 match/non-match/unresolved và FA/FR chỉ là phân tích thứ cấp với ngưỡng 1:1 khóa từ development, không trộn vào metric chọn mặt S4.

**Điều kiện để gọi là phép so định lượng có ích:** evaluation có ít nhất **30 present và 30 absent self-confirm** sau khi audit 64 scene; đây là mức mẫu tối thiểu nghiên cứu để tránh kết luận từ vài ảnh, không phải yêu cầu nghiệp vụ hay bảo đảm độ chính xác. Nếu thiếu, vẫn báo số thật nhưng gọi exploratory và dừng quyết định model/threshold; muốn tăng mẫu phải lập protocol revision **trước** khi xem thêm score. Dừng hoặc ghi `not runnable` nếu hash nguồn khác, identity giao nhau, nhãn/audit chưa khóa trước MBF candidate, R50 audit không tái lập, hoặc điều kiện B0/proposed khác ngoài S4. Không đặt ngưỡng latency hay false-select “đạt nghiệp vụ” khi chưa có policy/thiết bị đích.

## 6. Việc T-015/T-016 nhận từ protocol

T-015 tạo manifest 64 scene/split, self-confirm bằng nguồn + ảnh + R50 theo đúng quy tắc, khóa nhãn, rồi chạy A0/P1/P2. Kết quả ghi seed, SHA, phiên bản mã, CPU, các ca loại, cấu hình chọn trên development, score/outcome evaluation và sai khác protocol; ảnh/embedding/identity không lên Git. T-016 so paired, phân tích ca sai, trade-off và chi phí. **T-014 chưa kết luận P2 tốt hơn B0 hoặc dùng được ở cửa phòng.**
