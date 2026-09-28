# T-013 — Kiểm tính khả thi của phép thử chọn đúng mặt mục tiêu S4

**Trạng thái:** đã audit pilot 24 cảnh một lượt và ghi tiêu chí giữ/loại; đề xuất chọn **S4 chọn mặt mục tiêu** làm điểm cải thiện chính để thiết kế protocol T-014; cần nhóm kiểm lại nhãn trước khi báo benchmark. Chưa chọn phương pháp S4 hay thuật toán tối ưu. **Người phụ trách:** Quốc An; Minh Hy review theo Sheet. **Phạm vi dữ liệu:** dùng ảnh công khai đã có, không thu ảnh/video kỳ thi.

## Vì sao cần bước này

[B0](../03-baseline/T-012-B0-pipeline-choice.md) đã chạy chuỗi ảnh → SCRFD → A0 chỉ chấp nhận đúng một detection → MBF xác minh 1:1 trên XQLFW. [Chẩn đoán T-012](../03-baseline/T-012-B0-freeze-and-stage-diagnosis.md) ghi 908/7.263 ảnh có hơn một detection và 1.785/6.000 cặp `unresolved`; trong 1.399 cặp `unresolved` có ít nhất một ảnh nhiều detection. Đây là kết quả **detector/rule trên ảnh web**: 908 không đồng nghĩa 908 cảnh nhiều người thật. Mục tiêu nghiệp vụ từ [T-008](../01-problem/T-008-requirements.md) là đưa đúng người đã khai hồ sơ sang xác minh 1:1 khi camera thấy nhiều mặt.

**Câu hỏi T-013:** có thể dùng ảnh XQLFW công khai để tạo benchmark nhỏ nhưng có ground truth độc lập cho `reference identity A + scene nhiều mặt → mặt của A hoặc NONE` không? Chỉ khi trả lời câu hỏi dữ liệu/nhãn này mới thiết kế phương pháp S4 ở T-014.

## Đơn vị thử và nhãn cần kiểm

- Một đơn vị là **ảnh tham chiếu của identity A + ảnh scene công khai**. “A đã khai hồ sơ” được mô phỏng bằng việc đưa reference A vào input; không tuyên bố có sự kiện gõ mã trong dataset.
- `target-present`: người A có mặt trong scene; nhãn là một face cụ thể của A, độc lập với box/score do B0 hoặc candidate xuất ra. Nếu A có mặt nhưng detector bỏ sót, trường hợp vẫn ở benchmark để đo failure.
- `target-absent`: A không có trong scene; đáp án S4 là `NONE`/chưa chọn người. Không tự tạo nhãn absent chỉ vì tên thư mục ảnh khác A; phải kiểm người trong scene.
- `ambiguous/unusable`: không phân biệt được A, nguồn ảnh quá mơ hồ hoặc thiếu reference tin cậy; tách và báo mẫu số, không ép thành nhãn đúng/sai.
- Một ảnh có nhiều **detection** chỉ là ứng viên audit. Kiểm trực quan thành `true multi-person`, `false extra detection`, `ambiguous/unusable`. Ảnh chỉ có một người nhưng box trùng/sai không được báo là cảnh nhiều người.

## Pilot khóa trước khi xem ảnh

1. Dùng đúng archive/pairs/weight có SHA-256 ở [A-001/A-002](../00-project/external-assets.md) và cấu hình detector B0 (`SCRFD-500MF`, `640×640`, threshold `0,5`). Chỉ quét 7.263 ảnh thuộc 6.000 cặp gốc; không dùng output model làm ground truth.
2. Sắp ảnh bằng SHA-256 của `T-013-v1` + tên entry ZIP; quét tối đa 600 ảnh đầu theo thứ tự này. Chọn 24 ảnh đầu có hơn một detection, có ảnh reference cùng identity khác file trong genuine pairs, và **mỗi identity tối đa một scene**. Nếu không đủ 24, ghi số thật; không thay seed sau khi xem ảnh. Script chỉ hỗ trợ audit, không chấm phương pháp S4.
3. Với mỗi scene chọn một reference cùng identity và một reference identity khác làm ca absent ứng viên. Kiểm độc lập từ ảnh gốc: có ≥2 người thật không, người A nào là mục tiêu, người của reference absent có thực sự vắng không, reference có đủ rõ không. Không dùng similarity của B0 để điền nhãn. Ghi `ambiguous` nếu không thể xác định.
4. Ảnh, tên identity, bbox theo người và manifest từng mẫu ở thư mục tạm **ngoài Git**. Repository chỉ nhận quy tắc chọn mẫu, hash nguồn và số đếm tổng hợp không định danh. Không commit ảnh, embedding, weight hoặc nhãn theo người.

