# T-006 — Khảo sát dữ liệu, baseline và điểm tối ưu của Minh Hy

- **Ngày khảo sát:** 2026-09-24.
- **Task:** [T-006 trên Sheet](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0); Minh Hy thực hiện, Quốc An review.
- **Trạng thái:** phương án khảo sát độc lập để so sánh ở T-007, **chưa phải quyết định của nhóm hay xác nhận của thầy**. Trên Sheet, T-004 chọn use case vẫn chưa hoàn tất. Vì người dùng yêu cầu khảo sát T-006 ngay, tài liệu này lấy [use case A do Minh Hy đề xuất](../01-problem/minh-hy-proposal.md) làm **giả định làm việc**: từng người chủ động check-in trước camera điện thoại, hệ thống nhận dạng 1:N có quyền từ chối. Nếu T-004 chọn ảnh toàn lớp, phải khảo sát lại kích thước mặt, detector, dữ liệu và tiêu chí thời gian.

## 1. Câu hỏi nghiên cứu và phạm vi

**Câu hỏi có thể kiểm chứng:** Giữ nguyên detector SCRFD-500MF, trọng số nhận dạng MBF và danh sách đăng ký, việc tìm một chính sách crop/căn chỉnh khuôn mặt bằng thuật toán tối ưu có giảm **FNIR** ở cùng mức **FPIR** và trong giới hạn thời gian xử lý của điện thoại so với căn chỉnh chuẩn hay không; giảm bao nhiêu trên tập test chưa dùng để chọn chính sách?

