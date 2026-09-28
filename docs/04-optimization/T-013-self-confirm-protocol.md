# T-013 — Quy trình self-confirm nhãn pilot S4

**Thời điểm khóa quy tắc:** 2026-09-28, sau lượt xem ảnh sơ bộ 24 scene nhưng **trước khi tính điểm embedding cho phép kiểm chéo này**. Quy trình thay bước review của người thứ hai theo quyết định mới của Quốc An. Không gọi nhãn thu được là ground truth độc lập.

## Phạm vi

Đầu vào giữ nguyên 24 scene XQLFW đã chọn bằng seed `T-013-v1`, reference cùng identity và reference khác identity trong manifest riêng. Không chọn lại scene/reference theo điểm model. Mục đích là quyết định scene nào đủ nhất quán để **thiết kế** benchmark S4 ở T-014; pilot đã xem chỉ thuộc development, không là evaluation khóa và không đo hiệu năng phương pháp S4.

Ba nguồn kiểm **khác vai trò**:

1. **Metadata XQLFW:** ảnh scene/reference tồn tại trong archive đã pin hash; scene và present-reference có cùng identity folder và là genuine pair trong protocol; absent-reference thuộc folder identity khác. Metadata là nhãn nguồn ở mức ảnh, không gán người cụ thể cho từng box trong cảnh và có thể có lỗi nhãn.
2. **Ảnh gốc:** xem người thật khác nhau trong scene, người nào trùng reference, reference có mục tiêu rõ không, và người của absent-reference có nhìn thấy không. Ghi `ambiguous` nếu không thể chỉ duy nhất một người hoặc khẳng định vắng mặt. Kết quả xem ảnh sơ bộ ở [T-013](T-013-target-selection.md) là đầu vào thị giác; không sửa nó dựa trên điểm embedding.
3. **Embedding B0 phụ trợ:** chạy lại đúng SCRFD-500MF + MobileFaceNet từ `buffalo_sc` với cấu hình B0; chỉ tính cosine trên các detection. Không dùng dự đoán này để tạo nhãn người, chọn lại reference, đặt threshold hay phân xử ảnh mơ hồ.

## Quy tắc trước khi xem điểm

- Một scene chỉ là ứng viên S4 nhiều người nếu audit ảnh gốc thấy ≥2 người thật. `sample-05` bị loại khỏi tập này dù detector có >1 box. `03, 19, 21` giữ `ambiguous` vì thị giác không xác định chắc mặt mục tiêu.
- Kiểm hash archive/pairs/weight; ảnh cục bộ phải trùng byte với thành viên archive. Quan hệ genuine và identity folder phải khớp. Bất kỳ sai lệch metadata nào làm ca `ambiguous`, không suy nhãn từ embedding.
- Để kiểm chéo embedding, ảnh reference phải có **đúng một detection** với embedding hợp lệ. Scene phải có cùng số box và vị trí gần như trùng với lượt pilot; mục tiêu do lượt xem ảnh đã chỉ phải ứng với một detection. Thiếu điều kiện nào thì `ambiguous` cho quan hệ đó. Không đổi reference sau khi thấy điểm.
- **Target-present:** trong scene nhiều người và mục tiêu thị giác rõ, similarity của detection đã chỉ với present-reference phải **đứng đầu nghiêm ngặt** trong các detection của cùng scene. Không đặt ngưỡng score/margin; hòa điểm hoặc đứng sau người khác là tín hiệu mâu thuẫn → `ambiguous`. Metadata + thị giác + rank phải cùng nhất quán mới giữ tạm ca present.
- **Target-absent:** metadata khác identity và mắt không thấy người của absent-reference. Reference absent phải có một detection. Để kiểm chéo phụ, cosine lớn nhất của absent-reference với mọi face scene phải **thấp hơn** cosine của present-reference với mặt mục tiêu đã self-confirm trong cùng scene. Nếu không có positive anchor hoặc điều kiện tương đối này sai, ghi `ambiguous`. Điều kiện tương đối chỉ là tín hiệu cảnh báo, **không chứng minh một người vắng mặt**.
- Không ghép `ambiguous` thành `ABSENT`; không bỏ ca mơ hồ khỏi báo cáo số đếm pilot. Chỉ các ca vượt cả ba nguồn mới là `SELF_CONFIRMED` ở mức proxy, không phải nhãn độc lập. Kết quả chi tiết theo identity, bbox và score ở ngoài Git; repo chỉ ghi mẫu số và mã mẫu không định danh.

## Kết quả cần ghi sau run

Báo riêng số scene `MULTI / NOT_MULTI / AMBIGUOUS`, số quan hệ present/absent `SELF_CONFIRMED / AMBIGUOUS` và nguyên nhân: visual, metadata, reference, rerun box, rank, absent cross-check. Ghi danh sách mã mẫu mơ hồ để loại khỏi tập đánh giá khóa. Nếu self-confirm còn quá ít hoặc thiên lệch chỉ về ảnh dễ, T-014 phải ghi giới hạn và cân nhắc nguồn/proxy khác; không nới quy tắc sau khi xem score.

## Giới hạn và bước sau

Đây là **self-confirm có kiểm soát**, không có người gán nhãn độc lập. Cùng một pipeline B0 vừa chọn mẫu nhiều detection vừa cho tín hiệu embedding phụ, nên có nguy cơ bias và lỗi tương quan. Nhãn identity folder/pairs của XQLFW không khẳng định mọi mặt nền trong ảnh; ảnh web 250×250 không đại diện phòng thi. T-014 chỉ được khóa protocol development/evaluation tách identity, target-present/absent và phép so S4–B0 sau khi biết kết quả self-confirm; không dùng 24 pilot identity để báo hiệu năng held-out.
