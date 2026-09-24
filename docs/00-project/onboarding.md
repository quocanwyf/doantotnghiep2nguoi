# Minh Hy bắt đầu làm việc với Codex

Repo chung: https://github.com/quocanwyf/doantotnghiep2nguoi
Bảng task chung: https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0

## 1. Nhận quyền truy cập

Repo hiện công khai nên Minh Hy có thể clone để đọc. Để push nhánh trực tiếp và gửi pull request trong repo chung, Quốc An mời tài khoản GitHub của Minh Hy làm collaborator có quyền ghi. Quốc An cũng chia sẻ quyền xem/sửa Google Sheet cho tài khoản Google của Minh Hy. Tên người không đủ để cấp quyền; cần username GitHub và địa chỉ Google chính xác.

## 2. Clone repo một lần trên máy Minh Hy

Cài Git nếu máy chưa có. Mở PowerShell ở thư mục muốn chứa dự án:

```powershell
git clone https://github.com/quocanwyf/doantotnghiep2nguoi.git
cd doantotnghiep2nguoi
git status
```

Có thể dùng URL SSH `git@github.com:quocanwyf/doantotnghiep2nguoi.git` nếu Minh Hy đã cấu hình SSH key với GitHub. Không chạy `git init` hoặc `git remote add` trên bản clone. Đăng nhập GitHub trên máy Minh Hy để push; GitHub CLI `gh auth login` là một cách để bật các tính năng GitHub trong Codex trên Windows.

## 3. Mở trong Codex

Trong ChatGPT desktop/Codex, thêm **local project** và chọn thư mục `doantotnghiep2nguoi` vừa clone làm thư mục chính. Tạo chat mới từ project này. Codex sẽ đọc `AGENTS.md` ở gốc repo; yêu cầu AI đọc thêm `README.md`, `docs/00-project/status.md`, tài liệu giai đoạn và note bàn giao liên quan trước khi làm task.

## 4. Kết nối plugin theo từng tài khoản

Trên tài khoản Codex của Minh Hy, mở Plugins và xác nhận Google Drive đã **kết nối** với tài khoản Google có quyền vào Sheet. Nếu có plugin GitHub, kết nối nó với tài khoản GitHub đã được mời vào repo. Cài plugin trên máy Quốc An không tự cấp quyền cho tài khoản Minh Hy. Plugin GitHub hỗ trợ dữ liệu/tác vụ trên GitHub; bản mã cục bộ vẫn cần clone và đồng bộ bằng Git.

Thử yêu cầu AI: “Đọc `AGENTS.md` và `docs/00-project/status.md`; mở Sheet chung và cho biết task nào được giao cho Minh Hy. Chưa sửa gì.” Nếu AI không mở được Sheet, kiểm tra quyền chia sẻ và trạng thái kết nối Google Drive.

## 5. Mỗi khi bắt đầu và kết thúc task

```powershell
git switch main
git pull --ff-only origin main
git switch -c task/T-003-use-case-minh-hy
```

Đọc task trên Sheet, làm việc trên nhánh, cập nhật tài liệu và note bàn giao theo `workflow.md`. Sau khi kiểm tra:

Ví dụ với task T-003, sau khi tạo các file tương ứng:

```powershell
git status --short
git add -- docs/01-problem/minh-hy-proposal.md docs/handoffs/T-003-use-case-minh-hy.md
git commit -m "T-003: đề xuất use case của Minh Hy"
git push -u origin task/T-003-use-case-minh-hy
```

Với task khác, đổi mã task, tên nhánh và danh sách file. Kiểm tra `git status` trước khi stage.

Tạo pull request để Quốc An review. Sau khi gộp, cả hai `git switch main` rồi `git pull --ff-only origin main`; cập nhật link kết quả và trạng thái task trên Sheet. Đừng dùng `git add .` khi có dữ liệu mặt, checkpoint hoặc file nhạy cảm chưa kiểm tra.

Nguồn tham khảo: [local projects](https://learn.chatgpt.com/docs/projects), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [plugins](https://learn.chatgpt.com/docs/plugins), [Codex trên Windows](https://learn.chatgpt.com/docs/windows/windows-app).