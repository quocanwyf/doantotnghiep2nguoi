# T-005 — Khảo sát kỹ thuật của Quốc An cho bài toán cửa phòng thi

**Trạng thái:** đề xuất khảo sát cá nhân, làm song song với T-002 của Quốc An để sau này so sánh cả **bài toán + cách giải kỹ thuật** với T-003/T-006 của Minh Hy. Chưa có lựa chọn chung T-004; chưa chạy baseline, thu dữ liệu hoặc chốt model. Bài toán nguồn: [đề xuất T-002](../01-problem/quoc-an-proposal.md).

## 1. Câu hỏi kỹ thuật suy ra từ nghiệp vụ

Một thí sinh khai báo mã trước cửa phòng thi. Camera điện thoại có thể thấy cả người đứng chờ và giám thị. Hệ thống phải chọn **đúng mặt của người đang làm thủ tục**, đối chiếu 1:1 với ảnh đăng ký của mã đã khai báo, rồi kiểm tra phòng, ca, giờ và tình trạng lượt vào. Nếu ảnh hoặc điểm đối chiếu không đủ tin cậy, chuyển giám thị xử lý thay vì tự từ chối quyền thi.

Câu hỏi nghiên cứu dự kiến: **với ảnh tại cửa phòng có người xung quanh và chất lượng biến đổi, phần nào của pipeline gốc gây nhiều lỗi nhận dạng/lượt vào nhất, và có thể cải thiện phần đó mà vẫn đáp ứng thời gian xử lý trên điện thoại không?** Chưa chọn sẵn phương pháp tối ưu; những hướng dưới đây là ứng viên cần dữ liệu và baseline để loại/chọn.

## 2. Dữ liệu, quyền dùng và khả năng tiếp cận

### Dữ liệu mục tiêu cần thu hoặc được phép nhận

Một bản ghi cần có: ảnh đăng ký gắn với mã thí sinh đã được xác minh; ảnh/video **nguyên khung** ở cửa; vùng đứng của người làm thủ tục và nhãn mặt mục tiêu; mã được khai báo; cùng/sai người; phòng/ca/giờ; trạng thái đã vào hay chưa; số người trong nền; điều kiện sáng, góc mặt, khẩu trang; kết quả xử lý thật hoặc mô phỏng. Cần cả các lượt impostor cố khai báo mã người khác, người ngoài danh sách và lượt phải chụp lại. Nếu chỉ có ảnh mặt đã cắt, không kiểm tra được lỗi chọn nhầm mặt trong hành lang.

Nguồn thực tế ưu tiên là một buổi **mô phỏng cửa phòng thi với người tham gia đồng ý**, ghi ảnh đăng ký ở thời điểm khác với lượt qua cửa và thử nhiều điều kiện. Trước khi thu cần xác định quyền ghi hình, mục đích dùng, người được truy cập, cách lưu/xóa và việc không đẩy ảnh danh tính lên Git. Nếu không được tiếp cận dữ liệu kỳ thi thật, báo cáo phải gọi đúng đây là mô phỏng, không tuyên bố đã đạt chất lượng triển khai trong kỳ thi thật. Dữ liệu cá nhân và ảnh khuôn mặt không được đặt trong repo.

### Dữ liệu công khai chỉ để thử thành phần

