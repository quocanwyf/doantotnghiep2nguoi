# T-023 — MobileFaceNet development trên BFW hard-negative proxy

**Câu hỏi:** Có bằng chứng rằng representation MobileFaceNet hiện tại không thể tách genuine khỏi non-target mà S4/P2 dễ chọn, đến mức cần thay hoặc fine-tune model không?

**Phạm vi:** Ảnh BFW công khai được ghép thành hai panel có identity nguồn biết trước; không phải cảnh cửa phòng. Benchmark [khóa trước score](../04-optimization/T-023-encoder-assessment-protocol.md), SHA-256 `d586d97f1656a7f83b5ae37410b87ff0a0a95997e687d0ed47673205a38aec3b`. Không dùng sample/score/ground truth evaluation T-022 để tạo tập hoặc chọn ngưỡng. MobileFaceNet `buffalo_sc` và P2 `τ=0,14789717107158995`, `δ=0,07647264965285691` giữ nguyên. Raw development ngoài Git SHA-256 `21596e6565fbd6aa3b6d41e7c25b38a49012fba53e3b5c16bd3b7c8b0425c908`; summary SHA-256 `e78f193235a6fd8d91e1cdf2a256afc82104487ec163b241ca234d8a74a2a69b`. Evaluation chưa mở tại thời điểm viết.

## Mẫu số và phân bố

| Nhóm development | n | min | p05 | median | p95 | max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Genuine pair | 239 | 0,0041 | 0,1481 | 0,4299 | 0,6539 | 0,7897 |
| Ordinary impostor pair | 240 | -0,1485 | -0,1027 | 0,0003 | 0,1230 | 0,1992 |
| Genuine được P2 chọn đúng | 57 | 0,1835 | 0,2479 | 0,4221 | 0,6323 | 0,6544 |
| Hard negative P2 chọn từ cảnh absent | 41 | 0,1487 | 0,1513 | 0,2044 | 0,2910 | 0,3283 |

P2 chọn đúng 57/60 present, unresolved 3; trên **238 absent**, P2 no-select 197 và false-select 41 (random 5/119, challenge 36/119). Challenge được làm giàu bằng score SENet50 từ nguồn, nên **không** dùng 41/238 làm xác suất gặp lỗi ngoài thực địa. Hard negative có 41 trial thuộc 30 anchor, không phải 41 người độc lập. Khoảng điểm chung giữa selected genuine và hard negative là `0,1835–0,3283`: 11/57 selected genuine và 27/41 hard negative nằm trong khoảng này. Có overlap thật, nhưng không đủ để kết luận một ngưỡng bất kỳ đều vô dụng.

## Trade-off S8 trên development

Quy tắc S8 tham chiếu: accept nếu cosine của **chính mặt P2 chọn** so với reference `≥ θ`; cùng signal với S4, không giả là lớp bằng chứng độc lập. FMR = impostor pair accept / impostor pair; FNMR = genuine pair reject / genuine pair. Hard-negative accept có điều kiện chỉ tính trên 41 face P2 false-select. Tất cả mẫu số là cặp/cảnh proxy, không là lượt check-in.

| θ | Genuine FNMR | Ordinary FMR | Selected genuine accept | Hard negative accept | Absent: no-select / S8 reject / S8 accept |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0,122254 (mốc T-020) | 8/239 | 14/240 | 57/57 | 41/41 | 197 / 0 / 41 |
| 0,15 (mốc T-022) | 13/239 | 4/240 | 57/57 | 40/41 | 197 / 1 / 40 |
| 0,20 | 20/239 | 0/240 | 55/57 | 24/41 | 197 / 17 / 24 |
| 0,23 | 25/239 | 0/240 | 55/57 | 11/41 | 197 / 30 / 11 |
| 0,25 (stress point) | 30/239 | 0/240 | 53/57 | 10/41 | 197 / 31 / 10 |

**Diễn giải:** ordinary impostor thấp hơn hard negative rất rõ trong tập này; báo ordinary FMR một mình sẽ che lỗi sau S4. Nâng θ từ 0,15 lên 0,23 chặn thêm 29/41 hard negative được P2 chọn, nhưng genuine pair reject tăng từ 13 lên 25/239 và 2/57 selected genuine bị reject. Vẫn còn **11/41 hard negative được accept**, không thể gọi là an toàn. T-023 chỉ xác định có một vùng trade-off đáng kiểm trên holdout; chưa chứng minh MobileFaceNet đủ cho demo hay cần thay.

## Rule nghiên cứu được khóa sau development, trước evaluation

Trên grid đã công bố `[-1,1]` bước 0,01, chỉ xét điểm giữ selected-genuine accept **≥95%**; trong đó giảm số S4-derived hard-negative accept nhiều nhất. Hòa thì giảm genuine-pair FNMR, tiếp theo ordinary FMR, cuối cùng chọn θ nhỏ hơn. Rule này chọn `θ_research=0,23` trên development: 55/57 selected genuine accept, 11/41 hard negative accept. `95%` là **research screen** để thấy trade-off, không là yêu cầu nghiệp vụ hay deployment cap. Giữ `0,15` làm mốc lịch sử, `0,25` là stress point. [Freeze](T-023-evaluation-freeze.md) ghi code/data/hash trước khi mở evaluation; không chọn lại θ theo holdout.

## Giới hạn và câu hỏi holdout

BFW là ảnh mặt nguồn web, scene hai panel ghép, SENet50 làm giàu challenge và cùng một anchor tạo nhiều pair/trial; không suy ra real-world FAR. Một người tự rà scene, không có kiểm nhãn độc lập; pair thường không visual-check từng cặp. BFW có thể chồng identity với dữ liệu train của MobileFaceNet, chưa kiểm được. Holdout cần hỏi: với identity BFW chưa thấy, số hard negative có đủ và trade-off θ=0,23 có lặp không? Chỉ khi holdout cho thấy không có operating region hữu ích mới có căn cứ đề xuất thí nghiệm encoder khác/fine-tune. Không tự chọn model trong T-023.
