# BUM07 — P5.3A Blender Character Blockout

B — Gió Sân Cỏ / Field Breeze. Baseline `4218375`; P5.2R được chủ dự án chấp nhận có điều kiện làm định hướng. Nhánh `research/p53a-bum07-blender-blockout`.

**Bàn giao blockout thật, chưa nghiệm thu mỹ thuật. Dừng tại P5.3A; không tự chuyển P5.3B.**

## Mở và xem

1. Tải `bum07-p53a-blockout.blend` bằng nút **Download raw file** trên GitHub, hoặc tải ZIP trong Actions handoff.
2. Mở bằng Blender4.3.2 hoặc mới hơn. Không cần add-on; hình học/vật liệu nằm trong file, không tải mesh Scott.
3. Nhấn Numpad0 để vào camera hiện tại. Các camera trong collection `CAMERAS`: `Full_front-000`, `Full_three-quarter-045`, `Full_profile-090`, `Full_back-180`, `Full_A-pose-000`, và ba camera `Face_*`.
4. Chọn camera rồi Ctrl+Numpad0 để dùng camera đó; Camera Data → Type **Orthographic**. Scale toàn thân5.8H, cận mặt1.5H. F12 render; vật thể không đổi theo camera.
5. Chọn `Head_NEW_oval_integrated_nose_cheeks` hoặc `Hair_unified_low_swept_masses` → Tab để sửa mesh/Sculpt Mode để chỉnh khối. Đây là remesh blockout dày, chưa retopology để rig.
6. Collection `BUM07_DENTITION` có đúng một object `UpperDentalArch_SINGLE_8_teeth`, tám phần răng. Miệng neutral đóng, nên răng không lộ trong render. Không có bản sao răng theo góc nhìn.

## Bộ bàn giao

- `bum07-p53a-blockout.blend`: model chỉnh sửa được, vật liệu và camera thật.
- `renders/`: bảy render độc lập1200×1600 và một alias A-pose, PNG thẳng từ Blender, không AI thay thế/retouch.
- `full-a-pose-000.png` byte-identical với `full-front-000.png`: toàn bộ turnaround đã ở A-pose35°, không có thay dáng hoặc rig. `face-profile-090.png` là góc kiểm tra bổ sung.
- `BUM07-P53A-BLOCKOUT-COMPARISON.pdf`: conceptB/P5.2R/P5.3A, nhiều góc và giới hạn.
- `TECHNICAL-AND-ART-REPORT.md`, `PASS-FAIL.md`: tách kiểm chứng kỹ thuật khỏi mỹ thuật.
- `evidence/mesh-camera-audit.json`, `render-metadata.json`: đo từ file native, camera và fingerprint model/ánh sáng.
- `evidence/pre-repair/`, `evidence/preview-history/` và `evidence/before-collar-repair/`: tiến độ/debug được giữ lại, **không phải bộ nghiệm thu cuối**. Mở PNG trong `renders/` để xem bản bàn giao.

Một scene unit được dùng làm1H (sọ–cằm); chưa khóa tỉ lệ mét thực. Bảng màu nền lấy đúng P5.2R; màu pixel còn chịu AgX/ánh sáng. Nhiều bộ phận blockout chồng nhau; không phải mesh production nối liền, UV hoàn thiện hoặc game asset.

## Tái lập

Trong môi trường có Blender4.3.2 và font DejaVuSans-Bold:

```
blender -b -t 8 --python scripts/build-blockout.py -- --no-render
blender -b -t 8 --python scripts/render-final.py
blender -b -t 4 --python scripts/audit-blockout.py
blender -b -t 2 --python scripts/audit-palette.py
python scripts/build-review.py
NODE_PATH=/opt/codex/cua_node/lib/node_modules node scripts/export-pdf.cjs
python scripts/optimize-pdf.py
```

Đường dẫn script ở trên tính từ thư mục hồ sơ; script tự tìm ROOT. Chạy build sẽ tái tạo file P5.3A từ thông số, do đó hãy lưu bản chỉnh tay sang tên khác trước khi chạy lại. Không ghi đè bất kỳ phiên bản P4/P5 trước đó. PDF compression chỉ chạy một lần sau export; PNG không đổi.

Font chữ số: DejaVuSans-Bold, ghi nhận giấy phép trong `licenses/DejaVu-font-copyright.txt`. Không dùng Scott hoặc asset nhân vật bên thứ ba.

Không có rig hoàn chỉnh, animation, DQS, GLB sản xuất hoặc kiểm thử iPhone/FPS. Không tích hợp game, không thay main/Pages/PR#2 hoặc Supabase. Chờ chủ dự án nghiệm thu ngoại hình.