Pilot chỉ kiểm **khả năng dựng benchmark**; 24 ảnh không phải test cuối và không dùng để xếp hạng candidate. Nếu nguồn hợp lệ, T-014 phải khóa benchmark rộng hơn: ca target-present/absent và một mặt/nhiều mặt, identity-disjoint development/evaluation, cùng scene/reference cho B0 và phương pháp mới. XQLFW pair-fold gốc chia sẻ identity nên không được dùng nguyên trạng để tuyên bố tách danh tính.

## Điều kiện đi tiếp và phương án dự phòng

Đi tiếp S4 trên XQLFW nếu pilot cho thấy có cảnh nhiều **người thật**, target và ca absent có thể gán nhãn độc lập, reference khác ảnh scene, và còn đủ identity để tách development/evaluation. Ghi cả số hợp lệ/lỗi/mơ hồ; không tự đặt một tỷ lệ “đạt” sau khi xem ảnh. Nếu phần lớn multi-detection là box thừa, target không thể gán nhãn hoặc không thể tách identity, thử một benchmark **ghép có kiểm soát từ ảnh danh tính công khai đã có** và gọi đúng là dữ liệu ghép. Không chuyển proxy LTFT box-only thành kết quả pipeline có ảnh. Nếu cả hai nguồn không tạo được nhãn đáng tin, T-013 ghi S4 chưa đo được trong phạm vi dữ liệu hiện có và đề xuất một lỗi B0 khác có thể đo; không chọn model thay thế chỉ vì benchmark thuận tiện.

**Metric dành cho T-014, chưa đo ở T-013:** `correct-target / wrong-target / unresolved` trên toàn bộ scene đủ nhãn, báo riêng target-present và target-absent; nếu nối 1:1 thì thêm FA/FR và coverage trên cùng mẫu, thời gian trên cùng runner. B0 A0 là đối chứng bất biến: nhiều detection → `unresolved`. Một phương pháp chỉ có ích khi tăng kết luận đúng mà đánh đổi chọn sai/chưa kết luận được báo rõ.

## Kết quả pilot 28/09/2026

Chạy [`t013_xqlfw_multiface_audit.py`](../../scripts/t013_xqlfw_multiface_audit.py) với seed `T-013-v1`, tối đa 600 ảnh, mục tiêu 24 scene/mỗi identity một scene. Archive XQLFW, pairs và pack `buffalo_sc` đều khớp SHA-256 B0; Python 3.12, OpenCV 5.0.0, ONNX Runtime 1.20.1, InsightFace 0.7.3, CPUExecutionProvider. Script dừng sau **343 ảnh** vì đã chọn được **24 scene / 24 identity**. Trong 343 ảnh quét: 283 một detection, 21 không detection, 39 nhiều detection. Hai mươi bốn scene thỏa điều kiện có genuine-pair reference khác ảnh; 39 chỉ là số detection, không là số cảnh nhiều người.

Kiểm trực quan ảnh scene và reference của đúng 24 mẫu đã khóa, **một lượt đánh giá sơ bộ bởi Codex, chưa có người kiểm độc lập**:

