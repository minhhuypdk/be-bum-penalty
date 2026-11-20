# BUM07 P5.3A-R Refinement Handoff

Phương án B — Gió Sân Cỏ. Baseline `5dd8744`, nhánh `research/p53ar-bum07-refinement`. Chủ dự án chấp nhận kỹ thuật P5.3A, chưa duyệt mỹ thuật. **P5.3A-R tiếp tục chờ nghiệm thu ngoại hình; không tự chuyển P5.3B.**

## Xem và tải

- `bum07-p53ar-refinement.blend`: mở bằng Blender4.3.2 hoặc mới hơn. Đây là file riêng được chỉnh từ native P5.3A, không dựng lại nhân vật hoặc dùng Scott.
- `renders/before/`: sáu PNG gốc P5.3A từ5dd8744, giữ nguyên byte.
- `renders/after/`: sáu PNG thật từ Blender P5.3A-R,1200×1600; front/45/profile/back toàn thân và face front/45. Không AI thay render hoặc retouch.
- `BUM07-P53AR-COMPARISON.pdf`: P5.2R/P5.3A/P5.3A-R và phân tích kỹ thuật/mỹ thuật.
- `CHANGE-REPORT.md`, `CURVE-BOUNDS-AUDIT.md`, `PASS-FAIL.md`: thay đổi, chẩn đoán và điểm chưa đạt.
- `evidence/`: số đo native, lineage, camera, glare proxy, hem clearance, checksum. `previews/`, `pre-hem-clearance/`, `pre-hair-area-repair/` và `pre-optical-clearance-repair/` là debug được giữ lại, không phải ảnh cuối.

Trong Blender, Numpad0 vào camera; chọn camera khác trong `CAMERAS` rồi Ctrl+Numpad0. Các camera `Full_*` có ORTHO scale5.8H; `Face_*` scale1.5H. Model giữ A-pose tĩnh; không rig hoặc animation. Chọn head/hair vào Edit/Sculpt Mode để chỉnh tiếp. Không có phụ thuộc texture ảnh ngoài; font DejaVu giữ giấy phép trong `licenses/`.

## Phạm vi chỉnh sửa

Giữ topology head/hair và thân áo; chỉnh vị trí vertex, độ sâu cả nhãn cầu hình cầu, iris, mí/má/mũi/môi/cằm, tai/cổ và tóc có sẵn. Chỉ sửa cục bộ sáu dải trim lỗi và nới hai vòng thấp nhất của áo để quần không xuyên ra trước gấu; không retopology nhân vật để rig. Số07/BUM và cung tám răng giữ nguyên hình học.10màu nền P5.2R và tỷ lệ sọ–đất≈5.0007H được giữ.

Các cụm tóc còn đơn giản, gaze/mí/môi chưa đạt mỹ thuật phim; ảnh đẹp hay không thuộc nghiệm thu chủ dự án. Kiểm tra bounds hoặc export thành công không thay thế mỹ thuật. Chưa rig, animation, DQS, GLB production, tích hợp game hoặc đo iPhone.

## Tái lập

Tái lập script cần checkout đầy đủ repository chứa P5.3A/P5.2R; file .blend mở/chỉnh độc lập. Từ thư mục hồ sơ, với Blender4.3.2, Python/Pillow/NumPy và Chromium/Playwright đã có trong môi trường:

```
blender -b -t 1 --python scripts/diagnose-curves.py
blender -b -t 1 --python scripts/confirm-curve-cause.py
blender -b -t 3 --python scripts/refine-existing.py
blender -b -t 3 --python scripts/render-final.py
blender -b -t 1 --python scripts/audit-lineage.py
blender -b -t 1 --python scripts/diagnose-curves-after.py
blender -b -t 2 --python scripts/audit-refinement.py
blender -b -t 1 --python scripts/audit-optics.py
blender -b -t 1 --python scripts/audit-palette.py
blender -b -t 1 --python scripts/audit-hem-clearance.py -- --before
blender -b -t 1 --python scripts/audit-hem-clearance.py
blender -b -t 1 --python scripts/project-iris-rois.py
python scripts/measure-glare-proxy.py
python scripts/build-review.py
NODE_PATH=/opt/codex/cua_node/lib/node_modules node scripts/export-pdf.cjs
python scripts/optimize-pdf.py
```

`refine-existing.py` luôn nạp baseline5dd8744 và lưu sang file P5.3A-R riêng. Hãy Save As bản chỉnh tay trước khi chạy lại script này. Script không gọi builder P5.3A hay xóa nhân vật. PDF chỉ nén một lần sau export; PNG gốc không đổi. Local HTTP server khi in PDF cần quyền môi trường cho Chromium.

Không sửa main, Pages, Supabase, PR#2, ba nhân vật khác hoặc bất kỳ bản lịch sử nào. Dừng chờ nghiệm thu P5.3A-R.
