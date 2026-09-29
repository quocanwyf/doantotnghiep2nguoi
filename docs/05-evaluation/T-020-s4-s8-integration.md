# T-020 — Kiểm luồng S4 → S8 trên output T-017 đã khóa

**Ngày:** 2026-09-29. **Người phụ trách:** Quốc An (Codex hỗ trợ). **Phạm vi:** phép thử nghiên cứu trên proxy XQLFW; không phải kết quả tại cửa phòng thi. Xem [giao thức khóa trước lượt S8](T-020-s4-s8-protocol.md), [T-017](T-017-clean-confirmation.md) và [logic quyết định](DECISION_LOGIC.md).

## 1. Câu hỏi và thứ tự bằng chứng

T-017 cho thấy P2 chọn sai một mặt ở **2/41** trial target-absent. T-020 kiểm việc nối mặt đã chọn sang S8 1:1 có chặn hai lỗi này không. `S4=unresolved` không gọi S8 và đi nhánh retry/đứng một mình trước camera/nhân sự kiểm thủ công. Kết quả S8 không tự cấp quyền vào phòng hoặc ghi attendance.

| Trước khi xem kết quả S8 trên holdout | Bằng chứng |
|---|---|
| T-017 S4/nhãn/P2 đã khóa | Raw T-017 SHA `dceea1abe0d09e78479473bc28a068f2b32d601c840cff0fceac09e1419811c8`; nhãn SHA `130408bd8f7a02ce502f31cb8f386a01d7adfeab9d5be00bc8fe9a195adc7d11`; P2 `τ=0,14789717107158995`, `δ=0,07647264965285691`, config SHA `a63f64d7fa6cfe4d3d98f2d52c10a30d7bb8445b20de8b0e6b4780ff1ff7980d`. |
| Protocol và cách chọn S8 | Commit `eecee11`: chỉ chọn ngưỡng trên pair XQLFW development identity của T-014; quy tắc cân bằng FMR/FNMR đã có từ T-011. |
| S8 development chạy trước replay holdout | 3.512 pair đủ điều kiện identity: 2.061 genuine, 1.451 impostor. Sau lọc mỗi ảnh đúng một mặt: **1.441 genuine, 1.064 impostor**; loại 620/387 pair. Chọn cosine **`0,1222538902465593`**. Development FMR **71/1.064**, FNMR **96/1.441**; đây là số trên tập chọn ngưỡng, không phải kiểm định độc lập. Raw SHA `613418577a2f5a187dcd6df9478428642a14e8f0bd35c7b1a8d5a9a633c4dd3e`; frozen S8 SHA `edc5e46d8746b82d7011af6eea634bb3d35768390139cd2273dad4f950da538c`. |
| Khóa replay trước một lượt S8 | Commit `d06d7b4` ghi ngưỡng, hash và mã replay trước khi chạy holdout. Raw replay SHA `f96a10ba2bf4209f70c77835ad5a8606063893a25724e7fd140262a52ff33102`, script SHA khi chạy `092122f78afde689369234bcdd0696b84952a24cf9e6d9c61c42d46cf2ec516e`. |

S8 trong phép thử này so **chính cosine MobileFaceNet mà S4 đã tính cho box được chọn** với ngưỡng development. Không dùng một encoder hoặc bằng chứng nhận dạng độc lập. Không chạy lại T-017, không tune theo holdout, không sửa nhãn hoặc loại trial vì P1/P2 sai. Có 64 scene nguồn; sau audit T-017, **49 present và 41 absent trial dùng được**. Một scene có thể tạo cả present và absent trial, nên 90 trial không độc lập hoàn toàn. Các trial `AMBIGUOUS`/loại theo T-017 không đi vào mẫu số; không thay đổi quyết định loại đó ở T-020.

## 2. Kết quả thành phần và đầu-cuối

| Phương pháp | Present, N=49: chọn đúng + S8 accept | Chọn đúng + S8 reject | Chọn sai + S8 reject/accept | S4 unresolved | Absent, N=41: không chọn | Chọn + S8 reject | Chọn + S8 accept |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0 | 0 | 0 | 0/0 | 49 | 41 | 0 | 0 |
| P1 | **47** | **2** | 0/0 | 0 | 0 | **37** | **4** |
| P2 | **46** | **0** | 0/0 | **3** | **39** | **0** | **2** |

**Tách component:** S4 P2 vẫn đúng 46/49 present, unresolved 3/49, false-select absent 2/41. S8 chỉ được gọi ở **48 trial P2 đã chọn**: 46 genuine theo nhãn proxy đều accept; **2 impostor được chọn ở absent đều accept**. Vì mẫu số impostor có điều kiện chỉ là 2 trial đã lọt qua P2, `2/2` không phải ước lượng FMR tổng quát của S8. B0 không có trial qua S8, nên không có FMR/FNMR S8 cho B0. P1 gọi S8 ở 90 trial: genuine accept/reject 47/2, impostor accept/reject 4/37. Không gộp `unresolved` vào mẫu số FNMR S8.

**Đầu-cuối proxy:** P2 cho `đúng mặt + S8 accept` ở **46/49 present**; 3/49 không kết luận và cần fallback. Ở absent, **39/41 không có AI accept**, còn **2/41 được chọn sai rồi S8 accept** theo nhãn proxy. P1 tương ứng 47/49 present thành công và 37/41 absent không accept. B0 giữ toàn bộ present unresolved và toàn bộ absent không chọn. Các tỷ lệ không được gọi là xác suất thành công tại cửa phòng.