| Phân loại sơ bộ | Số scene | Ý nghĩa |
|---|---:|---|
| Có nhiều người và đối chiếu reference thấy mục tiêu đủ rõ để chỉ một mặt | 20 | Có cơ sở dựng ca target-present; trong 20 ca này có 1 ca target nằm ở detection thứ hai, nên không thể lấy box đầu làm nhãn. |
| Có nhiều người nhưng mặt mục tiêu/reference quá mơ hồ để gán chắc | 3 | Giữ `ambiguous`, không ép thành đúng/sai. |
| Detection bổ sung không phải một người thật rõ trong scene | 1 | Giữ riêng lỗi detector/ảnh; không gọi là ca nhiều người. |

Chạy đúng detector B0 trên 24 reference target-present: **20/24** ảnh có một detection, 4/24 có hai; trong 20 scene target-present rõ, **16** có reference một detection để bắt đầu phép thử pipeline không cần sửa cách xử lý reference. Với reference identity khác làm **ứng viên target-absent**, 21/24 ảnh có một detection, 1 không detection và 2 có hai; trong 23 scene nhiều người thật, **20** có absent-reference một detection. Kiểm trực quan sơ bộ không thấy người của absent-reference trong 24 scene, nhưng đây **chưa là nhãn absent đã xác nhận độc lập**. Các ca reference nhiều/không detection không bị xóa khỏi audit; T-014 cần chọn reference khác cùng identity hoặc báo riêng.

Ảnh XQLFW trong pilot là JPG 250×250 có người nền nhỏ, ảnh mờ và góc nhìn khác nhau; chúng là proxy học thuật hợp lý cho câu hỏi **chọn mặt từ nhiều detection**, không đại diện tần suất lỗi tại cửa phòng thi. Những identity/ảnh đã xem trong pilot là **development**, không được tái dùng làm test khóa. File ảnh, tên identity, bbox và phân loại từng mẫu chỉ ở thư mục tạm ngoài Git; [handoff T-013](../handoffs/T-013-s4-feasibility.md) ghi cách tạo lại và giới hạn.

## Audit 24 cảnh pilot: tiêu chí giữ/loại

Audit này xét **ảnh scene gốc cùng reference gốc**, không dùng điểm tương đồng hay vị trí box của B0 để suy ra danh tính. Mã `sample-01`…`sample-24` là thứ tự chọn mẫu cố định; ảnh, tên người và box chi tiết vẫn ở thư mục tạm ngoài Git. Đây là một lượt audit bởi Codex, **chưa phải nhãn độc lập được nhóm xác nhận**.

| Quyết định audit | Tiêu chí | Xử lý |
|---|---|---|
| Giữ tạm cho `target-present` nhiều người | Scene có ít nhất hai người thật có mặt nhìn được; reference khác ảnh scene; bằng mắt có thể chỉ **duy nhất một** người tương ứng với reference mà không dựa vào kết quả S4/B0. | Đủ tư cách làm ứng viên benchmark; người thứ hai phải xác nhận mặt mục tiêu trên ảnh gốc trước khi khóa nhãn. |
| Tạm giữ, chưa gán nhãn | Có nhiều người nhưng mặt trong scene hoặc reference quá mờ/che/cắt; hai người có thể bị nhầm, hoặc không thể khẳng định target hiện diện. | Ghi `ambiguous`; không chấm đúng/sai và không lén chuyển sang `target-absent`. Có thể thử reference khác cùng identity ở T-014, nhưng phải ghi rõ thay đổi. |
| Loại khỏi tập **nhiều người** | Detection thứ hai là ảnh nền/box thừa hoặc không xác nhận được một người thứ hai trong scene. | Báo riêng lỗi detector/scene; không tính vào mẫu số phép so S4 nhiều người. Vẫn giữ record audit để giải thích việc loại. |
| Ứng viên `target-absent` | Reference từ identity khác và kiểm bằng mắt rằng không người nào trong scene là identity đó. | Chỉ khóa nhãn `NONE` sau khi người kiểm độc lập xác nhận; tên thư mục khác nhau tự nó không chứng minh vắng mặt. |

