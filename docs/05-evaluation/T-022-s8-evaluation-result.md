# T-022 — Một lượt evaluation S4 → S8 trên controlled XQLFW proxy

**Ngày:** 2026-09-29. **Người phụ trách:** Quốc An, Codex hỗ trợ. **Trạng thái:** evaluation đã chạy **một lần** sau khi [rule và toàn bộ hash/version được freeze](T-022-s8-evaluation-freeze.md). Không thay ground truth, exclusion, P2, MobileFaceNet, threshold hoặc code sau khi xem kết quả. Đây là dữ liệu synthetic/controlled ghép từ XQLFW, **không** là lượt check-in hay FAR tại cửa phòng thi.

## Observation → question → protocol → evidence → decision

**Observation từ development:** S4/P2 false-select 4/32 target-absent scene; các non-target này có cosine chồng với genuine được chọn. Rule research đã được Quốc An duyệt: chọn `θ=0,15` bằng development, giữ `θ_old=0,122254` làm mốc lịch sử và `0,25` chỉ để stress. **Question trên unseen identities:** trade-off genuine/ordinary impostor có lặp lại không, và S8 có chặn được non-target mà S4 chuyển tiếp không?

**Protocol:** evaluation identity-disjoint đã khóa: 30 present + 30 absent scene, 355 genuine + 131 ordinary-impostor pair usable. 14 scene `AMBIGUOUS`, 54 detector-excluded, 113 pair detector-excluded và 14 pair trùng scene pair giữ nguyên ngoài mẫu số. Cùng SCRFD + MobileFaceNet, `τ=0,1478971711`, `δ=0,0764726497`, CPU; S8 `ACCEPT ⇔ cosine ≥ θ`. Ba θ được tính trên **cùng scores từ một run**, primary luôn là `0,15`. Preflight hash/code/label PASS trước inference.

## Primary result tại `θ_research=0,15`

| Tầng / nhóm | Mẫu số | Kết quả |
|---|---:|---|
| S4 target-present | 30 scene | **26 correct**, 0 wrong, **4 unresolved** |
| S4 target-absent | 30 scene | **30 no-select**, 0 false-select |
| S8 trên selected genuine | 26 candidate | **26 accept**, 0 reject |
| S8 trên S4-derived hard negative | **0 candidate** | **N/A**: không có ca nào tới S8 để đo accept/reject có điều kiện |
| Genuine pair 1:1 | 355 pair | 322 accept, **33 reject**; FNMR = **33/355 = 9,30%** |
| Ordinary-impostor pair 1:1 | 131 pair | **2 accept**, 129 reject; FMR = **2/131 = 1,53%** |
| Pipeline target-absent | 30 scene | **30 no-select / 0 false-select→S8 reject / 0 false-select→S8 accept** |

Kết quả pipeline present ở θ primary là 26 correct selection→S8 accept, 0 correct selection→S8 reject và 4 unresolved chuyển retry/manual review; không ép box cho 4 ca này. **Không viết `0/0=0%`** cho hard-negative FMR: mẫu số bằng 0. Con số `0/30` pipeline accept ở absent chủ yếu do **S4 không chọn**, nên không chứng minh S8 đã chặn được S4 false selection.

## Hai mốc đã công bố trước evaluation

| Mốc | Genuine reject / 355 (FNMR) | Ordinary accept / 131 (FMR) | Selected genuine S8 accept / reject | Hard negative S8 accept / reject | Pipeline absent: no-select / false-select→reject / false-select→accept |
|---|---:|---:|---:|---:|---:|
| Historical `θ_old=0,122254` | 20 (5,63%) | 5 (3,82%) | 26 / 0 | N/A (`n=0`) | 30 / 0 / 0 |
| **Research primary `θ=0,15`** | **33 (9,30%)** | **2 (1,53%)** | **26 / 0** | **N/A (`n=0`)** | **30 / 0 / 0** |
| Stress only `θ=0,25` | 76 (21,41%) | 0 (0/131) | 24 / 2 | N/A (`n=0`) | 30 / 0 / 0 |

Trên unseen identities, chiều trade-off ở **genuine pair / ordinary impostor pair** lặp lại development: từ θ cũ lên 0,15, ordinary accept giảm (development `67/992→31/992`; evaluation `5/131→2/131`) và genuine reject tăng (development `85/1.318→126/1.318`; evaluation `20/355→33/355`). Tại θ primary, selected genuine vẫn accept `29/29` development và `26/26` evaluation. Tuy nhiên các pair không độc lập hoàn toàn theo identity, số ordinary evaluation chỉ 131, và đây không phải ngưỡng đạt rủi ro nghiệp vụ.