**Theo số detection:** present có 40 trial hai detection, 9 trial từ ba detection; absent có 35/6. Holdout này không có single-face. T-020 vì vậy không so được luồng một mặt với nhiều mặt; T-011 E2 là phép đo pair 1:1 khác protocol.

## 3. Hai lỗi absent và cơ chế

| Trial | Detection | S4 P2 | Cosine box chọn | S8 ngưỡng | S8 | Kết quả proxy |
|---|---:|---|---:|---:|---|---|
| `holdout-010` absent | 4 | chọn box 3 | 0,238723 | 0,122254 | accept | false selection đi qua xác minh |
| `holdout-018` absent | 2 | chọn box 0 | 0,156472 | 0,122254 | accept | false selection đi qua xác minh |

Hai trial này là **lỗi chọn mặt của S4 và lỗi chấp nhận của pipeline S4→S8 theo nhãn absent proxy**. Nếu chỉ nhìn S4 thì chưa được gọi là S8 false accept; sau khi thực sự áp ngưỡng S8 mới có thể ghi S8 accept đối với trial được gán impostor. Tuy nhiên người nền trong XQLFW không có identity đầy đủ và nhãn chỉ self-confirm; không thể kết luận chắc họ khác người tham chiếu trong mọi ảnh. Không sửa ground truth sau khi thấy cosine.

Quan hệ ngưỡng giải thích toàn bộ kết quả P2: để P2 chọn, cosine đã phải `≥ τ=0,147897`; S8 accept khi cùng cosine `≥ 0,122254`. Vì `τ` cao hơn ngưỡng S8, **mọi box P2 chọn trong cấu hình này đều tự động qua S8**. Nhánh S8 đang có không cung cấp lớp chặn nhận dạng độc lập cho P2. Đây là đặc tính logic của hai điều kiện trên cùng score, không chỉ là ngẫu nhiên của hai ca lỗi. P1 không có `τ`, nên S8 còn từ chối 37/41 absent và 2/49 present.

Các ca chính khác: P1 false accept proxy ở `holdout-005`, `010`, `018`, `037`; P2 chỉ giữ `010`, `018`, không chọn `005`, `037`. P1 reject đúng target present ở `holdout-030`, `038`; P2 giữ cả hai unresolved và thêm `holdout-034` do ngưỡng/gap S4. Trên holdout này không có `S4 chọn sai present`, vì vậy chưa đo được khả năng S8 chặn kiểu lỗi đó.

## 4. Runtime và giới hạn

Development extraction 4.678 ảnh trên CPU warm mất khoảng **113,44 giây**; đó là chi phí tạo ngưỡng offline. Replay 90 trial chỉ so score có sẵn, mất khoảng **0,238 ms toàn bộ vòng Python** và **không phải latency camera/app**. T-017 đã đo decode/detect và embedding thành phần trên runner CPU; T-020 không chạy lại chúng và không cộng median thành thời gian đầu-cuối. Dùng lại cosine S4 khiến S8 không cần encode thêm trong phép thử, nhưng app thật còn capture, lookup, UI, lưu sự kiện và fallback.

Nguồn XQLFW là ảnh web, không là lượt check-in hoặc camera cửa phòng. Label `absent` dựa trên danh tính nguồn và self-confirm, không có danh tính mọi người nền; R50 chỉ là tín hiệu audit nhãn trước score. Mẫu số usable chịu lọc detector/reference, nên kết quả có thiên lệch chọn mẫu. Không có reviewer độc lập, thiết bị đích, policy kỳ thi hay target acceptance risk. Quy tắc ngưỡng cân bằng lỗi trên development không thể tự trở thành ngưỡng deployment.

Runner đã ghi xong raw/hash, sau đó lệnh in console gặp lỗi mã hóa Windows `cp1258` với ký tự mũi tên trong mô tả. **Không chạy lại holdout**; đã đọc và kiểm JSON/hashes đã ghi. Lỗi in console không thay đổi 90 trial hay kết quả. Mã đã chạy giữ ở commit `d06d7b4` và SHA ở trên; bản script sau run chỉ đổi cách escape ký tự khi in JSON, không đổi phép tính.

## 5. Quyết định nghiên cứu và bước kế tiếp

**Kết luận:** selective S4 P2 vẫn là ứng viên có ích để tăng coverage nhiều mặt so với B0, nhưng **cấu hình S4→S8 dùng cùng MobileFaceNet cosine và ngưỡng S8 hiện tại chưa đủ căn cứ cho chấp nhận tự động**. Hai false-selection absent của P2 không được S8 chặn. Không chốt P2, `τ`, `δ` hay ngưỡng S8 cho triển khai từ phép thử này; không retune chúng trên holdout đã xem.

Nếu trình diễn trong app T-018/T-019, `unresolved` phải đi nhánh retry/đứng một mình/manual review; một `ACCEPT` của S8 vẫn là tín hiệu kỹ thuật, không phải quyền vào phòng. Bước nghiên cứu sau phải đặt **yêu cầu rủi ro chấp nhận** và phép đo development/holdout mới cho verification độc lập hoặc ngưỡng có mục tiêu nghiệp vụ phù hợp; nếu không có dữ liệu/tiêu chí đó thì giữ kết quả ở mức demo nghiên cứu. Không tự chọn model/ngưỡng mới để làm đẹp hai ca này.
