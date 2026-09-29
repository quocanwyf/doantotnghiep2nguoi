# T-021 — Yêu cầu rủi ro và giao thức kiểm S8 sau S4

**Ngày:** 2026-09-29. **Người phụ trách:** Quốc An. **Trạng thái:** thiết kế nghiên cứu; chưa chọn ngưỡng S8 mới, model mới hoặc cấu hình triển khai. **Nguồn:** [T-008 FR-006/007/009, RISK-001/002](../01-problem/T-008-requirements.md) → [T-017](T-017-clean-confirmation.md) → [T-020](T-020-s4-s8-integration.md). Chỉ dùng dữ liệu có sẵn, không thu ảnh/video mới.

## Vì sao cần T-021

Người đến cửa phòng khai một hồ sơ → S4 chọn mặt ứng viên trong cảnh có thể nhiều người → S8 phải xác minh mặt đó có đủ bằng chứng khớp hồ sơ không. T-020 thấy **2/41 target-absent trial proxy** bị P2 chọn sai và S8 vẫn accept. S4 và S8 dùng cùng cosine, với ngưỡng S8 thấp hơn điều kiện P2 chọn. Vì vậy bước sau phải đặt rủi ro cần kiểm và dựng phép đo S8 trên *những mặt S4 thực sự chuyển sang*, bên cạnh phép đo cặp ảnh 1:1 thông thường.

S4 chỉ trả `SELECTED_FACE` hoặc `UNRESOLVED`; S8 nhận mặt đã chọn và reference của hồ sơ, trả `MATCH`, `NO_MATCH` hoặc `UNRESOLVED/UNAVAILABLE`. `MATCH` là tín hiệu kỹ thuật, **không tự ghi check-in, cấp quyền vào phòng hoặc kết luận attendance**. S4 unresolved không ép một box vào S8; app có thể retry, hướng dẫn đứng một mình hoặc chuyển người có quyền kiểm thủ công. `NO_MATCH` cũng không phải quyết định loại thí sinh cuối cùng.

## Yêu cầu rủi ro và mẫu số

| Lỗi | Cần báo | Hệ quả |
|---|---|---|
| Sai người vẫn được accept | `S4 chọn sai/target vắng + S8 MATCH`, trên tất cả trial và trên riêng các impostor đã được S4 chọn | RISK-001: có thể gây ghi nhận sai nếu app trao quyền quá mức; ưu tiên kiểm trước |
| Đúng người bị reject | `S4 chọn đúng + S8 NO_MATCH` | RISK-002: retry/review và tăng hàng chờ |
| Không kết luận | `S4 unresolved` hoặc `S8 unavailable/uncertain` | Fallback; không đưa vào mẫu số FMR/FNMR của các trial đã thực sự tới S8 |

**Quốc An xác nhận 2026-09-29:** chưa có mức false accept tối đa cho bản demo. Mức rủi ro số `α`, độ tin cậy, genuine accept tối thiểu, quyền tự động hóa và giới hạn review đều **TBD**; không tự đặt 1%, 0,1% hoặc một ngưỡng cosine. Hiện chỉ được thiết kế rule và phơi trade-off, không tuyên bố đáp ứng tiêu chí triển khai.

