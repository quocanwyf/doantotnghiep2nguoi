# T-005 — Khảo sát kỹ thuật cho xác thực thí sinh tại cửa phòng thi

**Người đề xuất:** Quốc An. **Trạng thái:** bản khảo sát có lập luận để nhóm review; chưa có dữ liệu thu, baseline chạy hoặc kết quả thực nghiệm. Quốc An thông báo nhóm đã chọn bối cảnh từ [T-002](../01-problem/quoc-an-proposal.md) ở T-004; tại thời điểm viết, Sheet và thư mục quyết định chưa có đầu ra T-004, nên cần đồng bộ hồ sơ quyết định. Không tự coi lựa chọn model/dataset/thuật toán trong tài liệu này là quyết định T-007.

## 1. Từ mục tiêu nghiệp vụ đến câu hỏi nghiên cứu

Đơn vị tổ chức biết trước lịch thi, danh sách theo phòng/ca và ảnh đăng ký. Hiện giám thị hoặc nhân sự được phân công phải đối chiếu từng người ở cửa, xử lý người đến muộn/sai phòng, rồi kiểm tra ai đã vào và ai vắng. Sản phẩm mong muốn là **thiết bị đảm nhận phần kiểm tra đầu vào thường lệ**, để giảm nhu cầu bố trí một người chuyên làm việc đó ở từng phòng; một người có thẩm quyền vẫn phải xử lý ngoại lệ và những nhiệm vụ giám thị mà quy chế yêu cầu. Với kỳ thi tốt nghiệp THPT theo [quy chế Bộ GD&ĐT hiện công bố](https://vqa.moet.gov.vn/uploads/news/2024_12/final-quy-che-thi-tot-nghiep-thpt.pdf), giám thị đối chiếu danh sách ảnh và giấy tờ, nên đồ án không được tuyên bố có thể bỏ bước đó khi chưa có quy trình được phép thay thế.

Luồng chính được chọn làm giả định khảo sát: **thí sinh khai báo mã trước → hệ thống lấy hồ sơ → camera chọn đúng người đang làm thủ tục dù hành lang có người khác → xác minh mặt 1:1 với ảnh đăng ký → kiểm tra phòng/ca/giờ/trùng lượt → cho tiếp tục hoặc chuyển xử lý**. Nhận dạng khuôn mặt trả lời “mặt có khớp ảnh tham chiếu?”, còn kiểm tra quyền vào phòng là quy tắc nghiệp vụ khác. Mã dự thi chỉ định hồ sơ, không tự chứng minh người cầm mã là chủ hồ sơ. Nếu máy không chắc, kết quả phải là chụp lại hoặc xử lý ngoại lệ, không tự tước quyền dự thi.

Câu hỏi kỹ thuật trung tâm của Quốc An: **trong ảnh nguyên khung tại cửa phòng có người xung quanh và chất lượng thay đổi, pipeline gốc sai nhiều ở khâu nào; có thể dùng một thuật toán tối ưu để chọn/cấu hình vùng mặt, khung hình hoặc quyết định phù hợp hơn nhằm giảm lỗi xác minh và thời gian xử lý trên điện thoại không?**

## 2. Đối chiếu bản Word định hướng gốc

[File dinhhuongdatn.docx](../sources/dinhhuongdatn.docx) là **ghi chép do nhóm cung cấp sau buổi gặp đầu**, không phải văn bản xác nhận từng ý của thầy. Tài liệu đó lặp lại logic: bắt đầu từ bài toán, chứng minh điểm yếu, xác định đối tượng và hàm mục tiêu, rồi mới chọn thuật toán optimization. Các ví dụ được ghi gồm ROI, bounding box, chọn đặc trưng, hyperparameter, cấu trúc model và đánh đổi chất lượng–tốc độ trên mobile; Jaya/HHO/PSO/GA/Bayesian Optimization đều chỉ là ứng viên. Bản ghi còn nêu train/fine-tune như phần cốt lõi và phân biệt optimization ở training với inference. Nhóm cần hỏi lại thầy xem **việc train/fine-tune model nhận dạng có bắt buộc** hay tối ưu có vai trò tìm kiếm rõ trong pipeline inference là đủ; câu hỏi này chưa được xác nhận trong biên bản/quyết định.

Hệ quả cho T-005: không gọi việc đặt ROI bằng tay, đổi Adam sang SGD, cắt vài layer hoặc quét một ngưỡng là đóng góp optimization nếu chưa chứng minh **thuật toán tìm kiếm/lựa chọn cái gì, trên không gian nào, tối ưu mục tiêu nào, hơn đối chứng đơn giản ra sao**. Nếu hướng chính tối ưu ở inference, phải giải thích rõ quan hệ với yêu cầu train/fine-tune trong bản ghi và có phương án dự phòng ở training.

## 3. Điều kiện vận hành và ranh giới của nghiên cứu

Một giao dịch bắt đầu khi thí sinh khai báo mã và kết thúc bằng một trạng thái được lưu: xác minh đủ điều kiện, yêu cầu chụp lại, hoặc chuyển người có quyền xử lý. Một lượt chỉ có một người trong vùng đứng, nhưng khung hình có thể có nhiều người ở nền. Máy phải chịu được khác biệt ánh sáng, chiều cao, khoảng cách, góc mặt, khẩu trang và hàng chờ gần giờ thi. Quy tắc “quá giờ 15 phút” chỉ là ví dụ người dùng nêu; **không hard-code 15 phút** trước khi biết quy chế của kỳ thi mục tiêu.

Các tình huống cần dữ liệu/giao thức: đúng người đúng phòng/ca; đúng người nhưng sai phòng/ca; người lạ dùng mã hợp lệ; mã không tồn tại; trùng lượt; đổi phòng; đến muộn; ảnh mờ/ngược sáng; hai mặt tranh vùng; khẩu trang; ảnh đăng ký cũ; trình ảnh/video giả mạo; mất mạng/thiết bị lỗi. Chống giả mạo là **điều kiện sản phẩm quan trọng nếu muốn bỏ người kiểm tra tại cửa**. Nếu đề tài không triển khai/đo PAD, bản demo chỉ được kết luận về xác minh trong điều kiện có giám sát, không tuyên bố cho vào tự động an toàn.

## 4. Khảo sát dữ liệu theo vai trò, quyền dùng và quyết định

### D1. Tập mô phỏng cửa phòng thi có sự đồng ý — dữ liệu chính được đề xuất

Thu ảnh đăng ký riêng trước ngày mô phỏng; sau đó ghi video/ảnh nguyên khung tại cửa với điện thoại cố định. Mỗi người có nhiều lượt ở ngày/giờ, ánh sáng và vị trí khác nhau. Bố trí người nền có đồng ý, có lượt người lạ khai báo mã của người khác, và kịch bản sai phòng/ca/trùng lượt. Gắn nhãn ID đã khai báo, ID thực, bounding box/track của người làm thủ tục, chất lượng thu, điều kiện nền và trạng thái nghiệp vụ đúng. Không dùng ảnh của một người chỉ để đánh giá nếu ảnh đó đã lọt vào bước huấn luyện/chọn ngưỡng không đúng giao thức.

**Vì sao chọn:** chỉ dữ liệu nguyên khung này đo được toàn bộ rủi ro “máy chọn mặt người đứng cạnh rồi cho qua”. Dữ liệu chân dung công khai đã cắt mặt không thay thế được. **Trạng thái:** chưa thu, chưa có phê duyệt/người tham gia/thiết bị; đây là điều kiện khả thi số một. Lưu dữ liệu ngoài Git, giới hạn người truy cập, có quy tắc đồng ý, thời hạn lưu và xóa. Nếu không thể thu tập này, phải thu hẹp nghiên cứu còn xác minh trên ảnh đơn lẻ và không kết luận về cửa phòng thi thực tế.

### D2. WIDER FACE — kiểm tra thành phần phát hiện nhiều mặt

[Trang chính thức](https://shuoyang1213.me/WIDERFACE/) cung cấp ảnh nhiều khuôn mặt, biến thiên kích thước/góc/che khuất và ghi giấy phép CC BY-NC-ND. Có thể dùng để đánh giá detector trong nghiên cứu sau khi đọc đúng điều kiện tải/sử dụng; không có mã thí sinh, mặt mục tiêu hay trạng thái lượt vào. **Không chọn làm tập đánh giá đầu-cuối.** Trọng số được huấn luyện bằng dữ liệu khác có điều khoản riêng; giấy phép của WIDER FACE không tự cấp quyền thương mại cho trọng số.

### D3. LFW — thử mô-đun xác minh 1:1

[Công bố LFW](https://people.cs.umass.edu/~elm/papers/lfw.pdf) mô tả phép thử cặp ảnh cùng/khác người. Dùng làm kiểm tra sơ bộ tính đúng của embedding/so điểm và đối chiếu literature, không dùng để đo chọn mặt ở hành lang. Quyền tải/sử dụng bộ ảnh và tình trạng truy cập hiện **chưa được xác minh**; không xem là tập chính đến khi kiểm tra xong.

### D4. Dữ liệu PAD riêng nếu chọn chống giả mạo

[Replay-Attack của Idiap](https://www.idiap.ch/en/scientific-research/data/replayattack/index_html?set_language=en) là một nguồn tham khảo về ảnh/video giả mạo; cần kiểm tra điều khoản truy cập, loại tấn công và mức giống camera cửa phòng. Dataset PAD không được trộn vào tập xác minh thường rồi báo một accuracy chung. Nếu không có quyền/tập tấn công phù hợp, giữ PAD là rủi ro và giới hạn phạm vi, không tuyên bố đã giải quyết.

### Kết luận về dữ liệu

**Đề xuất chọn D1 làm tập đánh giá chính**, D2/D3 chỉ hỗ trợ kiểm tra thành phần, D4 là nhánh có điều kiện. Không có dataset công khai nào trong các nguồn đã kiểm tra khớp cả ba phần: mã khai báo, mặt mục tiêu giữa người nền và sự kiện vào phòng. Chưa chọn dữ liệu train/fine-tune model nhận dạng vì quyền, kích thước và domain chưa đủ bằng chứng; đây là rủi ro nghiên cứu cần giải quyết trước khi hứa train lại mạng.

## 5. Model/pipeline ứng viên và lý do đề xuất baseline

### Phương án A — YuNet + SFace trong OpenCV Zoo

[YuNet](https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/README.md) là detector gọn có landmark; [SFace](https://github.com/opencv/opencv_zoo/blob/main/models/face_recognition_sface/README.md) là model nhận dạng dựa trên MobileFaceNet và hỗ trợ căn chỉnh theo 5 landmark. OpenCV Zoo có mã demo ghép hai thành phần. README thư mục YuNet ghi MIT và thư mục SFace ghi Apache 2.0. Chọn đúng phiên bản trọng số trước khi chạy và lưu hash; bản gợi ý để kiểm tra khả năng tái lập là YuNet 2023mar + SFace 2021dec, vì cặp này xuất hiện trong demo chính thức. Không lấy accuracy do tác giả báo trên LFW làm dự đoán accuracy ở cửa phòng.

**Lý do ưu tiên làm baseline khả thi:** hai thành phần có ví dụ tích hợp, model gọn và phù hợp để thử trên điện thoại. **Giới hạn:** giấy phép thư mục không giải quyết hết nguồn dữ liệu dùng để huấn luyện trọng số; phải rà provenance nếu tiến tới thương mại. Chưa đo tốc độ/độ chính xác trên điện thoại của nhóm nên chưa chốt đây là stack cuối.

### Phương án B — InsightFace buffalo_sc

[Model zoo chính thức](https://github.com/deepinsight/insightface/blob/master/python-package/docs/model_zoo.md) liệt kê gói buffalo_sc gồm SCRFD-500MF và MobileFaceNet, kích thước công bố khoảng 16 MB. Đây là đối chứng học thuật hợp lý nếu A yếu hoặc cần so với pipeline khác. **Giới hạn quyết định:** trọng số do InsightFace cung cấp chỉ dành cho nghiên cứu phi thương mại, dù mã thư viện có giấy phép MIT; không được chuyển nguyên gói này sang sản phẩm startup nếu chưa có quyền riêng. Nếu dùng B, báo rõ đây là benchmark nghiên cứu và không so B với A như bằng chứng cho thuật toán tối ưu khi cả detector lẫn embedding cùng đổi.

### Phương án C — MobileFaceNet được train/fine-tune trên dữ liệu có quyền

[MobileFaceNets](https://arxiv.org/abs/1804.07573) là kiến trúc định hướng thiết bị di động. Nếu thầy xác nhận cần train/fine-tune nhận dạng, khảo sát một phiên bản có trọng số và dữ liệu huấn luyện được phép dùng, cùng ngân sách tính toán và giao thức identity-disjoint. Không thể quyết định C chỉ vì nó “mobile”: cần biết quyền trọng số/dataset, số danh tính đủ cho fine-tune và máy huấn luyện. C là **phương án dự phòng có điều kiện**, không phải baseline đang sẵn sàng.

**Phân biệt thuật ngữ:** ArcFace là hàm loss/phương pháp học embedding, không phải tên một trọng số cụ thể; MobileFaceNet là kiến trúc; SCRFD/YuNet là detector; SFace có trọng số phát hành trong OpenCV Zoo. Mọi so sánh phải ghi chính xác model file và preprocessing.

## 6. Baseline và phép đo điểm yếu trước khi tối ưu

**B0 — baseline đầu-cuối bắt buộc:** camera nguyên khung → vùng đứng cố định → YuNet phát hiện mặt → chọn mặt trong vùng bằng quy tắc hình học công khai (ví dụ gần tâm vùng nhất, từ chối nếu có hai mặt tranh chấp) → căn chỉnh 5 điểm → SFace tạo embedding → cosine similarity so với ảnh đăng ký → một ngưỡng chọn trên development set → check phòng/ca/giờ/trùng lượt. Chọn ảnh tại một thời điểm quy định. Đây là baseline đề xuất để chạy đầu tiên, không phải kết quả đã chạy.

**B1 — đối chứng đơn giản trước thuật toán tối ưu:** giữ nguyên YuNet/SFace, vùng camera, dữ liệu và ngưỡng hiệu chỉnh đúng giao thức; lấy một cửa sổ khung ngắn rồi chọn khung theo quy tắc chất lượng đơn giản như kích thước mặt/độ mờ/góc mặt. B1 trả lời liệu cải thiện chỉ đến từ “đợi khung tốt hơn” hay thực sự cần thuật toán tìm kiếm. Nếu thu chỉ ảnh tĩnh, không chạy B1 và ghi giới hạn.

Đầu tiên chạy cả B0/B1 trên tập phát triển và đánh dấu lỗi theo nguyên nhân: không tìm thấy mặt; chọn sai người; crop/căn chỉnh lỗi; đúng mặt nhưng điểm so sai; ảnh đăng ký kém; quy tắc sai phòng/ca; xử lý chậm; nghi giả mạo. Chỉ chọn tối ưu chính khi phân bố lỗi và dữ liệu chứng minh nó đáng làm. B0/B1 có thể dùng trọng số cố định; nếu thầy yêu cầu train/fine-tune, cần thêm một baseline train/fine-tune tương ứng để so công bằng, không so model frozen với model đã học lại rồi quy mọi chênh lệch cho ROI optimization.

## 7. Các hướng cải thiện: đối tượng, search space, objective, điều kiện

### H1 — tối ưu chọn mặt/ROI trong khung đông người (ưu tiên kiểm tra)

**Giả thuyết:** detector tìm đúng các mặt nhưng quy tắc chọn mặt của B0 sai khi người nền bước gần camera, hoặc crop chứa ít/nhiều nền làm embedding kém. **Đối tượng optimization:** cấu hình chọn mặt và crop sau detector; không thay recognition model.

**Biểu diễn nghiệm có thể thử:** vùng đứng chuẩn hóa (x, y, rộng, cao); lề crop quanh box; trọng số cho khoảng cách đến tâm, kích thước mặt, độ rõ/góc và tính liên tục track; ngưỡng “hai mặt quá gần nhau thì chuyển thủ công”. Giới hạn nghiệm hợp lệ theo hình học khung hình và thời gian một lượt. Đây là không gian vừa có số liên tục vừa có lựa chọn rời rạc; không nên tối ưu một ROI cố định từ một cửa rồi báo tổng quát cho mọi cửa.

**Đối chứng/lựa chọn:** B0 gần tâm vùng; B1 chọn khung tốt thủ công; random/grid search với ngân sách bằng thuật toán được đề xuất; một thuật toán tìm kiếm như PSO/Jaya/GA hoặc Bayesian Optimization chỉ được chọn sau khi thử biểu diễn và ngân sách đánh giá. Nếu không gian nhỏ, grid/random đủ tốt thì không có lý do gọi metaheuristic là đóng góp.

**Đo:** tỷ lệ chọn nhầm người nền, tỷ lệ không xác định được mặt mục tiêu, FMR/FNMR đầu-cuối và thời gian/lượt trên các cửa/điều kiện chưa dùng lúc chỉnh tham số. Đổi vùng camera có thể làm thay đổi người được chọn, nên cần giữ cùng video/khung đầu vào khi so baseline và proposed.

### H2 — tối ưu chọn khung/kiểm tra chất lượng (ưu tiên kiểm tra cùng H1, nhưng ablation riêng)

**Giả thuyết:** một khung ngẫu nhiên có mặt mờ/ngoảnh đi; khung sau tốt hơn. **Đối tượng:** chọn khung nào đưa vào cùng recognizer và khi nào yêu cầu chụp lại. **Biểu diễn nghiệm:** số khung tối đa/thời gian chờ; trọng số kích thước, độ sắc nét, ánh sáng, góc mặt và che khuất; ngưỡng chất lượng. Có thể tối ưu offline bộ tham số chọn khung trên development set, rồi chạy chính sách cố định trên mobile.

**Objective:** trong tập phát triển, trước hết giữ FMR không vượt mức nghiệp vụ ấn định; sau đó giảm FNMR và tỷ lệ chuyển thủ công, kèm trần thời gian/lượt. Nếu mục tiêu xung đột, đưa đường đánh đổi thay vì chọn trọng số tùy tiện. **Đo:** FNMR@FMR mục tiêu, tỷ lệ chụp lại, tỷ lệ không có khung đủ tốt, p50/p95 thời gian và số lần chạy recognizer. Không chỉ báo điểm similarity trung bình vì tăng similarity của cả impostor có thể gây hại.

### H3 — tối ưu quyết định/ngưỡng và vùng chuyển thủ công

**Giả thuyết:** hệ thống thiếu vùng “không chắc”, khiến chấp nhận nhầm hoặc chuyển người hợp lệ quá nhiều. **Đối tượng:** ngưỡng accept, ngưỡng retry/manual, ngưỡng chất lượng và số lần thử. **Đối chứng bắt buộc:** tìm ngưỡng bằng quét lưới trên development set; với ít tham số, PSO/GA không tự có giá trị nghiên cứu. **Đo:** lỗi chấp nhận sai người, FNMR, tỷ lệ chuyển thủ công, thời gian. Đây là hướng phụ trợ nếu H1/H2 cần chốt chính sách, chưa đề xuất làm đóng góp chính đơn độc.

### H4 — feature selection hoặc cấu hình model

Bản Word gợi ý chọn feature/giảm chiều hoặc cấu trúc model. Với embedding đã huấn luyện, bỏ chiều theo score nhỏ không chứng minh phần bị bỏ là vô ích; cần một thuật toán chọn subset và đánh giá identity-disjoint với ràng buộc kích thước/tốc độ. Search space 512 chiều nhị phân dễ quá lớn và overfit tập nhỏ; chỉ nên thử nhóm chiều/projection có đối chứng PCA/random projection, dữ liệu đủ và đo thay đổi thật trên mobile. Model pruning/quantization cũng cần xác định tập cấu hình, objective và baseline trước khi gọi optimization. **Xếp dự phòng**, vì H1/H2 gắn trực tiếp lỗi nghiệp vụ hơn.

### H5 — optimization ở training/fine-tune nếu được yêu cầu

Nếu xác nhận train/fine-tune là điều kiện học thuật, cần dataset nhiều danh tính có quyền dùng và tách identity train/dev/test. Lúc đó một hướng riêng là tìm cấu hình fine-tune cho model gọn: learning rate, weight decay, augmentation, số epoch, margin/loss nếu phù hợp. Thuật toán tìm kiếm chỉ có ý nghĩa nếu so với default và random/grid cùng ngân sách train; mỗi trial lưu seed, code, thiết bị và chi phí. Hướng này có rủi ro cao về dữ liệu và compute; không được dùng vài chục người trong mô phỏng cửa phòng để train một recognizer rồi tuyên bố tổng quát.

### H6 — hiệu năng mobile và chống giả mạo

Nếu B0/B1 chậm, khảo sát giảm độ phân giải, model gọn hoặc lượng tử hóa trên **cùng điện thoại**; so FMR/FNMR, chọn mặt, bộ nhớ, kích thước và p95 thời gian. Đây có thể là mục tiêu đa tiêu chí nếu độ trễ thật sự là nút thắt. Edge device để sau mobile như bản Word ghi.

Nếu mong thiết bị làm phần kiểm tra đầu vào chính mà không có nhân sự đứng cửa, phải thiết kế lớp phát hiện ảnh/video giả mạo và cơ chế giám sát ngoại lệ. [NIST đánh giá PAD như một bài toán riêng](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based). Hướng PAD cần dữ liệu tấn công, metric lỗi người thật và lỗi chấp nhận tấn công; không thêm một model PAD vào cuối pipeline rồi coi như đã an toàn. Nếu tài nguyên không đủ, phạm vi đồ án là hỗ trợ/triage có người xử lý từ xa hoặc trong phòng, và giới hạn đó phải ghi rõ.

## 8. Đề xuất ưu tiên, chưa chốt đóng góp chính

**Khuyến nghị của Quốc An cho bước tiếp:** dùng A (YuNet + SFace) làm baseline đầu tiên nếu quyền/trọng số được rà xong; thu D1; đo lỗi B0. Nếu lỗi chọn sai người hoặc khung xấu chiếm tỷ trọng đáng kể, chọn **H1 hoặc H2** làm tối ưu chính; nếu cả hai cùng có tác động thì làm ablation B0, +H1, +H2, +H1+H2. Đây là hướng khớp nhất với tình huống hành lang đông người, ROI/bounding box trong bản Word và vai trò của optimization là **tìm/chọn một cấu hình** để xử lý ảnh hiệu quả hơn. Thuật toán cụ thể chưa chốt trước khi biết hình dạng search space và số lần đánh giá cho phép.

**Phương án dự phòng:** nếu lỗi chính nằm ở recognizer hoặc thầy yêu cầu train/fine-tune, khảo sát H5 với dữ liệu/quyền dùng tương ứng; nếu lỗi chính là thời gian trên điện thoại, khảo sát H6. H3 là phần hiệu chỉnh quyết định cần có ở mọi pipeline nhưng ít phù hợp làm đóng góp duy nhất. H4 chỉ chọn khi dữ liệu và bằng chứng cho thấy embedding/cấu trúc gây vấn đề. Không chạy tất cả tổ hợp.

**Lý do chưa chọn ngay thuật toán Jaya/PSO/HHO:** bản Word liệt kê chúng như công cụ, không có thuật toán nào tự tạo cải thiện. H1/H2 có biến rời rạc/liên tục và objective có ràng buộc; cần một thử nghiệm nhỏ trên development set để xem grid/random/BO/metaheuristic nào phù hợp. Nếu thuật toán đề xuất không hơn một phương pháp đơn giản cùng ngân sách, phải báo kết quả đó trung thực.

## 9. Giao thức chia dữ liệu và đánh giá định lượng

**Đơn vị split là người và lượt/phiên**, không phải khung hình ngẫu nhiên. Tập train (nếu huấn luyện), development để chọn model/cấu hình/ngưỡng, và test cuối phải độc lập theo người khi mục tiêu là khả năng dùng với thí sinh mới. Trong test, mỗi người vẫn có ảnh đăng ký riêng được cấp trước như nghiệp vụ thật; không dùng bất kỳ lượt qua cửa test nào để chỉnh ngưỡng. Các khung trong cùng lượt luôn nằm cùng một split; thử thêm tách theo ngày, camera và vị trí cửa để đo domain shift. Dữ liệu D1 phải có cả genuine và impostor claim, không chỉ hai ảnh của cùng người.

**Metric tầng mô-đun:** detection recall và lỗi chọn mặt mục tiêu; với xác minh 1:1 dùng FMR/FNMR và đường ROC, báo FNMR tại mức FMR được nghiệp vụ chấp nhận. [NIST định nghĩa/đánh giá FMR và FNMR tại ngưỡng](https://pages.nist.gov/frvt/html/frvt11.html). EER/accuracy có thể phụ trợ nhưng không thay FMR/FNMR khi lỗi cho nhầm người nặng hơn.

**Metric tầng giao dịch:** tỷ lệ máy đề xuất cho qua sai người; tỷ lệ người hợp lệ bị chụp lại/chuyển xử lý; tỷ lệ tự xử lý thành công; sai phòng/ca/trùng lượt; thời gian thao tác mỗi người, p50/p95 độ trễ kỹ thuật, thông lượng trong hàng chờ mô phỏng và thời gian đối soát người vắng. Phải phân biệt “máy đề xuất” với “người có thẩm quyền thực sự cho vào”. Đánh giá riêng theo khẩu trang, ánh sáng, góc và số người nền nếu mẫu đủ.

**Lỗi hiếm và độ tin cậy:** không tuyên bố đạt FMR rất thấp chỉ vì không thấy lỗi trong tập nhỏ. Báo số genuine/impostor attempts, số người, khoảng tin cậy và số lượt manual; các cặp chia sẻ cùng người không độc lập hoàn toàn. Mục tiêu FMR, thời gian/lượt và tỷ lệ chuyển thủ công là yêu cầu nghiệp vụ cần thống nhất, chưa tự đặt một con số.

**Điều kiện công bằng:** baseline và proposed cùng dữ liệu/split, ảnh đăng ký, protocol, preprocessing trừ thành phần nghiên cứu, seed, mã, thiết bị, giới hạn tính toán và cách chọn ngưỡng. Khi so thuật toán search, cùng số lần đánh giá objective và báo chi phí tìm kiếm. Trên mobile đo cùng máy, sau warm-up, nhiều lượt liên tiếp; không lấy thời gian desktop thay. Nếu đổi model đồng thời đổi ROI, cần ablation để tách tác động.

## 10. Quy trình quyết định và việc cần xác nhận

1. Xác nhận với đơn vị tổ chức/giám thị nghiệp vụ và ảnh đăng ký có được phép dùng; xác định quy tắc muộn, sai phòng, giấy tờ, trường hợp máy không chắc và ai xử lý. Không tự đặt “15 phút” cho mọi kỳ thi.
2. Xác nhận với thầy từ bản Word gốc: train/fine-tune recognizer có bắt buộc không, hay một thuật toán tối ưu offline chọn ROI/khung/chính sách inference với baseline/proposed và mobile là phù hợp? Ghi biên bản rồi cập nhật quyết định.
3. Có D1 hoặc kế hoạch thu được duyệt; kiểm tra nguồn/giấy phép D2–D4 và từng file trọng số. Nếu không có dữ liệu cửa phòng, không hứa đánh giá đầu-cuối.
4. Chạy B0/B1, công bố phân bố lỗi, chốt một optimization target cùng search space, objective và đối chứng đơn giản trước khi chọn thuật toán.
5. Thử trên development set, khóa phương pháp, đánh giá một lần trên test; báo cả cải thiện lẫn chi phí/giới hạn; triển khai mobile để chứng minh pipeline chạy thật.
