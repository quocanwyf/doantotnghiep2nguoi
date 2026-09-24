# Đề xuất use case điểm danh bằng nhận dạng khuôn mặt của Minh Hy

- **Task:** [T-003 trên Sheet chung](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0)
- **Ngày:** 2026-09-24
- **Trạng thái:** Đề xuất để Quốc An review và hai thành viên so sánh ở T-004. Chưa phải phạm vi, model hay dataset đã được nhóm hoặc thầy chốt.
- **Nguồn định hướng:** [Bản ghi do nhóm cung cấp](../sources/dinhhuongdatn.docx) và [tóm tắt phạm vi hiện tại](../00-project/brief.md). Bản ghi không chứng minh mọi ý trong đó đã được thầy xác nhận.

## Tóm tắt đề xuất

Đề xuất ưu tiên **điểm danh đầu giờ cho một lớp bằng điện thoại đặt tại điểm check-in, từng sinh viên đứng trước camera**. Hệ thống nhận dạng người đã đăng ký trong danh sách của phiên học và có quyền từ chối khi không đủ tin cậy. Phương án này giới hạn số mặt trong mỗi lượt, dễ thu dữ liệu đúng bối cảnh và đo lỗi nhận sai, bỏ sót, thời gian xử lý. Phương án thứ hai là ghi nhận nhiều người trong một ảnh lớp; nó gần với ý tưởng quan sát hiện diện nhưng đòi hỏi dữ liệu mặt nhỏ, che khuất, nhiều người cùng khung hình và quy tắc kiểm tra thủ công phức tạp hơn.

Nếu chọn phương án thứ nhất, đề xuất **MobileFaceNet** làm model nhận dạng cần khảo sát. Hai điểm có thể cải thiện theo bản định hướng là **tham số/chính sách huấn luyện** của model và **vùng crop từ bounding box** trước khi đưa mặt vào model. Đây là hai giả thuyết nghiên cứu khác nhau; nhóm cần đo lỗi trước rồi chọn **một** điểm chính để thử nghiệm. Dataset đề xuất gồm **DigiFace-1M cho huấn luyện nghiên cứu**, **ảnh người tham gia đồng ý cung cấp để đăng ký và đánh giá đúng bối cảnh**, và **LFW để kiểm tra tham khảo theo giao thức xác minh cặp ảnh**. Quyền sử dụng và chi phí huấn luyện cần được xác nhận trước khi lấy dữ liệu.

## Use case A — Điểm danh từng người tại điểm check-in (ưu tiên)

| Nội dung | Đề xuất |
| --- | --- |
| Người dùng | Sinh viên đã đăng ký; giảng viên hoặc người phụ trách mở/đóng phiên và xử lý lượt chưa xác minh. |
| Camera và đầu vào | Camera điện thoại ghi luồng hình của **một người chủ động đứng trước máy**. Hệ thống còn cần mã phiên học, danh sách sinh viên hợp lệ và mẫu đăng ký. Chỉ xử lý khi có đúng một mặt đủ rõ. |
| Đầu ra | Một trong các trạng thái: điểm danh thành công với mã người và giờ ghi nhận; đã điểm danh; chưa xác minh được; ảnh không đạt yêu cầu; phiên đã đóng. Người phụ trách xem danh sách đã ghi nhận và các lượt cần xử lý. |
| Cách ghi nhận | Mở phiên → phát hiện/căn chỉnh mặt → MobileFaceNet tạo embedding → so với mẫu của người thuộc phiên → áp ngưỡng được chọn trên dữ liệu phát triển → ghi một bản ghi theo khóa **mã phiên + mã sinh viên**. Không đủ tin cậy hoặc không có trong danh sách thì không tự ghi; cho thử lại hoặc xác nhận thủ công. Sau khi đóng phiên, người chưa có bản ghi hợp lệ được liệt kê để người phụ trách xử lý theo quy định. |
| Ý nghĩa “hiện diện” | Chỉ chứng minh một lượt check-in được ghi nhận tại thời điểm chụp. Không suy ra người đó ở lại cả buổi. |

**Tiêu chí thành công cần đo trên tập test riêng:**

