# BUM 07 — P5.3B.1 Artistic Head Sculpt

Baseline: `cebfbe1` · Branch: `research/p53b1-bum07-head-sculpt`.

**Kết luận nghiên cứu: FAIL_ARTISTIC_OBJECTIVE.** Đã tạo cấu trúc đầu/tai/hốc mắt và tóc mới bằng Blender Python, nhưng render chưa tạo được bước tiến lớn về mỹ thuật theo B — Gió Sân Cỏ. Đây là file nghiên cứu để xem xét và sculpt tiếp khi được phê duyệt, không phải nhân vật đã nghiệm thu hoặc đạt 9/10. Dừng tại P5.3B.1.

## Xem và tải

- [PDF so sánh / đánh giá](BUM07-P53B1-HEAD-REVIEW.pdf).
- [File Blender nghiên cứu, chỉnh sửa được](bum07-p53b1-head-study.blend).
- [Render chính diện](renders/after/head-front-000.png), [45°](renders/after/head-three-quarter-045.png), [nghiêng 90°](renders/after/head-profile-090.png), [sau 180°](renders/after/head-back-180.png).
- [Báo cáo kỹ thuật và mỹ thuật](ART-TECH-REPORT.md), [checklist](CHECKLIST.md), [quy trình sculpt thủ công đề xuất](MANUAL-SCULPT-WORKFLOW.md).
- [Bản R gốc được sao lưu nguyên byte](reference/bum07-p53ar-preserved.blend). Các file lịch sử tại thư mục gốc không bị sửa.

Ảnh trong `renders/after` là render Blender thật 1200×1600, Cycles CPU 64 samples, không AI/retouch. Ảnh trong `reference` là concept AI định hướng, không phải render hay camera orthographic đã chứng minh. `evidence/previews` là bản thử 12 samples trước sửa đường nối số học, không dùng thay bộ bàn giao cuối.

## Mở trong Blender

Dùng Blender 4.3.2 hoặc tương thích. Mở `bum07-p53b1-head-study.blend`. Các collection `BUM07_B1_HEAD_SCULPT` và `BUM07_B1_HAIR_SCULPT` chứa mesh mới, vẫn chỉnh sửa được; cổ và vai giữ làm ngữ cảnh. Không có thân dưới bị ẩn để che lỗi: hình học thân dưới đã được loại khỏi **file nghiên cứu mới**, bản R toàn thân vẫn được giữ riêng. Tóc đã voxel-union; không có sculpt layer/Multires lịch sử hoặc topology dành cho animation.

Bốn camera `Face_front-000`, `Face_three-quarter-045`, `Face_profile-090`, `B1_back_180` là ORTHO thật, scale 1.5H. File mở ở camera chính diện. Không có rig, animation, GLB hoặc tích hợp game.

## Tái lập

Từ root repository, với Blender 4.3.2 và NumPy đi kèm:

```bash
blender -b -t 3 --python-exit-code 1 --python research/p53b1-bum07-head-sculpt/scripts/build-head-study.py
blender -b -t 3 --python-exit-code 1 --python research/p53b1-bum07-head-sculpt/scripts/audit-head-study.py
blender -b -t 3 --python-exit-code 1 --python research/p53b1-bum07-head-sculpt/scripts/render-final.py
python3 research/p53b1-bum07-head-sculpt/scripts/build-review.py
NODE_PATH=/opt/codex/cua_node/lib/node_modules node research/p53b1-bum07-head-sculpt/scripts/export-pdf.cjs
python3 research/p53b1-bum07-head-sculpt/scripts/optimize-pdf.py
python3 research/p53b1-bum07-head-sculpt/scripts/manifest.py
python3 research/p53b1-bum07-head-sculpt/scripts/verify-handoff.py
```

Build chỉ ghi vào thư mục nghiên cứu này; cần baseline R có sẵn trong repository. Export PDF cần Playwright/Chromium và localhost. Chỉ tối ưu PDF một lần ngay sau export. PNG nguồn không bị nén lại hoặc chỉnh sửa. Sau khi tái lập, checksum có thể khác do lưu native/metadata; không sửa manifest cũ để giả vờ byte giống bản bàn giao.

## Bảo vệ

Không sửa main, Pages, Supabase, PR #2 hoặc ba nhân vật khác. Không tạo PR mới hoặc merge. Workflow mới chỉ kiểm tra checksum và đóng gói hồ sơ trên nhánh này, không triển khai game. Ghi công/font: xem `licenses/DejaVu-font-copyright.txt`; không nhập mesh Scott hay asset 3D bên ngoài trong giai đoạn này.
