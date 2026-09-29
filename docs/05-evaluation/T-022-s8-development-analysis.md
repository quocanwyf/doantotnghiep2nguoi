# T-022 — Phân tích S8 trên development của benchmark controlled XQLFW

**Ngày:** 2026-09-29. **Phạm vi:** development only; evaluation chưa được đọc/chấm. Đây là synthetic/controlled proxy, không phải ca check-in hoặc ước lượng FAR tại cửa phòng thi. [Benchmark và nhãn đã khóa trước score](T-022-controlled-s8-benchmark.md); [T-021](T-021-s8-risk-protocol.md) đặt câu hỏi rủi ro, không cấp một mức false accept chấp nhận được cho demo (`TBD`).

## Observation → question → protocol → evidence → decision

T-020 quan sát S8 replay accept hai non-target do S4/P2 chọn, bởi cùng cosine vượt cả điều kiện S4 và ngưỡng S8. Câu hỏi T-022 là liệu encoder/cosine hiện tại có tách được genuine khỏi ordinary impostor **và** non-target được S4 chọn hay không. Trên manifest T-022 khóa trước score, chạy cùng SCRFD + MobileFaceNet, P2 giữ `τ=0,1478971711`, `δ=0,0764726497`; thử nhiều ngưỡng S8 để **mô tả trade-off**, không chọn ngưỡng mới. Kết quả dưới đây chỉ dẫn đến đề xuất cách kiểm tiếp, không chốt cấu hình.

## Đầu vào, mẫu số và khả năng tái lập

- Manifest khóa SHA-256 `d752c99fae5071c2aedb7fe0e40842b8b25c05decf539b61df8e988fee8ec131`; XQLFW ZIP `1af459679fba23a12f4d83c82a81523eb930a4aec759eebefcbdde69a678962c`; model pack `57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72`. Script `scripts/t022_s8_development.py` xác minh các hash và chỉ chọn `development` từ manifest; không mở ảnh, pair hay score evaluation.
- 3.273 ảnh nguồn development được encode; 1.318 genuine pair, 992 ordinary-impostor pair và 64 scene (32 present, 32 absent) được chấm. Các pair/scene có identity chung trong cùng split; mẫu không độc lập thống kê. `AMBIGUOUS` và detector-excluded giữ nguyên theo benchmark khóa, không đưa vào mẫu số metric.
- CPUExecutionProvider, SCRFD `det_size=640`, `det_thresh=0,5`, MobileFaceNet `112×112`, Python 3.12.2, insightface 0.7.3, onnxruntime 1.20.1; runtime 220,812 giây trên máy 12 logical CPU. Runtime gồm đọc/encode ảnh và cảnh, **không phải latency một lượt check-in**.
- Raw per-pair/per-scene (không chứa identity nguồn) ở `%TEMP%/T-022-s8-development-v1/development-raw.json`, SHA-256 `7f912cb9647906314890d4e586b915b1a5b1b55451941e1c0651fdc6c6de0a2f`; summary và toàn bộ grid tại cùng folder, SHA-256 `c279922825717fab6959d5f0ff3437f4087e917e0123ba623251136227b91485`. File nằm ngoài Git; `%TEMP%` có thể bị dọn. Script run SHA-256 `ebf169ede8316c30464e10fa10487ab6da0c9824726144510a9a08881fbe2445`.

Ground truth genuine/ordinary đến từ folder identity + official pair label XQLFW; scene present/absent và panel target được khóa trước score rồi self-confirm bằng ảnh. Hard negative **không** được gán theo score: trong 32 scene absent đã biết A vắng, P2 chọn non-target ở 4 scene; chỉ 4 candidate ấy đi tới S8. Đây là tập âm tính **có điều kiện sau S4**, không đại diện mọi impostor.

## S4/P2 trước S8

| Mẫu số scene | P2 outcome | Số lượng | Ý nghĩa cho S8 |
|---|---|---:|---|
| Present 32 | Chọn đúng target | 29 | 29 genuine candidate tới S8 |
| Present 32 | Unresolved | 3 | Retry/manual review; không ép chạy S8 |
| Present 32 | Chọn sai target | 0 | Không có hard negative từ present trong development này |
| Absent 32 | Không chọn | 28 | Không có candidate tới S8 |
| Absent 32 | Chọn non-target | 4 | 4 S4-derived hard negative tới S8 |

Như vậy phải báo **cả** `4/32` false selection của S4 lẫn tỷ lệ S8 accept/reject **trong 4 ca đã chọn**; chỉ báo hard-negative FMR `n=4` sẽ che mất tầng S4. Mọi tỷ lệ này đều là proxy có mẫu nhỏ.

## Phân bố cosine trên development