1. Nhận dạng 1:N có quyền từ chối: **FPIR** (người ngoài danh sách vẫn bị gán danh tính) và **FNIR** (người trong danh sách không được nhận đúng) ở ngưỡng đã chọn trước trên validation, theo [định nghĩa đánh giá 1:N của NIST](https://pages.nist.gov/frvt/html/frvt1N.html). Báo cáo riêng theo điều kiện rõ, mờ, thiếu sáng và theo ngày chụp.
2. Nghiệp vụ: tỷ lệ lượt ghi đúng người và đúng phiên; lượt ghi sai; lượt phải xử lý thủ công; **không có bản ghi trùng** cho cùng người trong một phiên. Kiểm thử cả người không đăng ký, không có mặt, nhiều mặt và phiên đã đóng.
3. Triển khai: thời gian từ khi đưa mặt vào khung đến khi trả kết quả (trung vị và p95), kích thước model/app và bộ nhớ trên **điện thoại mục tiêu**. Chưa chọn điện thoại nên chưa đặt ngưỡng hiệu năng chính thức.
4. Nghiên cứu: baseline và proposed được so trên cùng dữ liệu, split, detector, danh sách đăng ký, giao thức, seed và thiết bị; báo cáo cả chi phí tìm kiếm tham số. Chỉ kết luận cải thiện nếu lỗi nhận dạng/điểm danh giảm trên test mà không làm tăng nhận sai người lạ quá mức đã định.

Ngưỡng minh họa để **thảo luận**, không phải yêu cầu đã chốt: FPIR không quá 1%, FNIR không quá 5% và p95 trả kết quả không quá 2 giây trên một thiết bị xác định. Các ngưỡng phải sửa theo quy mô mẫu, khả năng thu dữ liệu và mức rủi ro mà nhóm thống nhất. Ví dụ, 0 lần nhận sai trong 20 lượt người lạ chưa đủ chứng minh FPIR dưới 1%; nếu coi các lượt độc lập, 0 lỗi trong khoảng 299 lượt mới cho cận trên xấp xỉ 1% ở mức tin cậy 95%.

**Giả định chưa xác nhận:** nhà trường/lớp cho phép check-in bằng khuôn mặt; người tham gia đồng ý cung cấp dữ liệu; mỗi lượt có thể yêu cầu một người vào khung; có người phụ trách để xử lý ngoại lệ; quy tắc đi muộn/vắng/có phép được cung cấp; thiết bị và điều kiện mạng được xác định; thầy chấp nhận optimization ở giai đoạn huấn luyện nếu đó là hướng nhóm chọn. Nhận dạng khuôn mặt thông thường **không tự chống được ảnh in hoặc video phát lại**; demo có giám sát chỉ giảm một phần rủi ro, còn hệ thống không giám sát cần nghiên cứu chống giả mạo riêng. [NIST phân loại ảnh in và video phát lại là các kiểu tấn công vào khâu thu nhận khuôn mặt](https://pages.nist.gov/frvt/html/frvt_pad.html).

## Use case B — Ghi nhận nhiều người từ ảnh hoặc video lớp học

| Nội dung | Đề xuất |
| --- | --- |
| Người dùng | Giảng viên hoặc người phụ trách hướng camera vào lớp; sinh viên trong danh sách được đăng ký trước. |
| Camera và đầu vào | Một hoặc vài ảnh/video ngắn từ điện thoại chứa **nhiều người trong cùng khung hình**, cùng mã phiên và danh sách lớp. Mặt có thể nhỏ, nghiêng, bị che và không nhìn camera. |
| Đầu ra | Danh sách người được nhận dạng kèm trạng thái cần xác nhận, số mặt chưa nhận dạng; giảng viên rà soát trước khi ghi danh chính thức. |
| Cách ghi nhận | Phát hiện từng mặt → căn chỉnh và so với danh sách phiên → gộp kết quả lặp qua các khung hình theo cùng danh tính → chỉ ghi khi vượt ngưỡng và được kiểm tra theo quy tắc đã chốt. Không mặc định một mặt thấy trong ảnh đồng nghĩa đã điểm danh cả buổi. |

Tiêu chí cần đo thêm là **recall trên mặt nhỏ**, tỷ lệ người trong lớp được nhận đúng trên mỗi lần chụp, số nhận nhầm và thời gian xử lý một ảnh/phiên. Phương án này có thể bộc lộ lỗi detector và model nhận dạng rõ hơn, nhưng cũng có nguy cơ cao hơn về mặt bị che, dữ liệu khó thu và khó gán nhãn. Vì vậy chỉ nên chọn nếu nhóm có bối cảnh chụp thật và đủ dữ liệu để chứng minh mức cải thiện. Không nên dùng điểm số từ ảnh mặt lớn để suy ra hiệu năng cho ảnh toàn lớp.

**Giả định chưa xác nhận:** có thể chụp toàn lớp với sự đồng ý phù hợp; góc camera/độ phân giải cho mặt đủ lớn; giảng viên chấp nhận rà soát kết quả; thầy muốn xử lý nhiều người trong một lần chụp; điện thoại đáp ứng thời gian xử lý.

## Model đề xuất và điểm yếu cần kiểm chứng

**Model nhận dạng đề xuất:** MobileFaceNet tạo embedding khuôn mặt. Model phát hiện mặt có thể là SCRFD-500MF nếu giấy phép và thử nghiệm trên điện thoại phù hợp; detector được giữ cố định khi so sánh baseline với proposed. [Bài báo MobileFaceNets](https://arxiv.org/abs/1804.07573) thiết kế kiến trúc cho thiết bị di động. [ArcFace](https://openaccess.thecvf.com/content_CVPR_2019/html/Deng_ArcFace_Additive_Angular_Margin_Loss_for_Deep_Face_Recognition_CVPR_2019_paper.html) là một loss có thể dùng khi huấn luyện, không phải bộ nhận dạng thứ hai lúc chạy app.

**Lý do khảo sát:** mobile là đầu ra ứng dụng của định hướng; embedding hỗ trợ thêm người vào danh sách đăng ký mà không buộc huấn luyện lại toàn bộ model sau mỗi lần thêm. Trong [kết quả cùng bộ dữ liệu MS1MV2 do InsightFace công bố](https://github.com/deepinsight/insightface/blob/master/recognition/arcface_torch/README.md), MobileFaceNet-0.45G có điểm MFR-ALL thấp hơn backbone R50 (62,07 so với 75,13). Đây là bằng chứng về đánh đổi năng lực giữa các backbone trong benchmark đó, **không phải số liệu điểm danh của nhóm hay bằng chứng trực tiếp rằng ảnh mờ là nguyên nhân**.

**Giả thuyết điểm yếu:** trên camera dự kiến, ảnh mờ do chuyển động, giảm độ phân giải hoặc thay đổi sáng có thể làm embedding của cùng người kém ổn định. Ngoài ra, bounding box/crop lệch hoặc lấy quá ít/quá nhiều vùng quanh mặt có thể làm đầu vào nhận dạng xấu dù detector vẫn phát hiện được mặt. Nghiên cứu [AdaFace](https://openaccess.thecvf.com/content/CVPR2022/papers/Kim_AdaFace_Quality_Adaptive_Margin_for_Face_Recognition_CVPR_2022_paper.pdf) chỉ ra nhận dạng mặt chất lượng thấp là một bài toán riêng; còn ảnh thực tế của nhóm mới quyết định giả thuyết nào đúng. Cần đo lỗi phát hiện, crop/căn chỉnh và nhận dạng riêng; không gán lỗi detector hoặc ảnh thiếu thông tin cho MobileFaceNet.

### Hai hướng optimization cần so sánh trước khi chọn

| Hướng trong bản định hướng | Điểm yếu cần chứng minh bằng dữ liệu | Biến để thuật toán tìm kiếm | Baseline và proposed phải khác ở đâu? | Bối cảnh có khả năng phù hợp |
| --- | --- | --- | --- | --- |
| **Tham số/chính sách huấn luyện MobileFaceNet** (*training-time*) | Mặt được crop đúng nhưng ảnh chụp thực tế mờ, tối hoặc khác ảnh đăng ký khiến nhận dạng sai/bỏ sót. | Có thể tìm learning rate, weight decay, biên độ ArcFace và/hoặc xác suất, mức độ tăng cường ảnh. Thu hẹp search space sau thử nghiệm đầu; không tìm tất cả cùng lúc. | Giữ kiến trúc, detector, dữ liệu, split, khởi tạo và ngân sách huấn luyện; thuật toán tìm cấu hình trên validation rồi **fine-tune lại model**. So với cấu hình cố định và random search cùng ngân sách. | Use case A, nếu lỗi nằm ở embedding dù crop đã đạt. |
| **Bounding box/ROI trước MobileFaceNet** (*xử lý ảnh/inference*) | Detector tìm được mặt nhưng crop quá chặt, lệch hoặc nhỏ làm giảm chất lượng embedding; trong ảnh lớp có nhiều box không đủ chất lượng. | Tìm độ mở rộng box theo từng chiều, ngưỡng kích thước/chất lượng để xử lý, độ phóng và quy tắc chọn box/vùng cần xử lý. | Giữ detector, trọng số MobileFaceNet và dữ liệu; thay **chính sách chọn/cắt vùng mặt** đã được tìm trên validation. Hiệu chỉnh ngưỡng nhận dạng theo cùng một quy trình để so ở cùng mức FPIR; đo thời gian nếu phải xử lý nhiều crop. | Use case B có mặt nhỏ/nhiều người; cũng có thể áp dụng A nếu thử nghiệm cho thấy lỗi crop. |

Ở hướng **tham số**, thuật toán có thể là Bayesian optimization vì mỗi lần đánh giá phải fine-tune và tốn thời gian. Việc tìm chính sách tăng cường dữ liệu là một ví dụ có cơ sở trong [AutoAugment](https://research.google/pubs/autoaugment-learning-augmentation-policies-from-data/); các biến đổi phải tương tự camera thật và không làm mất danh tính. **Đăng ký embedding không được tính là train/fine-tune.** Nếu chỉ đổi ngưỡng nhận dạng sau khi xem tập test thì đó là rò rỉ dữ liệu, không phải cải thiện model.

Ở hướng **bounding box/ROI**, detector quyết định box ban đầu, còn thuật toán optimization quyết định **vùng nào và cách crop nào được đưa vào MobileFaceNet**. Hướng này cải thiện *pipeline dùng model*, không thay đổi trọng số MobileFaceNet; báo cáo không được gọi đó là “huấn luyện model tốt hơn”. Có thể tìm chính sách offline trên validation rồi áp dụng cố định khi app chạy, hoặc thử chính sách thích ứng theo kích thước/chất lượng box. Cần so với crop cố định đã được tinh chỉnh hợp lý, không chỉ so với một crop mặc định yếu. Nếu thầy yêu cầu train/fine-tune là phần bắt buộc, phải có kế hoạch huấn luyện riêng và đo tác động tách biệt với ROI.

**Cách chọn một hướng chính:** lấy bộ ảnh pilot đúng camera/bối cảnh, gắn nhãn vị trí mặt và danh tính, rồi kiểm tra (1) mặt không được phát hiện, (2) mặt được phát hiện nhưng crop/căn chỉnh sai, (3) crop tốt mà embedding vẫn nhận sai. So sánh thêm với crop do người kiểm tra để ước lượng mức lỗi có thể cứu bằng ROI. Nếu lỗi (2) chiếm đáng kể, thử ROI; nếu lỗi (3) nổi bật, thử tham số huấn luyện. Không khẳng định trước hướng nào chắc chắn cho cải thiện lớn.

**Objective chung:** giảm FNIR ở mức FPIR đã định, đồng thời báo cáo tỷ lệ ghi điểm danh đúng và p95 thời gian xử lý. Tập test cuối phải giữ riêng. Với ROI, nếu độ chính xác tăng do chạy nhiều crop, phải báo thêm chi phí xử lý; với tham số huấn luyện, phải báo chi phí tìm kiếm/fine-tune. Mỗi hướng cần một phép so sánh chỉ thay thành phần đang nghiên cứu.

## Dataset đề xuất và lý do

| Dataset/nguồn | Vai trò đề xuất | Lý do chọn | Điều kiện và giới hạn |
| --- | --- | --- | --- |
| [DigiFace-1M](https://github.com/microsoft/DigiFace1M) | **Ứng viên chính cho huấn luyện nhận dạng** MobileFaceNet trong nghiên cứu. Bắt đầu bằng phần 72 ảnh/người nếu tài nguyên không cho phép dùng toàn bộ; ghi chính xác tập con và seed. | Có nhãn danh tính và nhiều ảnh cho mỗi người; ảnh tổng hợp giảm phụ thuộc vào bộ ảnh thật thu thập từ Internet. [Bài báo gốc](https://openaccess.thecvf.com/content/WACV2023/papers/Bae_DigiFace-1M_1_Million_Digital_Face_Images_for_Face_Recognition_WACV_2023_paper.pdf) nghiên cứu cả khoảng cách từ tổng hợp sang ảnh thật. | [Giấy phép R-UDA](https://github.com/microsoft/DigiFace1M/blob/main/LICENSE) giới hạn ở nghiên cứu phi thương mại. Một tập con nhỏ không tự bảo đảm model đủ tốt; cần ước lượng GPU, dung lượng và hiệu năng sau huấn luyện. |
| Ảnh **người tham gia đồng ý cung cấp** | Đăng ký mẫu; dữ liệu train/fine-tune thực tế nếu đủ và được phép; calibration/validation; **test độc lập** của app điểm danh. | Chỉ nguồn này phản ánh camera, ánh sáng, khoảng cách và người dùng của use case. Phải có cả người **ngoài danh sách** để đo FPIR. | Cần thỏa thuận quyền thu, truy cập, lưu và xóa. Không commit ảnh, danh tính hoặc embedding cá nhân lên Git. Không dùng các khung hình gần nhau của cùng một lượt chụp ở cả train và test. |
| [LFW](https://web.cs.umass.edu/publication/docs/2014/UM-CS-2014-003.pdf) | Benchmark **bổ trợ** cho xác minh cặp ảnh cùng/khác người. | Có giao thức công bố để kiểm tra triển khai model và tham khảo nghiên cứu. | LFW là bài toán cặp ảnh; điểm LFW không thay thế kết quả nhận dạng 1:N và điểm danh trong lớp. Cần tuân theo protocol và điều kiện dùng dữ liệu trước khi báo số liệu. |
| [WIDER FACE](https://shuoyang1213.me/WIDERFACE/) | Chỉ dùng khi cần chẩn đoán/đánh giá **bộ phát hiện mặt**, đặc biệt nếu chọn use case B. | Có nhãn bounding box và phân mức Easy/Medium/Hard. | Không có nhãn danh tính để huấn luyện MobileFaceNet cho điểm danh; trang dự án ghi giấy phép CC BY-NC-ND. |

**Không chọn VGGFace2 làm nguồn huấn luyện chính lúc này:** [trang chính thức của Oxford](https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/) hiện ghi đường tải dataset không còn được cung cấp tại đó. Trọng số pretrained của [InsightFace](https://github.com/deepinsight/insightface/blob/master/python-package/docs/model_zoo.md) có điều kiện dùng nghiên cứu phi thương mại riêng với giấy phép mã nguồn. Nếu dùng trọng số đó cho prototype, phải ghi rõ xuất xứ và không coi nó là model nhóm tự huấn luyện trên DigiFace-1M.

**Phân chia dữ liệu dự kiến:** với người tham gia thật, ảnh đăng ký lấy ở buổi A; ảnh chọn ngưỡng và chính sách ở buổi B; ảnh test ở buổi C khác ngày/điều kiện. Người ngoài danh sách tham gia test cũng cần đồng ý. Với dữ liệu huấn luyện nhận dạng công khai/tổng hợp, không để ảnh hoặc danh tính của tập test đi vào bước tìm tham số hoặc ROI. Cả hai phiên bản phải dùng cùng split, detector và danh sách đăng ký; **cách crop chỉ được thay khi đó chính là biến nghiên cứu**. Ghi seed, phiên bản mã, trọng số khởi tạo, thiết bị và thời gian huấn luyện để so sánh có thể tái lập.

## Điều cần nhóm và thầy xác nhận trước khi chốt

1. Chọn use case A hay B; camera nhận một hay nhiều người mỗi lượt, và “hiện diện” nghĩa là check-in tức thời hay quan sát liên tục?
2. Được thu và dùng dữ liệu khuôn mặt người thật trong phạm vi nào; có được đưa model/ứng dụng demo ra ngoài nhóm không?
3. Yêu cầu train/fine-tune và thuật toán optimization: tối ưu tham số huấn luyện, tối ưu bounding box/ROI ở inference, hay cả hai được chấp nhận ở mức nào? Nếu ROI là đóng góp chính, phần train/fine-tune cần thực hiện ra sao?
4. Điện thoại, hệ điều hành, chạy trên thiết bị hay qua server, mục tiêu thời gian phản hồi và ngân sách GPU là gì?
5. Quy tắc nhận muộn, vắng, điểm danh trùng, nhận sai và xác nhận thủ công do ai quyết định?

Sau khi Quốc An có bản T-002, hai người so sánh hai phương án theo [quy trình giai đoạn 01](README.md) rồi mới ghi phạm vi chính thức ở T-004. Khảo sát model/dataset/optimization trong báo cáo này là **đề xuất sơ bộ** để thấy use case có thể nghiên cứu được, chưa thay thế khảo sát kỹ thuật T-005/T-006 hoặc quyết định T-007.