- **LFW:** có giao thức cặp cùng/khác người để kiểm tra bước xác minh 1:1 theo [công bố của tác giả](https://people.cs.umass.edu/~elm/papers/lfw.pdf). Chưa kiểm chứng đầy đủ điều khoản tải và sử dụng cho phương án cụ thể, nên trạng thái là **ứng viên, chưa được duyệt dùng**. LFW không thay cho video cửa phòng có người xung quanh.
- **WIDER FACE:** trang [benchmark và giấy phép CC BY-NC-ND](https://shuoyang1213.me/WIDERFACE/) là nguồn ứng viên cho thử phát hiện nhiều mặt/che khuất. Chỉ đánh giá thành phần phát hiện; không có nhãn mã thí sinh và lượt vào phòng. Quyền dùng trong sản phẩm thương mại không được suy từ benchmark nghiên cứu.
- **Replay-Attack:** [nguồn Idiap](https://www.idiap.ch/en/scientific-research/data/replayattack/index_html?set_language=en) là ứng viên nếu khảo sát ảnh/video giả mạo; cần đọc điều kiện truy cập trước khi tải. Đây là nhánh chống giả mạo riêng, không thể dùng để đo độ chính xác xác minh tại cửa.
- **Trọng số có sẵn:** [InsightFace phân biệt mã nguồn MIT với trọng số cung cấp chỉ cho nghiên cứu phi thương mại](https://github.com/deepinsight/insightface/blob/master/python-package/docs/model_zoo.md). Nếu thử trọng số này trong đồ án, không xem nó là giấy phép đưa cùng model vào sản phẩm startup. Mỗi checkpoint/model và dữ liệu huấn luyện của nó cần một dòng kiểm tra nguồn và quyền dùng.

**Điều kiện đủ dữ liệu để tiếp tục:** có tập ảnh nguyên khung được phép dùng, chứa nhiều lượt của cùng người ở thời điểm khác nhau, có người khác trong nền và có lượt sai người; có thể giữ một tập kiểm tra chưa dùng khi chọn phương án. Nếu không, cần thu thêm hoặc thu hẹp tuyên bố nghiên cứu.

## 3. Pipeline gốc và 1–2 baseline

Luồng từ đầu đến cuối: mã khai báo → truy vấn hồ sơ → camera thu vài khung → phát hiện mặt → xác định người đang ở vùng làm thủ tục → kiểm tra chất lượng/căn chỉnh → embedding ảnh thu và ảnh đăng ký → so điểm → chấp nhận sơ bộ/chụp lại/chuyển giám thị → kiểm tra phòng, ca, giờ, lượt trùng → ghi sự kiện.

**Baseline B0 (bắt buộc):** một khung hình; vùng đứng cố định; chọn mặt theo quy tắc hình học cố định trong vùng; một bộ phát hiện/căn chỉnh và một bộ embedding cố định; so độ tương đồng với một ảnh đăng ký; ngưỡng đặt trên tập phát triển. Chọn tên model sau khi kiểm tra trọng số/giấy phép và khả năng chạy. Đây là đối chứng tối thiểu có thể tái lập.

**Baseline B1 (nếu video đủ):** giữ detector, embedding, ngưỡng và dữ liệu như B0; thu một chuỗi ngắn rồi chọn khung theo quy tắc chất lượng đơn giản đã viết trước. B1 giúp biết liệu chỉ cần tránh một khung xấu hay không, trước khi dùng thuật toán tìm kiếm phức tạp.

Họ phương pháp có thể khảo sát gồm [SCRFD cho phát hiện](https://github.com/deepinsight/insightface/blob/master/detection/scrfd/README.md), [ArcFace cho embedding](https://arxiv.org/abs/1801.07698) và [MobileFaceNets cho mô hình gọn](https://arxiv.org/abs/1804.07573). Đây là **nguồn tham khảo kỹ thuật**, chưa phải quyết định sẽ ghép tất cả. Với mỗi model thử, ghi preprocessing, định dạng input, phiên bản/trọng số, giấy phép, kích thước và điều kiện chạy. Không thay detector và embedding cùng lúc khi đánh giá một cải tiến đơn lẻ.

## 4. Nhiều hướng tối ưu ứng viên

### H1. Chọn đúng mặt người làm thủ tục giữa người xung quanh

- **Thành phần:** bước chọn mặt sau detector, trước embedding.
- **Vấn đề cần thấy ở B0:** chọn mặt giám thị/người xếp hàng, hai mặt cùng lọt vùng hoặc mất mặt mục tiêu qua các khung.
- **Lựa chọn thử:** chọn mặt gần tâm vùng; vùng đứng có kích thước/vị trí khác nhau; theo dõi mặt liên tục trong vài khung; từ chối khung nếu có nhiều mặt tranh chấp trong vùng.
- **Dữ liệu cần:** ảnh/video nguyên khung có nhãn mặt mục tiêu và người nền.
- **Đo:** tỷ lệ chọn sai mặt, lỗi xác minh **đầu-cuối**, tỷ lệ phải làm lại, độ trễ. Không dùng độ chính xác detector đơn lẻ làm kết luận về đúng người làm thủ tục.

### H2. Chọn khung hình và kiểm tra chất lượng

- **Thành phần:** thời điểm chụp và chất lượng ảnh đưa vào embedding.
- **Vấn đề cần thấy:** mờ do di chuyển, ngược sáng, mặt nghiêng, khẩu trang, một khung ngẫu nhiên kém nhưng khung tiếp theo tốt.
- **Lựa chọn thử:** một khung so với vài khung; chọn theo kích thước mặt, độ sắc nét, độ sáng, góc mặt hoặc điểm chất lượng đã kiểm chứng; ngưỡng yêu cầu chụp lại.
- **Dữ liệu cần:** chuỗi khung cùng lượt và nhãn đúng/sai; cần lưu rõ trường hợp không tìm được khung đủ chất lượng.
- **Đo:** FNMR tại cùng giới hạn FMR, tỷ lệ chụp lại, thời gian/lượt, số khung xử lý. [NIST đánh giá chất lượng ảnh](https://pages.nist.gov/frvt/html/frvt_quality.html) như một yếu tố liên quan đến lỗi nhận dạng, nhưng tác dụng trong bối cảnh này phải đo bằng dữ liệu của nhóm.

### H3. Ảnh đăng ký và căn chỉnh

- **Thành phần:** phía ảnh tham chiếu và crop/alignment hai phía.
- **Vấn đề cần thấy:** ảnh đăng ký cũ, sai góc/khung, căn chỉnh không ổn định.
- **Lựa chọn thử:** một ảnh đăng ký so với nhiều ảnh **nếu được phép có**; quy tắc chọn ảnh đăng ký; căn chỉnh theo landmark so với crop đơn giản với cùng embedding.
- **Dữ liệu cần:** nhiều ảnh đăng ký/người ở các thời điểm; nếu chỉ có một ảnh, hướng này không đủ điều kiện.
- **Đo:** FMR/FNMR, tỷ lệ không tạo được embedding, chi phí đăng ký và giới hạn lưu dữ liệu.

### H4. Ngưỡng xác minh, chất lượng và chính sách thử lại

- **Thành phần:** bước quyết định sau điểm tương đồng.
- **Vấn đề cần thấy:** nhận nhầm khi ngưỡng thấp; bỏ sót/chuyển thủ công nhiều khi ngưỡng cao; ảnh chất lượng thấp không nên được xử lý như ảnh rõ.
- **Lựa chọn thử:** dò lưới ngưỡng cố định làm đối chứng; thêm ngưỡng chất lượng, số lần thử tối đa và vùng “chuyển giám thị”; nếu dùng PSO/GA/Bayesian Optimization hoặc thuật toán khác, chỉ dùng khi không gian lựa chọn và chi phí tìm kiếm biện minh được, so với dò lưới trên cùng ngân sách.
- **Hàm mục tiêu dự kiến:** giảm FNMR, tỷ lệ chuyển thủ công và thời gian **với ràng buộc FMR không vượt mức do nghiệp vụ chọn**. Nếu nhiều mục tiêu xung đột, báo đường đánh đổi thay vì trộn bằng trọng số tùy ý. Không đặt trước một con số FMR khi chưa có dữ liệu đủ để ước lượng.
- **Đo:** FMR/FNMR trên tập kiểm tra chưa dùng để chọn ngưỡng, tỷ lệ xử lý thủ công, chụp lại và thời gian. [NIST dùng FMR/FNMR tại ngưỡng trong đánh giá 1:1](https://pages.nist.gov/frvt/html/frvt11.html).

### H5. Thời gian và kích thước trên điện thoại

- **Thành phần:** detector/embedding/runtime sau khi biết bước nào chiếm thời gian.
- **Vấn đề cần thấy:** chờ lâu, nóng máy, bộ nhớ hoặc kích thước không phù hợp khi nhiều lượt liên tục.
- **Lựa chọn thử:** model gọn có quyền dùng; giảm độ phân giải đầu vào trong giới hạn không làm mất mặt; lượng tử hóa/chuyển runtime; chỉ thử khi pipeline đã có metric chất lượng đáng tin.
- **Đo:** lỗi xác minh và chọn mặt trên **cùng tập** trước/sau, p50/p95 thời gian mỗi lượt, bộ nhớ, kích thước và tốc độ sau nhiều lượt liên tiếp trên cùng điện thoại. Không dùng thời gian CPU máy tính thay cho đo mobile.

### H6. Chống giả mạo là hướng riêng có điều kiện

Nếu sản phẩm chỉ hỗ trợ giám thị đứng tại cửa, nghi giả mạo phải có luồng chuyển người xử lý; không được tuyên bố hệ thống đã chống giả mạo chỉ nhờ face matching. Nếu hướng nghiên cứu chọn PAD, cần nêu loại tấn công (ảnh in, màn hình, video...), dữ liệu cùng điều kiện camera, baseline PAD và metric lỗi chấp nhận tấn công/lỗi từ chối người thật. [NIST có đánh giá PAD riêng](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based). Hướng này có thể vượt nguồn lực nếu đồng thời tối ưu nhận dạng và mobile.

## 5. Giao thức thí nghiệm và metric

**Chia dữ liệu:** tạo tập phát triển để chọn model/ngưỡng và tập kiểm tra cuối độc lập về người hoặc phiên; ảnh đăng ký của mỗi người kiểm tra là một phần bắt buộc của tác vụ 1:1, nhưng lượt qua cửa của tập kiểm tra không được dùng để chỉnh ngưỡng. Với ít người, phải báo độ bất định và tránh nói đã đo được lỗi rất hiếm. Tách theo ngày/thiết bị nếu có thể. Không cho các khung gần như trùng từ một lượt rơi vào cả tập phát triển và kiểm tra.

**Cặp thử:** đúng người khai báo đúng mã; sai người khai báo mã của người khác; mã không tồn tại; hồ sơ đúng người nhưng sai phòng/ca; nhiều người trong nền; khẩu trang/ánh sáng xấu; lượt vào trùng. Tách lỗi nhận dạng khỏi lỗi quy tắc nghiệp vụ để biết phần nào cần tối ưu.

**Metric chính:** FMR và FNMR cho xác minh 1:1; tại cấp lượt vào là tỷ lệ đề xuất chấp nhận sai người, tỷ lệ người hợp lệ bị chuyển thủ công hoặc chụp lại, tỷ lệ chọn sai mặt và lỗi sai phòng/ca/trùng lượt. Metric vận hành: thời gian mỗi lượt, hàng chờ trong pilot, tỷ lệ ngoại lệ giám thị phải xử lý, độ trễ p95/bộ nhớ trên mobile. Với khẩu trang, ánh sáng và số người nền, báo riêng từng nhóm điều kiện nếu mẫu đủ.

**Đối chứng:** baseline và đề xuất dùng cùng ảnh đăng ký, lượt kiểm tra, cách chia, metric và thiết bị. Nếu đổi nhiều thành phần, làm ablation: B0; chỉ thay H1; chỉ thay H2; H1+H2. Giữ nguyên các phần khác. Không lấy kết quả LFW so trực tiếp với dữ liệu cửa phòng để tuyên bố cải thiện.

## 6. Chi phí, rủi ro và điều kiện chọn hướng chính

H1/H2 cần công sức ghi nhãn ảnh nguyên khung và thu video nhưng gần vấn đề tại cửa nhất. H3 cần nhiều ảnh đăng ký có quyền dùng. H4 rẻ hơn về huấn luyện nhưng rất dễ thành “chỉ chỉnh ngưỡng”; cần đối chứng đơn giản và câu hỏi nghiên cứu rõ. H5 cần điện thoại mục tiêu để đo thực, có rủi ro thay model làm nhiễu tác động. H6 cần dữ liệu tấn công và giao thức riêng, có thể thành đề tài khác.

**Ưu tiên khảo sát đầu tiên của Quốc An:** kiểm tra baseline đầu-cuối trên dữ liệu nguyên khung để xem lỗi có tập trung ở chọn đúng mặt và chất lượng khung (H1/H2) không. Nếu không, đổi trọng tâm theo số liệu sang H3/H4/H5. Hướng đóng góp chính chỉ chọn sau khi biết dữ liệu, giấy phép, lỗi baseline, ngân sách chạy và khả năng đo mobile. Các hướng còn lại là phương án dự phòng hoặc mở rộng.

**Điều kiện để so sánh với đề xuất Minh Hy:** hai bên phải trình bày cùng mức đầy đủ: use case, dữ liệu/quyền dùng, pipeline, baseline, điểm lỗi, lựa chọn cải thiện, objective/metric, chi phí và rủi ro. Chưa ghi một quyết định nhóm khi T-003/T-006 chưa được trình bày.
