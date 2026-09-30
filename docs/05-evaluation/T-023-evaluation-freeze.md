# T-023 — freeze trước một lượt BFW evaluation

**Thời điểm:** 2026-09-29, sau [development](T-023-development-analysis.md) và trước khi mở bất kỳ MobileFaceNet score nào trên BFW evaluation. Đây là mốc nghiên cứu encoder, không chốt ngưỡng triển khai.

## Đầu vào và quy tắc đã cố định

- Source BFW Release SHA-256 `5053c12a0d65424ae619ba7376746e6977c2fb23b2682741ecdff82ef52a6957`; inner noncrop MD5 `c1c5869f31c6137b40f7755ce8e8f6db`; model `buffalo_sc` SHA-256 `57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72`.
- Candidate manifest SHA-256 `3ac495fefaf440687f379965f44fac772b585dd5e66b09fcde25d0115af1a492`; detector audit `280964a73be58d7995d2fe2c8809ef57463ce6c24336c2d3e86f805a1ae95cb0`; **ground-truth/exclusion lock** `d586d97f1656a7f83b5ae37410b87ff0a0a95997e687d0ed47673205a38aec3b`. Seed `T-023-BFW-scoreblind-v2`; development fold 1–3, evaluation fold 4–5, zero identity overlap nội bộ. Evaluation: 60 present, 238 absent usable, 2 absent `AMBIGUOUS`, 240 genuine + 240 ordinary pair usable. Không đổi nhãn/trial/exclusion sau score.
- P2 giữ `τ=0,14789717107158995`, `δ=0,07647264965285691`; S8 accept nếu cùng cosine của P2-selected box so với reference `≥ θ`. Primary **research** θ=`0,23`, được chọn trên development theo rule [đã ghi](T-023-development-analysis.md); θ=`0,15` historical và `0,25` stress chỉ làm tham chiếu. Business false-accept cap vẫn `TBD`; không gọi θ này là deployment/optimal.
- Development raw SHA-256 `21596e6565fbd6aa3b6d41e7c25b38a49012fba53e3b5c16bd3b7c8b0425c908`, summary `e78f193235a6fd8d91e1cdf2a256afc82104487ec163b241ca234d8a74a2a69b`. Private freeze JSON SHA-256 `ca43678f6fab121129f18698f7a737d8f37f46e099f72d6166ab1985f940ab19` giữ code hashes của script dựng/audit/lock/chấm cùng source/model hash. Script evaluation từ chối code/input khác và từ chối ghi đè output.

## Primary questions/mẫu số sẽ báo sau một run

1. S4 present correct/wrong/unresolved; S4 absent no-select/false-select, tách random/challenge.
2. Hard-negative count và số anchor độc lập; nếu `<20` hard-negative hoặc `<20` anchor, hoặc `<50` selected genuine, kết quả chỉ exploratory.
3. Tại θ=0,23: selected genuine accept/reject, hard-negative accept/reject, genuine FNMR, ordinary FMR; pipeline absent `no-select / false-select→S8 reject / false-select→S8 accept`. Báo thêm phân bố score và overlap, không chỉ accuracy tổng.
4. So chiều trade-off với development, chỉ nhận xét MobileFaceNet có/không có vùng nghiên cứu hữu ích; không đổi model, P2, threshold hoặc nhãn dựa trên holdout. Nếu bằng chứng không đủ, đề xuất task mới với benchmark riêng trước khi thử model khác.

Ảnh BFW, identity, manifest và raw score nằm ngoài Git. Không dùng T-022 evaluation làm train/dev hoặc để chọn θ/model; BFW vẫn là controlled proxy, không phải tỷ lệ lỗi phòng thi.