| Nhóm | n | Median | p05–p95 | Min–max |
|---|---:|---:|---:|---:|
| Genuine pair nguồn | 1.318 | 0,3574 | 0,1059–0,6007 | −0,0739–0,7983 |
| Ordinary-impostor pair nguồn | 992 | 0,0080 | −0,0986–0,1358 | −0,2201–0,2884 |
| Genuine được S4 chọn | 29 | 0,2887 | 0,1671–0,5565 | 0,1640–0,6464 |
| Hard negative được S4 chọn trên absent | 4 | 0,2210 | 0,1558–0,2478 | 0,1485–0,2483 |

Median hard negative cao hơn median ordinary impostor (`0,2210` so với `0,0080`), đúng với cách chọn có điều kiện bằng cosine của S4. Nhưng `n=4`, không đủ để ước lượng phân bố ổn định hay kết luận nguyên nhân score cao. Khoảng score của 4 hard negative **chồng với** 29 genuine được S4 chọn; vì vậy không có một ngưỡng cosine đơn lẻ nào trên development này vừa giữ cả 29 genuine vừa reject cả 4 hard negative. Đây là tính chất của chính các mẫu quan sát, chưa chứng minh model/kiến trúc khác sẽ tốt hơn.

## Trade-off S8 theo ngưỡng minh họa

Quy tắc minh họa: `ACCEPT` nếu cosine `≥ θ`, còn lại `REJECT`. Grid mô tả đã có trong script trước run: `−1…1`, bước `0,05`, thêm `θ=0,122254` cũ của T-020 và `τ` P2. Không giá trị nào trong bảng là ngưỡng được chọn cho demo/evaluation. FNMR = genuine pair bị reject / 1.318; ordinary FMR = ordinary pair được accept / 992. Hard accept tính trên **4** âm tính mà S4 đã chuyển tiếp; absent pipeline tính trên **32** scene absent ban đầu.

| θ tham khảo | Genuine reject / 1.318 (FNMR) | Ordinary accept / 992 (FMR) | S4-selected genuine reject / 29 | S8 accept / reject trên 4 hard negative | Absent pipeline: no-select / false-select→S8 accept / false-select→S8 reject |
|---:|---:|---:|---:|---:|---:|
| 0,122254 (T-020) | 85 (6,4%) | 67 (6,8%) | 0 | 4 / 0 | 28 / 4 / 0 |
| 0,147897 (τ P2) | 125 (9,5%) | 32 (3,2%) | 0 | 4 / 0 | 28 / 4 / 0 |
| 0,15 | 126 (9,6%) | 31 (3,1%) | 0 | 3 / 1 | 28 / 3 / 1 |
| 0,20 | 213 (16,2%) | 6 (0,6%) | 7 | 2 / 2 | 28 / 2 / 2 |
| 0,25 | 336 (25,5%) | 1 (0,1%) | 9 | 0 / 4 | 28 / 0 / 4 |

Tăng θ có thể chặn các ca âm tính quan sát được, nhưng đồng thời tăng genuine rejection. `0/4` hard accept ở `θ=0,25` **không** là bằng chứng rủi ro thấp cho scene mới; 4 ca quá ít, và genuine pair FNMR đã là `336/1.318`. Score S8 là cùng cosine của reference với box S4 đã chọn; chỉ đổi ngưỡng tạo *quyết định bổ sung*, không tạo nguồn bằng chứng độc lập.

## Ca lỗi cần truy ngược

| Trial development | Nhãn nguồn | P2 outcome | Selected score | Margin | Ở θ T-020 | Diễn giải |
|---|---|---|---:|---:|---|---|
| `013-absent` | Target vắng | False selection | 0,248328 | 0,277332 | S8 accept | Non-target qua cả τ và δ |
| `014-absent` | Target vắng | False selection | 0,244944 | 0,230846 | S8 accept | Non-target qua cả τ và δ |
| `025-absent` | Target vắng | False selection | 0,197019 | 0,215204 | S8 accept | Non-target qua cả τ và δ |
| `090-absent` | Target vắng | False selection | 0,148543 | 0,193459 | S8 accept | Score chỉ nhỉnh hơn τ; vẫn qua δ |
| `012-present` | Target có mặt | Unresolved | Top 0,120945 | 0,218202 | Không chạy S8 | Rớt τ |
| `015-present` | Target có mặt | Unresolved | Top 0,088049 | 0,028651 | Không chạy S8 | Rớt cả τ và δ |
| `084-present` | Target có mặt | Unresolved | Top 0,118158 | 0,019482 | Không chạy S8 | Rớt cả τ và δ |

Trial ID trong raw có tiền tố `development-`; bảng rút ngắn để đọc. Không commit ảnh, identity, embedding hay raw score. Không gán nguyên nhân hình ảnh/identity cụ thể cho bốn score cao nếu chưa có kiểm chứng riêng.

## Quyết định nghiên cứu hiện tại và điều chờ review

**Evidence development:** encoder/cosine tách ordinary impostor khỏi genuine ở nhiều ngưỡng, nhưng các non-target được S4 chọn khó hơn rõ trong tập nhỏ này và chồng score với genuine được chọn. Ngưỡng S8 cũ không chặn ca nào trong 4 hard negative; ngưỡng cao hơn có trade-off genuine rejection đáng kể. Không đủ căn cứ để chốt `P2 + S8` cho auto-accept, chọn model khác, đặt false-accept cap demo, hoặc suy ra rủi ro thực địa.

