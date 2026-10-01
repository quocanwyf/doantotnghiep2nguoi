# Quyết định chính thức

Mỗi quyết định quan trọng có một file `T-004-D-001-ten-ngan.md` khi phát sinh từ task T-004; không sửa mất lịch sử. Quyết định mới thay thế mục cũ bằng liên kết hai chiều. Đã ghi [D-001 — chọn bài toán cửa phòng thi](T-004-D-001-chon-bai-toan-cua-phong-thi.md) và [D-002 — dùng T-005 làm hướng khảo sát](T-007-D-002-chon-huong-khao-sat-t005.md) theo xác nhận của Quốc An về lựa chọn nhóm. D-002 là survey decision, chưa phải quyết định kỹ thuật cuối; chưa ghi nhận thầy xác nhận hai quyết định này.

[D-004 — Duyệt default demo T-024](T-024-D-004-duyet-default-demo.md) ghi xác nhận của Quốc An ngày 2026-09-30 cho **Group 1**. Quyền auto-check-in, manual authority và risk chưa được duyệt cùng quyết định này; toàn profile chưa freeze.

[D-005 — Auto-check-in có điều kiện](T-024-D-005-auto-checkin-co-dieu-kien.md) ghi duyệt **Group 2** của Quốc An cùng ngày: quyền trong demo profile qua `auto_checkin_enabled`, hỗ trợ READY_FOR_CONFIRMATION khi tắt.

[D-006 — Manual authority ba tầng](T-024-D-006-manual-authority.md) ghi duyệt **Group 3** của Quốc An cùng ngày: operator chỉ tương tác/route; cán bộ phòng được manual identity/late/re-entry trong quyền được ủy quyền; admin giữ data/policy/correction/lifecycle. Manual identity cần quyền + evidence method đã duyệt + scope; HUMAN không sửa verdict AI.

[D-007 — Workflow acceptance và AI/risk evaluation](T-024-D-007-workflow-va-risk-evaluation.md) ghi duyệt **Group 4** ngày 2026-10-01: mandatory workflow invariants có PASS/FAIL; AI/pipeline errors báo attempt-level, manual riêng. Cap TBD nên test chưa có safety PASS/FAIL hoặc kết luận đạt rủi ro chấp nhận được. Bốn group policy chính đã chốt; test profile cụ thể chưa freeze/test, nguồn existing/replay/fixture không là camera thực địa.

Mẫu:

```md
# D-001 — Tên quyết định

- Trạng thái: Đề xuất | Nhóm đã chốt | Thầy đã xác nhận | Đã thay thế
- Ngày:
- Người chốt/xác nhận:
- Vấn đề và các phương án:
- Lựa chọn và lý do:
- Bằng chứng: biên bản, khảo sát hoặc thí nghiệm
- Tác động/giới hạn:
- Thay thế quyết định nào (nếu có):
```