Đây là **tối ưu đầu vào của model nhận dạng**, tức cải thiện pipeline dùng model; không được diễn giải là trọng số MBF đã được huấn luyện tốt hơn. Nếu ảnh pilot cho thấy crop chuẩn đã đúng nhưng embedding vẫn thất bại, hướng dự phòng là tìm tham số fine-tune MobileFaceNet. Chỉ chọn một hướng chính sau khi chẩn đoán lỗi và biết quyền dùng dữ liệu, GPU, điện thoại mục tiêu. Việc tìm crop/căn chỉnh đã có tiền lệ trong [Searching for Alignment in Face Recognition](https://arxiv.org/abs/2102.05447); đóng góp khả dĩ của nhóm là thiết kế và kiểm chứng chính sách cho quy trình điểm danh 1:N trên điện thoại, **không tuyên bố phát minh phép tìm alignment**.

## 2. Dữ liệu cần có trước khi chọn dataset

| Nhóm dữ liệu | Thông tin tối thiểu | Vai trò và điều không được suy diễn |
| --- | --- | --- |
| Ảnh đăng ký của người đồng ý tham gia | Mã giả danh, mã buổi, thiết bị, ảnh gốc, nhãn danh tính, kết quả phát hiện 5 mốc mặt. | Tạo gallery của phiên; ảnh đăng ký **không** là lượt test. Không cần đưa tên thật vào tập nghiên cứu. |
| Lượt check-in của người trong gallery | Nhãn người thực, phiên, thời điểm/buổi chụp, điều kiện sáng/góc/khoảng cách, box và 5 mốc mặt, kết quả hệ thống. | Đo FNIR, nhận nhầm người khác trong gallery, lỗi ghi điểm danh và thời gian. Cần cả lượt lỗi, không chỉ ảnh được model nhận. |
| Lượt của người ngoài gallery | Danh tính giả danh khác gallery, buổi chụp và điều kiện tương ứng. | Đo FPIR; không dùng ảnh của chính người đó để đăng ký trong cùng phép thử. |
| Nhãn kiểm tra detector/crop | Box hoặc mốc do người kiểm tra gán cho tập pilot và một phần test, cờ mặt bị che/mờ/nhỏ. | Phân biệt lỗi không phát hiện, lỗi mốc/crop và lỗi embedding. Nếu detector không tìm được mặt, thay ROI sau detector không thể cứu lượt đó. |

**Giao thức tách dữ liệu đề xuất:** E = ảnh đăng ký ở buổi A; C = lượt hiệu chỉnh ngưỡng ở buổi B; V = lượt chọn chính sách ở buổi C; T = test khóa ở buổi D, khác buổi/ngày nếu có thể. Các tập C/V/T không chứa các khung hình gần kề cùng một lượt quay. Danh tính người đã đăng ký xuất hiện ở E và các lượt check-in theo đúng bài toán 1:N; **buổi chụp** phải tách để tránh đánh giá trên ảnh gần như trùng. Danh tính người ngoài gallery cần được ghi riêng và trải qua nhiều buổi; không đưa người ngoài gallery trong T vào bước chọn chính sách/ngưỡng. Nếu quy mô thu ảnh không đủ bốn buổi, có thể dùng chia theo buổi và lặp nhiều fold trong phát triển, nhưng vẫn phải khóa một test độc lập. Chốt quy tắc chia trước khi xem T.

### Nguồn dữ liệu và quyền dùng

| Nguồn | Có thể dùng cho | Quyền dùng và giới hạn cần kiểm tra |
| --- | --- | --- |
| Ảnh nhóm tự thu với người tham gia đồng ý | **Nguồn bắt buộc để đánh giá cuối** trong đúng camera/quy trình check-in; E/C/V/T; có thể làm dữ liệu fine-tune nếu người tham gia đồng ý rõ. | Cần xác định mục đích nghiên cứu, phạm vi người truy cập, thời gian giữ/xóa ảnh và embedding, quyền rút lại, cách trình bày ảnh trong báo cáo. Chưa có sự đồng ý/ảnh thật nào được xác nhận. Không commit ảnh, nhãn danh tính, embedding hay link riêng vào Git. |
| [InsightFace `buffalo_sc`](https://github.com/deepinsight/insightface/blob/master/python-package/docs/model_zoo.md) | **Trọng số baseline/prototype**, gồm SCRFD-500MF và `MBF@WebFace600K`; gói công bố 16 MB, không có module thuộc tính 2d106/3d68. | Theo model zoo, **mã thư viện MIT nhưng trọng số pretrained chỉ dành cho nghiên cứu phi thương mại**. Phải xác minh điều khoản tại lúc tải và quyền dùng trong demo. `MBF@WebFace600K` là model đã huấn luyện trước, **không** được gọi là model nhóm huấn luyện trên DigiFace. Gói không tự chứng minh thời gian chạy trên điện thoại của nhóm. |
| [DigiFace-1M](https://github.com/microsoft/DigiFace1M) | Ứng viên **huấn luyện/fine-tune trong nhánh dự phòng**, không cần tải nếu chỉ thử ROI trên trọng số cố định. | Khoảng 720 nghìn ảnh/10 nghìn danh tính với 72 ảnh/người và 500 nghìn ảnh/100 nghìn danh tính với 5 ảnh/người; [R-UDA](https://github.com/microsoft/DigiFace1M/blob/main/LICENSE) giới hạn dùng tính toán cho nghiên cứu phi thương mại. Ảnh tổng hợp không thay test ảnh thật: [bài báo gốc](https://openaccess.thecvf.com/content/WACV2023/html/Bae_DigiFace-1M_1_Million_Digital_Face_Images_for_Face_Recognition_WACV_2023_paper.html) thảo luận khoảng cách tổng hợp–thật và tác động của augmentation/fine-tune. Xác minh tải được, dung lượng và GPU trước khi chọn. |
| [WIDER FACE](https://shuoyang1213.me/WIDERFACE/) | Chẩn đoán detector nếu pilot cho thấy mặt bị bỏ sót, nhất là khi T-004 chọn ảnh nhiều người. | Là benchmark phát hiện mặt có nhãn box, không có nhãn danh tính để đo điểm danh. Trang dự án ghi giấy phép CC BY-NC-ND; phải kiểm tra điều khoản trước khi tải/dùng. |
| [LFW](https://web.cs.umass.edu/publication/docs/2014/UM-CS-2014-003.pdf) | Kiểm tra bổ trợ việc triển khai xác minh cặp ảnh. | Giao thức cặp ảnh không đại diện cho tìm kiếm 1:N, quyền từ chối và điều kiện camera lớp; không dùng điểm LFW làm kết quả thành công của đồ án. Xác minh quyền truy cập/sử dụng cụ thể trước khi tải. |

**Ưu tiên chọn nguồn:** nếu chỉ kiểm tra ROI, dùng gói pretrained hợp lệ và ảnh tự thu cho E/C/V/T; DigiFace-1M là nguồn dự phòng cho nghiên cứu thay đổi trọng số. [VGGFace2 hiện không cung cấp đường tải dataset trên trang chính thức](https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/), nên không xây kế hoạch phụ thuộc vào đó. Dataset huấn luyện đã dùng cho trọng số `MBF@WebFace600K` không phải dữ liệu của nhóm; cần ghi rõ tính phụ thuộc đó trong báo cáo.

**Quy mô mẫu:** số người/lượt chỉ chốt sau khi kiểm tra khả năng thu. Nếu muốn tuyên bố FPIR < 1% với 95% tin cậy một phía và quan sát 0 lần nhận nhầm, cần khoảng **299 lượt âm độc lập** (`1 - 0,05^(1/n) < 0,01`); nhiều lượt từ cùng một người/buổi có tương quan nên thực tế cần thiết kế nhiều người và nhiều buổi. Khi chưa đủ mẫu, ghi số lỗi/tổng lượt và khoảng tin cậy; không tuyên bố đạt ngưỡng 1%. Các ngưỡng 1%, 2 giây ở [T-003](../01-problem/minh-hy-proposal.md) chỉ là ví dụ thảo luận, chưa phải tiêu chí được chốt.

## 3. Một đến hai baseline khả thi

**B0 — pipeline chuẩn, không tìm chính sách:** lấy gói `buffalo_sc` (nếu quyền dùng phù hợp), cố định phiên bản/hash trọng số và input detector; SCRFD phát hiện mặt/5 mốc → [căn chỉnh chuẩn `norm_crop`](https://github.com/deepinsight/insightface/blob/master/python-package/insightface/utils/face_align.py) về kích thước mà ONNX recognizer yêu cầu → embedding chuẩn hóa L2 → cosine với gallery → top-1 nếu vượt ngưỡng, ngược lại từ chối. Trước thử nghiệm cần kiểm tra file detector tải về thực sự xuất 5 mốc; nếu không, không dùng cấu hình này như đã mô tả. Thực thi quy tắc đúng một mặt và ghi một lần cho mỗi mã phiên/người. Mã recognizer của InsightFace thực sự gọi `norm_crop` với `face.kps` trước khi lấy embedding, nên **box thô không phải baseline tương đương** ([mã nguồn](https://github.com/deepinsight/insightface/blob/master/python-package/insightface/model_zoo/arcface_onnx.py)). Ngưỡng chọn trên C và không sửa sau khi xem T.

**B1 — cùng pipeline, random search cùng ngân sách:** giữ nguyên detector/trọng số/giao thức; lấy ngẫu nhiên chính sách alignment trong **cùng search space và cùng số lần đánh giá** như proposed, chọn trên V. Đây là đối chứng để biết thuật toán tìm kiếm proposed có tốt hơn một cách tìm đơn giản hay chỉ được lợi vì đã thử nhiều cấu hình. [Random search là baseline có cơ sở cho tìm hyperparameter](https://jmlr.org/beta/papers/v13/bergstra12a.html). B1 chỉ chạy sau khi có C/V đủ dữ liệu; nếu chưa đủ, chỉ có B0 và chưa thể đánh giá đóng góp của thuật toán.

Hai baseline này dùng **cùng ảnh đăng ký, gallery, detector, recognizer, threshold-selection rule, thiết bị và code nghiệp vụ**. Khác biệt duy nhất giữa B0 và B1 là chính sách alignment. Mỗi phương án dùng ngưỡng riêng được **hiệu chỉnh trên cùng C theo cùng quy tắc** để so chất lượng ở một mức FPIR mục tiêu; không dùng một ngưỡng cosine cố định cho mọi crop rồi quy lỗi cho model.

## 4. Điểm cần tối ưu, lựa chọn thử và thuật toán

### Chẩn đoán trước khi đầu tư vào ROI

Trên pilot có nhãn, đếm riêng: (a) không phát hiện được mặt; (b) có mặt nhưng box/mốc/crop sai; (c) crop được người kiểm tra xác nhận đạt nhưng embedding vẫn sai hoặc điểm quá thấp. Thử thêm **crop mốc do người kiểm tra** trên cùng ảnh để ước lượng trần cải thiện mà alignment có thể mang lại. Nếu nhóm (b) hiếm hoặc crop chuẩn và crop kiểm tra cho kết quả gần nhau, **không chọn ROI làm đóng góp chính**. Nếu nhóm (a) chiếm ưu thế, nghiên cứu detector/input resolution; nếu nhóm (c) chiếm ưu thế, cân nhắc fine-tune/augmentation của recognizer. Đây là quy tắc quyết định dựa trên pilot, chưa có quan sát thật.

### Phương án chính để thử nếu ROI có dư địa

- **Biến quyết định:** `θ = (s, dx, dy)` với `s` là tỉ lệ khung alignment so với template chuẩn, `dx, dy` là dịch ngang/dọc theo tỉ lệ bề rộng đầu ra. Tìm trong miền thử sơ bộ `s ∈ [0,90; 1,10]`, `dx ∈ [-0,04; 0,04]`, `dy ∈ [-0,06; 0,06]`; **θ chuẩn = (1,0,0)**. Đây là phạm vi thăm dò, phải kiểm tra không cắt mất cấu trúc mặt hoặc tạo quá nhiều viền đen. Cùng θ áp dụng cho ảnh đăng ký và ảnh check-in; detector, 5 mốc, kích thước ảnh vào model và trọng số giữ nguyên. Không thay bằng resize box vuông không căn chỉnh.
- **Thuật toán ứng viên:** Bayesian optimization kiểu **TPE** ([bài báo thuật toán gốc](https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization)) để chọn θ từ các phép đo trên V. TPE phù hợp để khảo sát khi mỗi đánh giá phải chạy lại recognizer trên E/C/V; đây là đề xuất kỹ thuật, chưa phải quyết định. Chạy B1 random search với cùng miền, cùng ngân sách thử và các seed công bố. Nếu ngân sách rất nhỏ hoặc đáp ứng đủ bằng lưới thưa, báo thẳng rằng TPE không cho lợi thế.
- **Ngân sách thử dự kiến để ước lượng công việc:** một lượt B0; ví dụ 20–30 cấu hình cho TPE và đúng 20–30 cho random search; lặp seed tìm kiếm nếu khả thi. Đây **không phải** số lượt đã chạy hay ngân sách được duyệt. Có thể lưu kết quả detector và mốc sau khi chạy một lần, nhưng phải tính lại crop, embedding đăng ký và embedding lượt thử cho mỗi θ; không cache embedding của θ khác. Chi phí xấp xỉ số cấu hình × số ảnh E/C/V × một lần suy luận recognizer, cộng thời gian đo trên điện thoại.

### Phương án dự phòng nếu lỗi nằm ở embedding

Khảo sát MobileFaceNet với **cùng kiến trúc**, cùng detector/crop chuẩn và cùng dữ liệu huấn luyện được phép dùng. Baseline là cấu hình huấn luyện/fine-tune cố định có thể tái lập; proposed tìm một tập biến nhỏ như learning rate, weight decay và mức augmentation ảnh mờ/sáng. Dùng random search cùng ngân sách đối chứng với TPE; mục tiêu vẫn là FNIR tại FPIR mục tiêu, nhưng mỗi trial cần huấn luyện rồi đánh giá nên chi phí **số trial × thời gian train/fine-tune**. Không thể gọi việc đổi ngưỡng cosine hoặc đăng ký thêm embedding là fine-tune model. Nhánh này chỉ khả thi khi xác minh dữ liệu, giấy phép, trọng số khởi tạo và GPU; không so model tự train với pretrained `buffalo_sc` rồi quy toàn bộ chênh lệch cho optimization.

## 5. Hàm mục tiêu và cách đo “cải thiện bao nhiêu”

Gọi `α` là FPIR tối đa, `Tmax` là p95 latency tối đa do nhóm đặt **trước khi mở test**. Với mỗi θ, chọn ngưỡng `τ_C(θ)` trên C theo cùng một quy tắc, ví dụ ngưỡng thấp nhất có FPIR thực nghiệm trên C không vượt `α`; báo kèm khoảng tin cậy của ước lượng này. Trên V, coi θ **khả thi** khi `FPIR_V(θ,τ_C) ≤ α` và `p95_V(θ) ≤ Tmax`. **Hàm mục tiêu đề xuất:**

`θ* = argmin_{θ khả thi} FNIR_V(θ, τ_C(θ))`.

Nếu không có θ khả thi, **không âm thầm nới ràng buộc**: báo bảng đánh đổi FNIR–FPIR–latency và lý do chưa đạt. Trong pilot ít lượt âm, có thể dùng số lỗi thô để sàng lọc nhưng chưa kết luận FPIR đạt α. Cần chốt α/Tmax theo rủi ro nhận nhầm, cỡ mẫu và điện thoại thực tế; không giả vờ ngưỡng minh họa là yêu cầu của thầy.

**Đơn vị và định nghĩa đo:** mỗi lượt check-in theo kịch bản chụp đã khóa là một probe; không lọc bỏ lượt khó sau khi nhìn kết quả detector. `FPIR = số lượt người ngoài gallery bị gán bất kỳ người nào / tổng lượt người ngoài gallery`; `FNIR = số lượt người trong gallery không trả đúng danh tính trên ngưỡng / tổng lượt người trong gallery`, gồm không phát hiện mặt, từ chối và gán sai người. Báo riêng **tỷ lệ gán sai danh tính của người trong gallery**, tỷ lệ không phát hiện mặt, tỷ lệ ghi đúng người/đúng phiên, lượt xử lý thủ công và bản ghi trùng. Lượt nhiều mặt là lỗi điều kiện đầu vào theo use case A và được thống kê riêng theo quy tắc định trước. [NIST FRTE 1:N](https://pages.nist.gov/frvt/html/frvt1N.html) dùng FPIR/FNIR để đánh giá hệ thống nhận dạng mở có ngưỡng; báo cáo của nhóm phải ghi rõ định nghĩa, gallery size và quy tắc đếm của chính mình.

**So sánh trên T:** khóa θ và quy tắc chọn τ trước khi mở T. Chạy B0, B1 và proposed trên **chính các lượt T**, cùng gallery, cùng phiên bản detector/recognizer, cùng camera và thiết bị. Báo `ΔFNIR = FNIR_B0 - FNIR_proposed` và `ΔFNIR_vs_random = FNIR_B1 - FNIR_proposed` theo **điểm phần trăm**, mức thay đổi tương đối nếu mẫu đủ; báo song song `ΔFPIR`, `Δp95`, số nhận sai thô và chi phí tìm kiếm. Vẽ/ghi nhiều điểm ngưỡng nếu có đủ dữ liệu; tránh chọn ngưỡng trên T để làm đẹp kết quả. Tách kết quả theo sáng/tối, mờ, khoảng cách và buổi chụp nếu số mẫu cho phép.

**Độ bất định và tái lập:** ghi số người, số buổi, số probe và số lỗi trong từng nhóm; khoảng tin cậy cho tỷ lệ và khoảng tin cậy của **chênh lệch ghép cặp** (bootstrap theo người/buổi, không coi khung hình liền nhau là độc lập). Với random search/TPE, công bố các seed và phân bố kết quả qua nhiều lần chạy; chọn một chính sách theo V rồi đo T một lần. Ghi mã commit, phiên bản ONNX/runtime, hash trọng số, kích thước gallery, tham số detector, điện thoại/CPU hoặc GPU, warm-up, số lần đo và p50/p95 từ camera đến kết quả. Benchmark của tác giả model không được điền vào bảng kết quả của nhóm.

**Bảng kết quả sẽ điền sau thực nghiệm** (để trống số thay vì dự đoán):

| Phiên bản | FNIR @ quy tắc FPIR đã chọn | FPIR (lỗi/tổng lượt âm) | Gán sai người trong gallery | Điểm danh đúng | p95 toàn pipeline | Thử nghiệm/chi phí tìm kiếm |
| --- | --- | --- | --- | --- | --- | --- |
| B0 `norm_crop` chuẩn | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo | 0 trial tìm kiếm |
| B1 random search | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa chạy |
| Proposed TPE alignment | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa đo | Chưa chạy |

## 6. Ước lượng khả thi, rủi ro và điểm cần chốt

| Hạng mục | Kiểm tra trước khi bắt đầu | Hệ quả nếu không đạt |
| --- | --- | --- |
| Quyền dùng model và dữ liệu | Xác nhận demo nghiên cứu phi thương mại, điều khoản tải `buffalo_sc`, đồng ý thu/lưu/xóa dữ liệu người thật. | Chọn trọng số/dữ liệu có quyền dùng phù hợp; không sử dụng dữ liệu nhạy cảm khi chưa có căn cứ. |
| Số người, nhiều buổi, người ngoài gallery | Kiểm kê thực tế số người và lượt âm có thể thu; lập kế hoạch C/V/T trước. | Nếu ít mẫu, chỉ kết luận pilot, không khẳng định cải thiện FPIR thấp hoặc độ tin cậy cao. |
| Dư địa ROI | So lỗi (a)/(b)/(c) và thử crop do người kiểm tra trên pilot. | Nếu ROI không cứu được lỗi chính, chuyển khảo sát sang recognizer hoặc detector; không chạy TPE chỉ để có tên thuật toán. |
| Khả năng chạy mobile | Xác định điện thoại, runtime ONNX, tốc độ detector + recognizer + xử lý nghiệp vụ thực tế. | Nếu vượt thời gian, thu hẹp search space/chính sách hoặc xem lại model; không dùng benchmark máy khác để kết luận. |
| Tính mới và đối chứng | Đối chiếu [FAPS](https://arxiv.org/abs/2102.05447), so B0/B1 công bằng, tách tác động crop với ngưỡng và model. | Kết luận ở mức ứng dụng/thực nghiệm; không nhận một thủ thuật alignment đã công bố là đóng góp mới. |

**Việc phải thống nhất ở T-004/T-007:** use case một hay nhiều người; mục tiêu lỗi và thời gian; quyền thu dữ liệu; ngân sách GPU/thiết bị; ROI có được xem là phần optimization chính khi model không fine-tune hay thầy yêu cầu thay đổi trọng số; chọn baseline/dataset/thuật toán sau khi hai thành viên so sánh. Hiện không có quyết định kỹ thuật mới trong `../00-project/decisions/` và không có số liệu thực nghiệm của nhóm.