### Đề xuất **một** rule research/reference để Quốc An review

**Câu hỏi của rule:** S8 có chặn được một phần false selection quan sát được mà không làm rớt thêm genuine candidate đã qua S4 trên development không? Đây là mốc kiểm khả năng phòng thủ trong cùng pipeline, không là mục tiêu rủi ro nghiệp vụ.

1. Chỉ xét ngưỡng `θ ≥ θ_old = 0,122254` trong grid development đã công bố trước run (`−1…1`, bước `0,05`, cộng thêm `θ_old` và `τ` P2). Giữ nguyên quy tắc `score ≥ θ` là accept.
2. Điều kiện bảo toàn utility quan sát được: trên **29 genuine candidate đã được S4 chọn đúng**, S8 không reject ca nào (`0/29`), bằng mức của `θ_old`. Đây là ràng buộc nghiên cứu trên sample hiện có, không là minimum genuine-accept requirement của kỳ thi.
3. Trong các ngưỡng thỏa điều kiện đó, chọn ngưỡng làm **ít S4-derived hard negative được S8 accept nhất** trên 4 ca development. Nếu hòa, chọn ordinary-impostor FMR thấp hơn; nếu vẫn hòa, chọn genuine-pair FNMR thấp hơn rồi θ thấp hơn. Luôn báo cả ordinary FMR, genuine-pair FNMR, hard accept và chuỗi absent 32 scene; không chỉ báo metric dùng để chọn.

Áp dụng rule trên summary development: các điểm hợp lệ là `0,122254` (hard accept `4/4`, ordinary accept `67/992`), `τ=0,1478971711` (`4/4`, `32/992`) và **`θ_research=0,15`** (`3/4`, `31/992`). Ở `0,15`, genuine pair reject `126/1.318` (`9,6%`, so với `85/1.318` hay `6,4%` ở θ cũ), nhưng 29/29 genuine **được S4 chọn** vẫn accept. Pipeline absent là `28/32` P2 no-select, `1/32` P2 false-select→S8 reject, `3/32` P2 false-select→S8 accept. Rule chỉ chặn **1/4** hard negative có điều kiện; không tạo bảo đảm an toàn.

**Vì sao rule phù hợp để kiểm nghiên cứu khi false-accept cap còn TBD:** nó không đặt một tỷ lệ rủi ro giả định, không gán trọng số kinh doanh tùy ý cho FMR/FNMR, và không tối ưu theo evaluation. Nó hỏi câu hẹp có thể kiểm chứng: phần lỗi S4 nào S8 chặn được trước khi làm tăng số ca đúng bị reject sau S4. Số `0/29` và `1/4` quá nhỏ để tổng quát hóa; ordinary pair genuine FNMR vẫn tăng. Vì vậy đây là **reference operating point đề xuất**, không phải threshold mới được duyệt/khóa hoặc threshold triển khai.

`θ_old=0,122254` tiếp tục là **baseline lịch sử T-020**. `θ=0,25` tiếp tục chỉ là **stress point**: reject 4/4 hard negative development nhưng cũng reject 9/29 genuine được S4 chọn và 336/1.318 genuine pair. Nó không được chọn bởi rule research ở trên. Tại `0,20` đã reject 7/29 genuine mà vẫn accept 2/4 hard negative. Trên development này không thấy vùng ngưỡng vừa chặn phần lớn hard negatives vừa giữ nguyên utility quan sát được; điều đó gợi ý threshold tuning một mình có thể không đủ, nhưng **chưa** là bằng chứng để đổi encoder/model khi chưa có evaluation.

**Điều chờ duyệt:** Quốc An review rule và số `0,15` trước khi freeze. Nếu được duyệt, cố định trước evaluation ba mốc báo cáo `θ_old`, `θ_research` và `0,25` stress; chạy **một lần** trên cùng evaluation đã khóa, không chọn lại mốc theo kết quả. Trước run phải ghi hash code, rule, manifest, model và danh sách mốc; nếu không duyệt, tiếp tục thảo luận chỉ trên development. **Evaluation chưa mở.**

## Giới hạn

XQLFW ghép hai ảnh tĩnh, self-confirm một người, identity nguồn công khai và lọc detector; không đại diện camera cửa phòng hay thao tác khai hồ sơ. Các ordinary pair và hard-negative scene có điều kiện lấy mẫu khác nhau, nên không thể so FMR như hai mẫu ngẫu nhiên cùng phân bố. `AMBIGUOUS` không bị ép nhãn và vẫn ngoài metric. Một số identity/ảnh có thể đóng góp nhiều pair, nên phần trăm quan sát không phải khoảng tin cậy độc lập. S8 ở đây reuse cùng MobileFaceNet cosine như S4; chưa thử tín hiệu xác minh độc lập. Evaluation frozen vẫn nguyên trạng.