1. **S8 1:1 thông thường:** positive pair cùng identity, negative pair khác identity; báo genuine accept/reject, impostor reject/accept, FMR = impostor accept / impostor pair hợp lệ, FNMR = genuine reject / genuine pair hợp lệ. Báo ảnh/pair bị loại và lý do. Đây là định nghĩa đo verification theo [NIST FRTE 1:1](https://pages.nist.gov/frvt/html/frvt11.html), không thay bằng accuracy gộp.
2. **S8 có điều kiện sau S4:** giữ P2 và tham số T-017. Positive là box P2 chọn đúng identity; hard negative là box P2 chọn nhưng **khác identity hồ sơ**. Báo hard-negative accept/reject, genuine accept/reject, và trên mọi trial target-present/absent báo correct accept, wrong accept, reject, unresolved. Mẫu số `impostor đã đến S8` khác mẫu số `mọi trial absent`; không trộn chúng.
3. Tách một mặt/nhiều mặt **nếu thực sự có cả hai nhóm**, chất lượng/detector error, loại negative thường/hard và các ca unresolved. Raw theo sample, hash và khoảng bất định phải được lưu ngoài Git. `0/n` với `n` nhỏ không chứng minh rủi ro thấp.

## Dữ liệu mới từ nguồn sẵn có

| Tập | Mục đích và cách khóa |
|---|---|
| Development pair | XQLFW pair cùng/khác identity, tách identity; dùng cùng detector/encoder/preprocessing. Pair không đúng một mặt giữ lý do loại. Không lấy ngưỡng cân bằng T-020 làm mục tiêu rủi ro. |
| Development scene | Chọn scene/reference bằng seed và metadata **trước score**. Điểm target trên ảnh gốc rồi nối detector box; metadata nguồn + nhìn ảnh nhất quán; model khác chỉ cross-check phụ. Hard negative là mọi box sai mà P2 cố định chọn, không cherry-pick lỗi S8. `AMBIGUOUS` không ép nhãn. |
| Evaluation pair + scene | Identity nguồn tách development và loại identity pilot/T-015/T-017; manifest, nhãn, điều kiện loại sample khóa trước score; chỉ chạy sau khi ngưỡng/cấu hình khóa. Không xem kết quả rồi chỉnh threshold, nhãn hoặc P2. |

**Kiểm kê metadata, chưa phải tập thử:** sau khi loại các identity nguồn trong manifest T-015/T-017, split T-014 còn **2.481 identity development** với 3.162 pair tiềm năng (1.817 genuine/1.345 impostor) và 2.929 ảnh scene-order; **875 identity evaluation** với 613 pair (434/179) và 723 ảnh scene-order. Chưa lọc detector hoặc audit nhãn nhiều mặt. T-015 development có 0/37 absent được P2 chọn vì P2 đã tune ở đó; không dùng con số đó để khẳng định S8 chặn hard negative. Phân bố pair/identity nguồn không tương đương trial độc lập; cần báo lại mẫu số sau audit.

XQLFW không gán đầy đủ identity mọi người nền trong cảnh. Absent chỉ vào mẫu số impostor khi nhãn nguồn và audit có căn cứ đủ chắc; còn lại `AMBIGUOUS`. Nếu nguồn sẵn có không tạo đủ hard negative đáng tin, báo **không đủ dữ liệu để chốt ngưỡng tự động**. Có thể nghiên cứu nguồn công khai có box–identity rõ hơn hoặc bộ kiểm soát từ ảnh có identity đã biết, nhưng phải tách domain gap và quyền dùng; không biến proxy thành lượt check-in thực.

## Rule ngưỡng và evaluation

1. Trước khi xem score evaluation, nhóm/chủ sở hữu nghiệp vụ xác định `α` tối đa cho **false accept sau S4**, độ tin cậy thống kê và AI được phép gợi ý hay tự động xử lý. Nếu `α=TBD`, chỉ được báo trade-off development; **không chọn ngưỡng số mới hoặc mở evaluation để lựa theo kết quả**.
2. Khi có `α`, trên development chọn ngưỡng mà **giới hạn trên một phía** của FMR (ở độ tin cậy đã chốt) không vượt `α` cho cả negative thông thường lẫn hard negative có điều kiện sau S4; phải tính việc nhiều trial có thể cùng scene/identity. Trong các ngưỡng đủ điều kiện, ưu tiên genuine accept cao hơn, hòa thì ngưỡng cao hơn. Báo FNMR và unresolved tương ứng. Nếu mẫu ít khiến giới hạn bất định không chứng minh được `α`, hoặc không ngưỡng nào giữ được genuine utility cần thiết, kết luận **không có ngưỡng đủ căn cứ**, không tự nới `α`.
3. Khóa seed, manifest, nhãn, source/model hashes, code và ngưỡng trên development. Evaluation chạy **một lần** cùng điều kiện. Không dùng T-017/T-020 holdout để chọn cấu hình mới; nếu thay phương pháp, mở protocol/holdout mới.

NIST báo FNMR tại một mức FMR đã chọn vì hai loại lỗi đổi theo ngưỡng; mức FMR của NIST **không phải yêu cầu của kỳ thi này** ([NIST FRTE 1:1](https://pages.nist.gov/frvt/html/frvt11.html)). Điểm quan trọng ở đây là negative thông thường có thể dễ hơn negative **đã được S4 chọn do score cao**.

## Dependency và quyết định hiện tại

Nếu P2 chọn khi cosine `s ≥ τ` và gap `≥ δ`, còn S8 accept khi **cùng** `s ≥ θ`, thì sau P2: `accept ⇔ s ≥ max(τ, θ)` và gap `≥ δ`. T-020 có `θ=0,122254 < τ=0,147897`, nên S8 **không thể chặn** box P2 đã chọn. Nếu sau này `θ>τ`, S8 có thể chặn vài box nhưng vẫn là cùng tín hiệu, **không là hàng rào nhận dạng độc lập**; phải đo hard-negative accept và genuine reject trên tập mới. Hai threshold không tự tạo hai bằng chứng.

Các hướng *để thử sau khi có evidence*: cùng encoder với operating point chọn theo rủi ro có điều kiện; một tín hiệu xác minh khác nếu dữ liệu/compute cho phép; hoặc giữ abstain + người xử lý. Chưa chọn model/architecture mới. Nếu cùng encoder không có operating point đáp ứng rủi ro và coverage, mới có căn cứ nghiên cứu thiết kế S8 khác.

**Kết luận T-021:** rủi ro ưu tiên là `S4 chọn sai → S8 accept`; threshold S8 nên chọn theo giới hạn false accept định trước trên **hard negatives sau S4**, rồi báo đổi lại FNMR/unresolved. Cấu hình T-020 không tạo lớp chặn độc lập. Giữ S8 hiện tại làm **mốc nghiên cứu/app tham chiếu**, chưa chốt ngưỡng hoặc tự động accept. Bước kế tiếp là audit/khóa tập thử mới từ nguồn sẵn có và xác nhận `α`/authority; chỉ sau đó mới chạy phép chọn ngưỡng development và một lượt evaluation.