S4 hiện có `29/32` correct và `3/32` unresolved present trên development, so với `26/30` correct và `4/30` unresolved evaluation. Với absent, development có `28/32` no-select và `4/32` false-select; evaluation `30/30` no-select và **không có false-select**. Sự khác nhau này không được dùng để tuyên bố lỗi đã biến mất: holdout mới không tạo một hard negative đi tới S8.

## Ca unresolved và failure mode

| Trial | Top cosine | Margin | Vì sao P2 chưa chọn |
|---|---:|---:|---|
| `evaluation-021-present` | 0,136328 | 0,171386 | Score dưới `τ` |
| `evaluation-022-present` | 0,084798 | 0,014515 | Score dưới `τ`, margin dưới `δ` |
| `evaluation-027-present` | 0,193196 | 0,054567 | Margin dưới `δ` |
| `evaluation-053-present` | 0,100098 | 0,026872 | Score dưới `τ`, margin dưới `δ` |

Không có `S4 wrong selection` trong present hoặc `S4 false selection` trong absent evaluation. Vì thế cũng không có S8 false accept **sau S4** trên holdout này; đó là **thiếu cơ hội kiểm failure path**, không phải bằng chứng S8 phòng thủ thành công. Hai ordinary-impostor pair accept ở θ primary là lỗi 1:1 trên cặp ảnh nguồn; không gọi chúng là pipeline false accept.

## Bằng chứng run và khả năng truy ngược

- [Freeze trước score](T-022-s8-evaluation-freeze.md): private freeze SHA-256 `37071ad8bd244ddad1cf1d45fc279d642903b18f073553cb04d51eb1e45ad705`; GT/status SHA-256 `1a1adbc67fb327888b5b40f95b31f79c312e7a5730d5e115ecc05ccdbd2f0a19`; code version `T-022-S8-evaluation-v1`, code commit chuẩn bị `120fbff`. Preflight PASS. Evaluation script đối chiếu lại hash trước inference.
- Raw per-pair/per-scene: `%TEMP%/T-022-s8-evaluation-v1/evaluation-raw.json`, SHA-256 **`b284c5d50a76eee0764f92cb15c519b1d395ba15959ab5f0c98f65abf939f575`**. Summary: `evaluation-summary.json`, SHA-256 **`f27f233aefc42f8146874e68bff11fe66875622f6f23f17ab686f39da9009afe`**. Đã kiểm độc lập sau run: raw có 486 pair, 60 scene; summary trỏ đúng raw/freeze hash và các mẫu số cộng khớp. Không chạy lại model để tạo báo cáo.
- Runtime toàn script `20,391` giây trên máy Windows 11, 12 logical CPU, Python 3.12.2, OpenCV 5.0.0, ONNX Runtime 1.20.1, InsightFace 0.7.3, NumPy 2.2.6, CPUExecutionProvider. Runtime gồm tải/encode ảnh và cảnh; **không** phải latency một lượt check-in. 793 ảnh nguồn evaluation được encode.
- Raw, source ZIP, ảnh cảnh, manifest và private freeze giữ ngoài Git; không commit ảnh mặt, identity hoặc per-sample score. `%TEMP%` có thể bị dọn, nên artifact cần được sao lưu riêng trước khi chuyển máy.

## Kết luận và đóng T-022

**Finding:** trên holdout identity-disjoint này, genuine/ordinary pair cho thấy cùng **chiều** trade-off với development ở θ primary: ordinary FMR giảm so θ lịch sử nhưng genuine FNMR tăng; selected genuine vẫn 26/26 accept. **Câu hỏi hard-negative sau S4 chưa được xác nhận trên evaluation** vì 30/30 absent scene đều no-select; không có mẫu số để xem S8 có chặn false selection hay không. `θ=0,25` làm ordinary accept bằng 0/131 nhưng reject 2/26 selected genuine; vẫn chỉ là stress point.

**Decision:** giữ SCRFD + MobileFaceNet + P2 + `θ=0,15` như **mốc nghiên cứu có thể tái lập**, chưa chốt auto-accept hoặc cấu hình triển khai. Evidence hiện tại **chưa đủ để khẳng định encoder phải thay/fine-tune**, và cũng **chưa đủ để xác nhận S8 kiểm soát được hard negative mà S4 chọn**. Không đặt ngưỡng rủi ro demo khi business cap còn `TBD`. T-022 kết thúc với kết luận có giới hạn này; **không tạo T-022B/T-022C hoặc tune tiếp trên cùng evaluation**. Nếu muốn theo đuổi lựa chọn encoder/model, task tiếp theo phải hỏi riêng: *model/encoder hiện tại có cần thay hoặc fine-tune không?* và khóa một phép kiểm hard-negative mới, độc lập với evaluation T-022, trước khi so candidate.
