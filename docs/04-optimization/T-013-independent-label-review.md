# T-013 — Hướng dẫn kiểm nhãn pilot độc lập

**Mục đích:** xác nhận liệu 24 cảnh pilot có dùng được để dựng phép thử chọn mặt mục tiêu hay không. Đây là kiểm **nhãn dữ liệu**, không chấm S4, không chọn model và không thay thế benchmark T-014.

## Gói xem ảnh

Chạy `scripts/t013_xqlfw_multiface_audit.py` theo [bàn giao T-013](../handoffs/T-013-s4-feasibility.md) để tạo lại 24 mẫu trong thư mục riêng ngoài Git. Sau đó dùng:

```powershell
py scripts/t013_prepare_blind_review.py --manifest <private-manifest.json> --packet-dir <empty-private-dir> --key-file <private-key-outside-packet.json>
```

Script tạo 24 `case-XX-scene.jpg`, hai ảnh `case-XX-ref-A/B.jpg` cho mỗi cảnh và `review-blank.csv` gồm 48 dòng. Thứ tự cảnh và vị trí A/B được xáo cố định; **key nằm ngoài gói gửi người kiểm**. Không gửi manifest gốc, key, bảng kết luận sơ bộ T-013 hoặc box/score của B0 cho người kiểm trước khi họ nộp nhãn. Ảnh, CSV có vị trí mặt và key đều ở ngoài Git; không commit, không đẩy lên PR.

Gói đã tạo trên máy hiện tại ở `C:\Users\Admin\AppData\Local\Temp\T-013-blind-review-20260928-v1`; key riêng ở cùng thư mục Temp với tên `T-013-review-key-20260928-v1.json`. Người kiểm ở máy khác tự tải archive/weight từ nguồn tác giả, đối chiếu hash rồi tạo lại gói. [Audit quyền T-009](../02-survey/T-009-candidate-audit.md) chưa xác nhận quyền **phân phối lại ảnh XQLFW**, nên không gửi ZIP ảnh hoặc đưa gói lên Git/Drive khi chưa làm rõ quyền đó. Trên cùng máy, người kiểm chỉ mở thư mục gói ẩn nhãn, không mở key/manifest gốc. Đây không phải ảnh kỳ thi; XQLFW chỉ dùng cho phép thử học thuật.

## Cách điền `review-blank.csv`

Mỗi `case_id` có hai dòng, một cho reference A và một cho B. Chỉ xem ba ảnh cùng case. Không xem kết quả audit trước hoặc dùng tên identity/điểm model để trả lời.

| Cột | Giá trị cần điền |
|---|---|
| `scene_people` | `MULTI`: nhìn thấy ≥2 người thật khác nhau; `SINGLE`: chỉ một người, box thừa có thể đến từ ảnh nền; `UNCERTAIN`: ảnh quá mờ/cắt để quyết định. Điền giống nhau ở hai dòng cùng case. |
| `reference_usable` | `YES` nếu reference có một người mục tiêu nhận diện được bằng mắt; `NO` nếu không có hoặc nhiều mặt làm mục tiêu không rõ; `UNCERTAIN` nếu chất lượng không đủ chắc. |
| `relation` | `PRESENT` nếu xác định duy nhất người của reference trong scene; `ABSENT` nếu đã xem các người trong scene và chắc không có; `UNCERTAIN` nếu không phân biệt được. Reference không usable thì `relation=UNCERTAIN`. |
| `target_x_normalized`, `target_y_normalized` | Chỉ điền khi `PRESENT`: tâm mặt được chọn theo tỷ lệ 0–1 trên **ảnh scene gốc**, để đối chiếu người nào được chỉ. Không dùng tọa độ box B0. |
| `reason` | Ghi ngắn lý do khi `SINGLE/UNCERTAIN`, reference không usable hoặc relation chưa chắc; có thể ghi “ảnh nền”, “mặt rìa bị cắt”, “reference mờ”. |
| `reviewer`, `review_date` | Người kiểm và ngày kiểm; không điền tên thí sinh/người trong ảnh. |

Nếu không chắc, dùng `UNCERTAIN`; không suy `ABSENT` chỉ từ tên folder khác nhau. Không sửa ảnh hoặc thay reference trong lượt kiểm này. Ghi mọi lỗi file vào `reason`.

## Đối chiếu sau khi người kiểm nộp

Chỉ sau khi CSV đã điền xong, người tổng hợp mới mở key để nối `case_id` với `sample-XX` và A/B với reference gốc. So với audit một lượt ở [T-013](T-013-target-selection.md):

1. Đếm đủ 24 scene, 48 dòng, trường hợp thiếu và reference không usable.
2. Ghi từng bất đồng về `scene_people`, `PRESENT/ABSENT/UNCERTAIN` hoặc **người được chỉ** trong scene; không gộp bất đồng vào số “đúng”.
3. Nếu bất đồng, hai người xem lại ảnh gốc và ghi quyết định cùng lý do. Nếu vẫn không chắc, giữ `UNCERTAIN` và loại khỏi mẫu số chấm target, nhưng báo số loại.
4. Chỉ chốt nhãn present/absent cho những case được đối chiếu rõ. Pilot đã xem thuộc **development**; T-014 không lấy 24 identity này làm evaluation khóa.

**Đầu ra để T-014 bắt đầu:** số case giữ/loại/mơ hồ sau đối chiếu, bảng bất đồng, quy tắc gán nhãn áp dụng được và danh sách identity pilot để loại khỏi evaluation (danh sách này giữ ngoài Git). T-014 mới khóa protocol target-present/target-absent, split development/evaluation và phép so S4–B0; không dùng pilot này để báo hiệu năng cải thiện.
