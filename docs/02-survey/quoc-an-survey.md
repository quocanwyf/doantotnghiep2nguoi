# T-005 — Khảo sát kỹ thuật cho xác thực thí sinh tại cửa phòng thi

**Người đề xuất:** Quốc An. **Trạng thái:** khảo sát để chọn dữ liệu, baseline và hướng tối ưu; chưa phải kết quả benchmark. Quốc An cho biết T-004 đã chọn bối cảnh T-002, còn biên bản quyết định/Sheet cần đồng bộ. Các model và hướng tối ưu dưới đây là **ứng viên có điều kiện**, không tự coi là quyết định T-007.

## 1. Bài toán, phạm vi và câu hỏi nghiên cứu

Bối cảnh sản phẩm là kỳ thi có danh sách thí sinh, ảnh đăng ký, phòng/ca và giờ thi từ trước. Thiết bị ở cửa, ban đầu dự kiến là điện thoại, xử lý mỗi lượt thí sinh khai báo mã rồi đứng vào vùng camera. Nó cần xác minh mặt 1:1 với ảnh của mã đó, kiểm tra đúng phòng/ca/giờ, tránh ghi trùng và cập nhật danh sách có mặt. Mục tiêu dài hạn là giảm nhu cầu một người chuyên đứng kiểm tra đầu vào ở từng phòng; người có thẩm quyền vẫn xử lý ngoại lệ và làm các bước mà quy chế yêu cầu. Với kỳ thi tốt nghiệp THPT, [quy chế hiện công bố](https://vqa.moet.gov.vn/uploads/news/2024_12/final-quy-che-thi-tot-nghiep-thpt.pdf) vẫn quy định giám thị đối chiếu ảnh và giấy tờ; đồ án không được diễn giải kết quả kỹ thuật thành quyền bỏ bước đó.

**Phạm vi thực nghiệm T-005:** dùng **dataset công khai** để chọn và đánh giá pipeline nhận diện. Câu chuyện kỳ thi là bài toán thiết kế và bộ ràng buộc; đồ án này không dựa vào việc xin dữ liệu thí sinh thật, xin trường cho thử tại cửa hoặc chứng minh đã tiết kiệm nhân sự trong thực tế. Dùng dữ liệu công khai không biến nó thành dữ liệu thi: kết luận chỉ là tính khả thi kỹ thuật trên những điều kiện mà dataset có, không phải độ an toàn triển khai ở một kỳ thi cụ thể.

**Câu hỏi nghiên cứu:** với ảnh tham chiếu và chuỗi ảnh tại một điểm qua cửa, model/pipeline nào cho cân bằng tốt giữa lỗi xác minh, độ trễ và kích thước trên thiết bị dự kiến? Nếu pipeline gốc còn yếu, điểm yếu do phát hiện/căn chỉnh, chất lượng khung hình, embedding, ngưỡng hay giới hạn tính toán? Một phương pháp tối ưu có cải thiện điểm yếu đó **so với baseline mạnh và đối chứng đơn giản** không?

## 2. Đọc đúng định hướng từ file gốc

[File ghi chép dinhhuongdatn.docx](../sources/dinhhuongdatn.docx) gợi trình tự: chọn bài toán → chỉ ra chỗ pipeline chưa tốt → xác định biến tìm kiếm, hàm mục tiêu và ràng buộc → chọn thuật toán optimization → so baseline/proposed cùng điều kiện → báo cải thiện định lượng, cân nhắc mobile. Các ví dụ trong file gồm ROI/bounding box, chọn đặc trưng, hyperparameter, cấu trúc/kích thước model và đánh đổi độ chính xác–tốc độ; Jaya, HHO, PSO, GA, Bayesian Optimization chỉ là thuật toán ứng viên. File là **ghi chép do nhóm cung cấp**, không phải văn bản chứng minh thầy đã duyệt từng ý. Ghi chép có nhắc train/fine-tune; cần hỏi lại thầy đây có phải yêu cầu bắt buộc, vì hướng tối ưu ở inference có thể là nghiên cứu khác với tối ưu training.

Bởi vậy T-005 **không chọn một model yếu chỉ để dễ báo tăng điểm sau tối ưu**. Phải trả lời cả: model đó phù hợp mục tiêu hơn đối thủ ở điểm nào, điểm nào còn yếu, cải tiến giải quyết đúng điểm yếu ấy không, và kết quả cuối có còn cạnh tranh với pipeline tốt nhất chưa tối ưu không.

## 3. Quy tắc chọn dataset trước khi chọn model

Dataset được chọn theo **vai trò đo**, không cộng mọi ảnh vào một tập lớn. Tiêu chí sàng lọc: (a) có ảnh/chuỗi và nhãn danh tính để tạo cặp genuine–impostor 1:1; (b) có yếu tố gần bài toán như lối đi/camera cố định, nhiều khung, thay đổi góc/chất lượng; (c) có protocol và nguồn gốc rõ để tái lập; (d) tải được với dung lượng/thiết bị của đồ án; (e) quyền dùng cho nghiên cứu học thuật rõ. Không dùng dataset chỉ có bounding box để tuyên bố đo xác minh danh tính.

### D1 — ChokePoint: ứng viên **chính** cho nhận diện ở lối đi

[Trang gốc ChokePoint](https://arma.sourceforge.net/chokepoint/) và [bản phát hành Zenodo](https://zenodo.org/records/815657) mô tả camera ở các cổng, video nhiều khung với biến thiên tư thế, ánh sáng, độ nét và căn chỉnh; có ảnh/chuỗi gốc, nhãn và protocol xác minh G1/G2. Giấy phép cho nghiên cứu phi thương mại và yêu cầu dẫn nguồn/giữ thông báo giấy phép. Đây là lựa chọn gần nhất trong các tập đã khảo sát với tình huống “camera ở điểm qua cửa”, nên được ưu tiên **nếu kiểm tra file và mapping ảnh tham chiếu thành công**. Có thể bắt đầu bằng một số chuỗi gốc và protocol một camera để giới hạn dung lượng; không dùng crop sẵn khi đang đánh giá detector/căn chỉnh. Ảnh still của cùng người có thể làm ảnh tham chiếu nếu mapping và điều kiện thu phù hợp; nếu không, chọn ảnh từ phiên khác làm **proxy** và ghi rõ khác ảnh đăng ký trước kỳ thi.

**Giới hạn quan trọng:** tập chỉ có 25/29 người ở hai cổng, phần lớn khung hình có một người; hai chuỗi đông người có che khuất nhưng không thay thế được dataset được gắn nhãn nhiều mặt cùng tranh vùng làm thủ tục. Không dùng D1 để tuyên bố giải quyết chắc chắn việc chọn đúng thí sinh giữa đám đông, ước lượng lỗi cực hiếm hay tổng quát cho người Việt. Dataset khoảng 12 GB nếu tải toàn bộ; phương án lấy phần cần thiết phải ghi manifest và không phá protocol.

### D2 — XQLFW: kiểm tra xác minh khi ảnh tham chiếu và ảnh chụp chênh chất lượng

[Nhóm tác giả XQLFW](https://martlgap.github.io/xqlfw/) cung cấp giao thức 3.000 cặp cùng người và 3.000 cặp khác người, nhấn vào chênh lệch chất lượng/độ phân giải. Nó giúp hỏi model nào bền hơn khi ảnh ở cửa kém ảnh hồ sơ, và liệu hướng chọn khung theo chất lượng có lý do. **Không dùng làm tập chính cho video, chọn mặt trong cảnh hoặc thời gian qua cửa**, vì đây là benchmark cặp ảnh. Cần xác nhận điều kiện sử dụng **ảnh** ở trang tải; giấy phép MIT của mã đánh giá không tự là giấy phép của ảnh.

### D3 — CPLFW hoặc CFP-FP: kiểm tra nhạy với góc mặt

[CPLFW của nhóm tác giả](https://www.whdeng.cn/CPLFW/index.html) tập trung vào cặp khác tư thế; [CFP-FP](http://www.cfpw.io/) là đối chiếu frontal–profile nếu trang/dữ liệu còn truy cập được. Chỉ chọn **một** tập pose sau kiểm tra quyền dùng và file protocol để tránh thêm benchmark vì số lượng. Chúng giúp giải thích lỗi do thí sinh quay mặt, nhưng không mô phỏng trọn luồng cửa phòng. Nếu không truy cập được nguồn chính thức/điều khoản, bỏ tập đó thay vì lấy bản sao không rõ nguồn.

### D4 — WIDER FACE: chỉ đo phát hiện mặt khi cần

[WIDER FACE](https://shuoyang1213.me/WIDERFACE/) có nhiều mặt, kích thước và che khuất, giấy phép công bố CC BY-NC-ND. Nó hữu ích nếu phải so detector hoặc kiểm tra recall với mặt nhỏ/đông. Nó **không có giao thức mã khai báo + ảnh tham chiếu + sự kiện vào phòng**, nên không tính vào kết quả xác minh đầu-cuối. Việc dùng/biến đổi/công bố ảnh phải theo điều khoản dataset; không đưa ảnh vào Git.

### Dataset không chọn làm trụ chính

[LFW](https://vis-www.cs.umass.edu/lfw/) là phép thử sanity cho cặp ảnh quen thuộc; điểm cao trên LFW không trả lời tình huống ảnh qua cửa khác chất lượng. [IJB-C](https://www.nist.gov/itl/tted/btg/ijb-c-dataset-request-form) có thử thách rộng hơn nhưng NIST đã ngừng phân phối từ 14/03/2023, nên không đặt làm điều kiện bắt buộc. Tập ảnh thi thật hoặc tập tự thu tại trường **không nằm trong kế hoạch dữ liệu của đồ án này**. Dữ liệu chống giả mạo không đưa vào ma trận chọn hướng tối ưu nhận diện.

**Kết luận dataset ở mức khảo sát:** thử D1 làm tập chính; D2 kiểm tra cross-quality; chọn thêm D3 nếu lỗi pose nổi bật; D4 chỉ khi hướng nghiên cứu chạm detector. Đây là lựa chọn có lý do, chưa phải xác nhận đã tải/kiểm tra đủ file và giấy phép từng bộ.

## 4. Model ứng viên và câu hỏi “sao không dùng model tốt hơn luôn?”

Trước khi so, cố định **tên file trọng số và phiên bản**, detector, bước căn chỉnh, kích thước đầu vào, màu kênh, điểm similarity, runtime. “ArcFace” là một phương pháp học/loss, không đủ để định danh một model; “MobileFaceNet” chỉ là kiến trúc. Báo rõ training source và điều khoản của **trọng số**, không suy từ giấy phép thư viện.

- **M0 — YuNet + SFace (OpenCV Zoo):** [YuNet](https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/README.md) phát hiện mặt và landmark; [SFace](https://github.com/opencv/opencv_zoo/blob/main/models/face_recognition_sface/README.md) tạo embedding, có ví dụ tích hợp chính thức. Ưu điểm khảo sát: pipeline gọn, dễ tái lập và hợp để thử trên thiết bị hạn chế. Điểm cần kiểm chứng: accuracy trên D1/D2, tốc độ máy nhóm, nguồn huấn luyện của trọng số và khả năng chuyển sang sản phẩm. Dùng bản model được pin/hash, không để cập nhật tự đổi baseline.
- **M1 — InsightFace buffalo_sc:** [model zoo chính thức](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md) ghi SCRFD-500MF + MobileFaceNet, gói khoảng 16 MB. Đây là **đối thủ cùng nhóm gọn**; nếu M1 vừa chính xác hơn vừa nhanh/gọn hơn M0 theo cùng phép đo, không có cơ sở chọn M0 làm pipeline cuối chỉ để tối ưu cho thấy tăng điểm. Trọng số InsightFace công bố cho nghiên cứu phi thương mại; dùng để làm đồ án được theo điều khoản, chưa chuyển nguyên model sang startup.
- **M2 — InsightFace buffalo_l:** model zoo ghi SCRFD-10GF + ResNet50, gói khoảng 326 MB. Đây là **đối chứng mạnh về chất lượng** và giúp biết đổi sang model lớn giải quyết bao nhiêu lỗi; phải đo thật trên dữ liệu/thiết bị đang dùng, không lấy bảng accuracy công bố ở dataset khác làm kết luận. Nếu M2 tốt hơn nhưng vượt giới hạn tốc độ/kích thước của điện thoại, M0/M1 vẫn có lý do tồn tại như nghiệm trên đường đánh đổi. Nếu M2 thỏa mọi ràng buộc và tốt hơn, không được lờ nó đi.
- **M3 tùy chọn — AdaFace R18:** [mã/trọng số tác giả](https://github.com/mk-minchul/AdaFace) cho một đối chiếu về ảnh chất lượng kém nếu D2 bộc lộ lỗi rõ; chi phí tích hợp/preprocess và quyền trọng số phải được rà. Chỉ thêm sau M0–M2 nếu nó trả lời câu hỏi mà ba phương án đầu chưa trả lời, không mở rộng danh sách model vô hạn.

**Tiêu chuẩn chọn model gốc:** không phải “accuracy cao nhất” đơn lẻ. Trước hết loại pipeline không chạy/không có quyền dùng nghiên cứu/không đạt yêu cầu tối thiểu được chốt. Trong các phương án còn lại, so lỗi xác minh ở cùng operating point, độ trễ p95, kích thước, RAM và độ ổn định qua D1/D2. Chọn một nghiệm Pareto phù hợp mục tiêu mobile làm baseline để tối ưu và **giữ model mạnh nhất làm đối chứng bên ngoài**. Nếu chọn model nhẹ B thay model mạnh A, tài liệu phải ghi rõ A tốt hơn bao nhiêu và B tiết kiệm bao nhiêu thời gian/bộ nhớ; proposed của B phải được so với **cả B gốc lẫn A**, tránh kết luận sai kiểu “B tăng điểm nên là tốt nhất”.

## 5. Pipeline gốc và hai tầng benchmark

**Pipeline nghiệp vụ mẫu:** mã khai báo → lấy một ảnh tham chiếu → frame camera → phát hiện mặt → chọn/căn chỉnh mặt → embedding → so 1:1 → vùng quyết định accept / chụp lại / xử lý thủ công → kiểm tra quy tắc phòng/ca/giờ/trùng lượt → nhật ký. Dataset công khai chỉ đo được các khâu mà nó có nhãn; quy tắc phòng/ca/giờ có thể kiểm tra bằng hồ sơ **giả lập không chứa danh tính thật**, và kết quả ấy không được gộp thành “face accuracy”.

**B0 — baseline đơn khung:** mỗi lượt/chuỗi dùng một khung theo quy tắc cố định trước; mỗi model chạy theo preprocess chính thức; ngưỡng similarity được chọn trên development set. Đây là điểm gốc để thấy lỗi do ảnh vào, model và ngưỡng.

**B1 — baseline nhiều khung đơn giản:** cùng model và tập lượt như B0, chọn khung rõ nhất bằng một quy tắc chất lượng công khai hoặc lấy trung bình embedding của số khung cố định. B1 là đối chứng bắt buộc nếu đề xuất tối ưu chọn khung/ghép embedding; nếu proposed chỉ hơn B0 mà không hơn B1 thì đóng góp tối ưu chưa thuyết phục.

**Tầng 1: chọn model** chạy M0–M2 trên D1 với cùng các lượt/cặp và điều kiện đo, rồi kiểm tra D2. Có thể so pipeline trọn bộ để quyết định sử dụng. Muốn giải thích vì sao score khác nhau, chạy thêm phép đối chiếu **cùng box/landmark đầu vào**, nhưng vẫn phải dùng alignment/input phù hợp từng recognizer; báo đây là phân tích thành phần, không đánh tráo thành so pipeline trọn bộ. Không so số similarity thô giữa model như cùng một thang.

**Tầng 2: tối ưu** cố định model đã chọn, cùng dữ liệu/split và chỉ thay thành phần được nghiên cứu. Nếu đổi cả detector, recognizer và logic chọn khung, không thể gán mức tăng cho một phương pháp optimization; phải có ablation riêng.

## 6. Benchmark công bằng và cách chọn

1. **Kiểm tra nguồn trước khi chạy:** tải từ nguồn chính thức, lưu manifest/checksum, xác nhận mapping nhãn và protocol, phiên bản trọng số, preprocessing và quyền nghiên cứu. Dữ liệu, ảnh mặt và checkpoint để ngoài Git.
2. **Chia theo lượt/chuỗi, không chia ngẫu nhiên từng frame.** Với D1, trước hết tái lập G1/G2 do tác giả công bố: chọn ngưỡng/siêu tham số trên nhóm phát triển và báo trên nhóm đánh giá, rồi đảo chiều theo protocol. Các frame liên tiếp của một lượt chỉ ở một phía. Vì cùng người có thể xuất hiện ở cả nhóm, đây là đánh giá **khác phiên**, chưa phải chứng minh tổng quát cho danh tính hoàn toàn mới. Nếu đủ người, thêm phép thử identity-disjoint; mẫu nhỏ thì ghi độ bất định.
3. **Genuine và impostor claim:** ảnh tham chiếu và ảnh tại cửa cùng người là genuine; người khác khai báo cùng hồ sơ là impostor. Cách lấy cặp impostor phải cố định và công bố, tránh nhân cùng một người thành hàng nghìn cặp rồi coi như quan sát độc lập.
4. **Metric nhận diện:** FMR (chấp nhận sai người), FNMR (từ chối người đúng), ROC/DET, FNMR tại mức FMR đã chốt cho phép thử, số cặp và khoảng tin cậy. [NIST nêu FMR/FNMR là các metric theo ngưỡng](https://pages.nist.gov/frvt/html/frvt11.html). Accuracy/EER có thể báo thêm, không thay lỗi tại ngưỡng vận hành. Với D1 ít người, không tuyên bố FMR cực thấp từ việc không thấy lỗi.
5. **Metric pipeline:** detection recall, tỷ lệ không có mặt đủ chất lượng, số khung/lượt, retry/manual, p50/p95 độ trễ xử lý, RAM, dung lượng model và lỗi giao dịch. Đo trên cùng phần cứng; nếu chưa có điện thoại thì báo rõ benchmark máy tính chỉ là bước sàng lọc, chưa chứng minh chạy mobile.
6. **Quy tắc chọn:** chốt mục tiêu lỗi và giới hạn tài nguyên từ yêu cầu đồ án trước khi xem test; so các model ở cùng mức FMR hoặc trình bày đường đánh đổi. Model được chọn bằng development, khóa cấu hình rồi mới mở test. Nếu xét nhiều dataset, không lấy trung bình accuracy giữa các tập khác protocol để tuyên bố một model thắng; báo từng tập và lý do khác biệt.

**Phân tích “vì sao cao/thấp”:** phân nhóm lỗi theo kích thước mặt, mờ, độ sáng, pose, che khuất, chất lượng ảnh tham chiếu, số frame và nguồn detector. So score distribution genuine/impostor, FNMR theo điều kiện và ảnh lỗi đại diện **chỉ trong môi trường làm việc được phép**, không commit ảnh. Dùng ablation/same-input để phân biệt lỗi do detector/căn chỉnh với lỗi embedding. Đây là giả thuyết có bằng chứng, không khẳng định nguyên nhân chỉ vì model A có số tổng tốt hơn B. Kết quả tác giả công bố có thể khác do dữ liệu huấn luyện, preprocessing, protocol và phần cứng; không so trực tiếp với số của đồ án.

## 7. Những hướng tối ưu cho **nhận diện chính**

### H1 — chọn và ghép nhiều khung theo chất lượng (ưu tiên khảo sát)

**Giả thuyết:** D1 có chuỗi mặt lúc rõ, lúc mờ/nghiêng; B0 đơn khung bỏ lỡ khung tốt, còn B1 chọn khung/mean embedding đơn giản chưa dùng hết thông tin. **Thành phần được tối ưu:** chính sách chọn K khung hoặc trọng số ghép embedding trước phép so 1:1, không thay model nhận diện. **Biến:** K, khoảng thời gian chờ, ngưỡng loại frame mờ/góc lớn, trọng số chất lượng, quy tắc loại ngoại lệ và số lần inference tối đa. **Objective:** giảm FNMR trên development khi giữ FMR ở mức đã chốt, cùng trần p95 độ trễ/số inference; có thể trình bày Pareto nếu các mục tiêu xung đột. **Đối chứng:** B0, B1 chọn ảnh rõ nhất, mean embedding, random/grid search cùng số lần đánh giá. Chỉ chọn PSO/Jaya/BO khi không gian và ngân sách cho thấy nó có ích. **Đo:** FMR/FNMR, tỷ lệ cần retry, p95 độ trễ trên D1; dùng D2 để kiểm tra riêng phần chống chênh chất lượng, không suy từ D2 ra lợi ích video. Tách tác động “chọn frame” và “ghép embedding” bằng ablation.

### H2 — phát hiện/căn chỉnh/crop phục vụ nhận diện

**Giả thuyết:** lỗi ở D1 đến từ box hoặc landmark không ổn định khi mặt nhỏ/nghiêng. **Thành phần:** detector threshold, crop margin, alignment hoặc bộ lọc kích thước mặt. **Biến/objective:** tham số tiền xử lý, giữ detection recall và giảm FNMR/FMR đầu-cuối với trần latency. **Đối chứng:** preprocess mặc định của từng model và grid/random cùng ngân sách. D4 có thể chẩn đoán detector, nhưng kết luận nhận diện phải nằm trên D1/D2. Chỉ nhận H2 làm đóng góp chính nếu phân tích B0 chứng minh lỗi ở khâu này; thay detector thường kéo theo thay landmark/crop nên cần ablation.

### H3 — đặc trưng và phép so sau embedding

**Giả thuyết:** embedding hiện có dư chiều hoặc cosine/normalization chưa phù hợp với ảnh chất lượng kém. **Thử:** PCA/projection hoặc chọn nhóm chiều có ràng buộc, metric/cách gộp điểm có regularization. **Đo:** FMR/FNMR, RAM, thời gian và kích thước trên test độc lập. Với vài chục người của D1, học subset 512 chiều dễ overfit; không ưu tiên nếu thiếu tập development đủ lớn. Không dùng nhãn test để học phép chiếu.

### H4 — ngưỡng quyết định và vùng “không chắc”

**Thử:** một ngưỡng accept so với hai ngưỡng accept/manual, cộng giới hạn số lần chụp lại. **Đo:** FMR, FNMR, manual rate và thời gian. Đây là chính sách cần có, nhưng quét ngưỡng ít chiều vốn đơn giản; không dùng metaheuristic chỉ để tạo tên thuật toán. Ngưỡng là theo **model và protocol**, không bê ngưỡng SFace sang buffalo_sc.

### H5 — kích thước/tốc độ model trên mobile

Nếu benchmark chỉ ra latency/RAM là nút thắt, so lượng tử hóa hoặc cấu hình input/model gọn với bản gốc **trên cùng điện thoại**. **Đo:** FMR/FNMR, p95, RAM, kích thước và năng lượng nếu đo được. Đối chứng gồm model gọn chưa tối ưu (M0/M1) và model mạnh M2 để biết chi phí chính xác của giảm kích thước. Đây là hướng có giá trị nếu nghiệm tối ưu tiến lên đường Pareto, không phải chỉ chạy nhanh hơn nhưng lỗi không chấp nhận được.

### H6 — train/fine-tune nếu được thầy yêu cầu và có dữ liệu phù hợp

Bản Word có nhắc train/fine-tune, nhưng D1 quá ít danh tính để huấn luyện recognizer tổng quát. Chỉ mở H6 khi tìm được tập train có quyền rõ, tách identity khỏi test và có compute. Search space có thể gồm learning rate, weight decay, augmentation, margin/số epoch; so default, random/grid và thuật toán optimization cùng ngân sách. **Không giả vờ rằng fine-tune trên vài chục người D1 chứng minh hệ thống dùng được cho thí sinh mới.**

## 8. Chọn đóng góp chính sau benchmark, không chọn trước kết quả

**Ưu tiên nghiên cứu hiện tại:** H1, vì D1 thực sự có chuỗi ở điểm qua cửa và file gốc gợi việc tối ưu chọn thông tin đầu vào/đánh đổi chất lượng–thời gian. Đây là **giả thuyết để kiểm tra**, không phải quyết định đã chứng minh. Mốc chốt theo dữ liệu:

- Nếu B0 lỗi chủ yếu ở frame mờ/góc xấu và B1 vẫn còn khoảng cải thiện: chọn H1.
- Nếu chọn frame tốt rồi mà detector/căn chỉnh vẫn sai nhiều: chọn H2.
- Nếu embedding đúng mặt, ảnh rõ nhưng FNMR còn cao: xem model khác mạnh hơn trước; chỉ mở H3/H6 khi dữ liệu cho phép.
- Nếu model tốt nhất quá chậm/lớn trên điện thoại: chọn H5.
- Nếu một model khác **thống trị** baseline dự định tối ưu ở cả lỗi và chi phí, phải đổi baseline/chủ đề hoặc nêu rõ ràng buộc khác; không cố tối ưu model yếu cho đẹp biểu đồ.

Khi đã chọn H, khóa câu hỏi nghiên cứu dưới dạng: “Trên D1 với model M đã chọn và protocol P, tối ưu tham số X theo objective O có cải thiện FNMR tại FMR mục tiêu và p95 latency so với B1/random search, và kết quả cuối có cạnh tranh với M mạnh nhất chưa tối ưu không?” Thuật toán optimization được chọn **sau** khi biết X và ngân sách, không mặc định Jaya/HHO/PSO. Nếu làm H1+H2, báo B0, +H1, +H2, +H1+H2 trên cùng split và hardware.

## 9. Chống giả mạo và nghiệp vụ hệ thống là phần bổ trợ

Chống ảnh/video giả mạo (PAD) là **mô-đun để hệ thống hoàn thiện về sau**, không nằm trong hướng tối ưu nhận diện chính của T-005 và không cần dataset PAD trong benchmark chọn model/đóng góp. Nếu có thời gian tích hợp, phải đo riêng lỗi PAD trên dữ liệu tấn công phù hợp; [NIST cũng đánh giá PAD như bài toán riêng](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based). Không gộp accuracy PAD với FMR/FNMR nhận diện, không nói hệ thống đã chống giả mạo nếu chỉ thêm bước UI.

Phòng/ca, đến muộn, sai phòng, trùng lượt, người vắng và lưu nhật ký có thể được minh họa bằng dữ liệu hồ sơ giả lập. Các quy tắc cụ thể phải đặc tả theo kỳ thi mục tiêu. Phần đó chứng minh logic phần mềm, không bù cho giới hạn của dataset mặt. Nếu chưa có PAD/kiểm thử thực tế, demo chỉ là prototype nghiên cứu có cơ chế chuyển ngoại lệ, không phải hệ thống tự cho vào an toàn.

## 10. Đầu ra cần có của T-005 và bước tiếp

1. Danh mục dataset có nguồn, mục đích, quyền dùng, dung lượng, protocol và **khoảng cách với cửa phòng thi**; kiểm tra file D1/D2 thực tế trước khi chốt tải toàn bộ.
2. Danh mục trọng số M0–M2 với version/hash, detector, recognizer, preprocess, giấy phép và điều kiện chạy. Chưa khẳng định model nào tốt nhất khi chưa benchmark.
3. Giao thức benchmark được khóa: split G1/G2, cách tạo claim, threshold, metric, phần cứng, seed, số cặp/lượt và cách báo uncertainty.
4. Sau benchmark: bảng kết quả từng dataset/từng model, phân tích lỗi theo điều kiện và đường đánh đổi accuracy–latency–size; từ đó viết **lý do chọn model gốc và lý do không chọn các model còn lại**.
5. Chỉ khi đã thấy bottleneck mới chốt H1/H2/H5/H6, search space/objective/thuật toán, baseline mạnh và ablation. Hỏi thầy rõ yêu cầu train/fine-tune, ghi biên bản trước khi biến nó thành ràng buộc chính thức.

**Trạng thái hiện tại:** đây là kế hoạch khảo sát có căn cứ nguồn, **chưa có điểm benchmark, chưa xác nhận đã tải dữ liệu hay quyền dùng của từng ảnh, chưa chọn model cuối**. Kết luận về tiết kiệm nhân sự và triển khai thương mại vẫn là mục tiêu sản phẩm, ngoài phạm vi suy ra trực tiếp từ benchmark dataset công khai.