| Mã mẫu | Kết luận audit một lượt | Lý do/xử lý |
|---|---|---|
| `01, 02, 04, 06–18, 20, 22–24` (20 cảnh) | **Giữ tạm**: nhiều người, target-present có thể chỉ một mặt. | Không phải nhãn cuối; `sample-11` cho thấy target không nhất thiết ở detection đầu. Trong 20 cảnh này, 16 reference hiện có chỉ có một detection khi chạy B0; 4 reference còn lại cần báo riêng hoặc thay reference trước phép đo toàn pipeline. |
| `03` | **Tạm giữ — không gán chắc.** | Mặt/người ở rìa scene bị cắt; reference quá mờ so với các mặt trong scene. Không thể chỉ một target duy nhất đáng tin. |
| `19` | **Tạm giữ — không gán chắc.** | Reference mờ và người ở rìa scene chỉ hiện một phần; chưa thể xác nhận đúng người nào. |
| `21` | **Tạm giữ — không gán chắc.** | Scene mờ, mặt mục tiêu có thể nhầm với người ở nền; đối chiếu reference chưa đủ chắc. |
| `05` | **Loại khỏi tập nhiều người.** | Chỉ thấy một người thật rõ trong scene; detection thêm gắn với chi tiết/ảnh nền. Giữ ở nhóm lỗi extra detection. |

Với 24 reference khác identity dùng cho ca absent, lượt xem sơ bộ **không thấy** người của reference trong scene; **0/24 nhãn absent được coi là đã xác nhận độc lập**. Vì vậy pilot hiện có **20 ca present đủ hứa hẹn, 3 ca present chưa thể gán chắc, 1 ca không thuộc tập nhiều người**, cùng 24 ca absent *ứng viên*; đây không phải tỷ lệ hiệu năng và không ngoại suy sang 908 ảnh nhiều detection của B0. Những cảnh mơ hồ vẫn nằm trong audit denominator 24, nhưng sẽ không nằm trong denominator chấm chọn target nếu không được giải quyết trước khi khóa benchmark.

**Điều kiện hoàn tất nhãn:** theo [gói và biểu mẫu kiểm độc lập](T-013-independent-label-review.md), người kiểm thứ hai xem scene/reference gốc, độc lập ghi `present + mặt mục tiêu`, `absent`, `ambiguous` hoặc `không nhiều người`, kèm lý do khi bất đồng. Nếu hai lượt không thống nhất, giữ `ambiguous` hoặc cùng xem lại trước khi khóa; không dùng dự đoán của candidate để phân xử. T-014 sẽ quy định protocol/split/metric và cách xử lý các ca còn thiếu sau audit này, rồi mới chạy so S4 với B0.

## Quyết định đề xuất cho bước sau

Pilot cho thấy **có triển vọng dựng nhãn target-present và target-absent từ ảnh công khai**, sau bước xác nhận độc lập mà không cần sự kiện gõ mã thật: reference mô phỏng hồ sơ đã khai, scene giữ các mặt nền. Vì S4 trực tiếp nối nhu cầu nghiệp vụ với nhánh B0 đang `unresolved` khi nhiều mặt, **chọn S4 làm mục tiêu cải thiện chính để thiết kế T-014**. Đây là quyết định về *câu hỏi có thể đo*, không phải chọn cách chọn mặt, model, threshold hay tuyên bố cải thiện.

Trước run so B0/proposed, T-014 phải (1) quy định kiểm nhãn độc lập và phân xử bất đồng từ audit T-013, (2) mở rộng mẫu target-present/absent và một/nhiều mặt với identity-disjoint development/evaluation, (3) định nghĩa riêng trường hợp target có mặt nhưng detector bỏ sót và case reference không hợp lệ, (4) giữ cùng scene/reference/detector/encoder khi chỉ thử S4, (5) báo đúng/sai/chưa kết luận trên toàn bộ mẫu và hậu quả FA/FR sau verification. Nếu nhãn mở rộng không đạt độ tin cậy, dùng dữ liệu ghép có kiểm soát **như một proxy riêng**, hoặc quay lại mục tiêu B0 khác; không chạy candidate S4 trên nhãn suy từ chính model.
