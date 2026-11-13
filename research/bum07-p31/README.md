# BUM 07 — Automated Art Pipeline 3.0 / P3.1

**Bản thử nghiệm chưa nghiệm thu. Chưa đạt mục tiêu mỹ thuật; facial rig chưa đạt. Không phải sản phẩm 9/10. Không chuyển sang P3.2 trước khi chủ dự án duyệt.**

Baseline: commit `47cfa8c`, `docs/artist-production/BUM07/BUM07-ARTIST-PRODUCTION-v1.pdf` và workbench P2 nguyên byte, SHA-256 `30338d105c61eb206b688d31d74f9a7ccd947607f7ad67a5aff89833a8cb2f4c`.

## File thực tế

- [Blender editable](assets/bum07-p31-workbench.blend): mở bằng Blender 4.3.2, không cần Auto Run. Collection mới `04_P31_PROCEDURAL_FACE_HAIR`. C/P2, hair guides, sáu ảnh packed và body gốc vẫn trong file; C/P2 ẩn trong file P3.1 để đối chiếu, nguồn C/P2 trên repository không đổi.
- [GLB thử nghiệm](assets/bum07-p31-experimental.glb): texture/buffer nhúng, skin và bốn action C, facial morph nghiên cứu. Không tích hợp runtime game.
- `renders/chromium`, `renders/webkit`: bốn góc C/P2/P3.1, morph 0/50/100%, bốn pose action gốc và layout 390×844.
- `comparison/`: bốn bảng ảnh đặt cạnh C/P2/P3.1, không retouch.
- [Báo cáo kỹ thuật](TECHNICAL-REPORT.md), [lỗi còn lại](issues.csv), `visual-review.json`, `assets/source-audit.json`, `assets/glb-audit.json`, `assets/manifest.json`.

## Phương pháp mới

Không đọc rồi dịch chuyển vài đỉnh của head P2. Script tạo topology đầu mới 192×128 samples với pole duy nhất, mặt analytic có socket concavity, bridge/tip/alar, má và muzzle liên tục. Tạo globe sâu hơn; mí annulus hai lớp có thickness/inner và outer wall, không còn single-sided patch. Môi/brow dạng volume kín, head có Smile study.

Tóc gồm nền kín theo hairline + tám leaf volumes rộng, taper, gờ/lõm và underside riêng. Projection lên scalp ellipsoid làm roots bám nền hơn; không dùng các ống tròn hoặc chỉ tăng subdivision. Nhưng cách này vẫn để lại nền cap và shape leaf khá đều, **chưa tương đương sculpt chuyên nghiệp**.

Mỗi mesh mới được recalc winding, smooth normals, UV tham số, weight Head và modifier rig C. Đây là các component giao nhau có chủ đích, **không phải một retopology đầu–mí–miệng liền mạch đã hoàn thiện**. Không có chứng nhận không tự giao cắt giữa mọi object.

## Kết luận hình ảnh

Có cải thiện cục bộ so với P2: silhouette tóc ít vỡ/răng cưa, roots bớt nổi; mắt giảm nhô. Tuy vậy chưa có bước nhảy mỹ thuật đủ đáng kể theo mục tiêu: mí vẫn dạng vành/mảng dán, eye region thiếu chuyển tiếp, tóc còn cap, môi thiếu biểu cảm. Chớp mắt 100% xuyên/lộ iris và sclera; facial deformation **FAIL** về thị giác dù dữ liệu hữu hạn và không có tam giác diện tích 0 trong bài kiểm tra.

Codex ghi `FAIL_ART_TARGET` và `FAIL_FACIAL_DEFORMATION` ở cổng nội bộ. Đây là đánh giá quan sát ảnh, không thay quyết định nghiệm thu của chủ dự án và không tự chấm điểm số. Không lấy manifold, polygon count, GLB xuất được hoặc browser test PASS để gọi là đạt 9/10.

## Xem và tái lập

Xem PNG trực tiếp trong repository hoặc tải ZIP; mở `index.html` trong gói để đối chiếu ảnh. Khi mở GLB trên Showcase hiện có, dùng import file cục bộ; đừng ghi đè C/P2 hoặc triển khai file này vào game. Bản copy review do test tạo có normalization 2,2 và các hook kiểm thử riêng, khác importer public mặc định 1,9 cho BUM.

Tạo lại vào thư mục mới, không ghi đè nguồn:

```sh
blender -b --disable-autoexec docs/artist-production/BUM07/BASELINE-P2/artist/bum07-facehair-workbench.blend -P scripts/assets/build-bum07-p31.py -- /tmp/bum07-p31-rebuild
python3 tests/p31-glb.py /tmp/bum07-p31-rebuild/bum07-p31-experimental.glb
blender -b --factory-startup --disable-autoexec -P tests/p31-source.py -- docs/artist-production/BUM07/BASELINE-P2/artist/bum07-facehair-workbench.blend /tmp/bum07-p31-rebuild/bum07-p31-workbench.blend /tmp/bum07-p31-rebuild/source-audit.json
python3 tests/stage-p31-review.py /tmp/bum07-p31-review /tmp/bum07-p31-rebuild research/bum07-p31/reference/p2-original.glb
node tests/p31-browser.cjs /tmp/bum07-p31-review /tmp/bum07-p31-images/chromium chromium
node tests/p31-browser.cjs /tmp/bum07-p31-review /tmp/bum07-p31-images/webkit webkit
```

Cần Blender 4.3.2, Python, Node và Playwright Chromium/WebKit cùng dependencies. Có thể chọn Chromium qua `BROWSER_EXECUTABLE`, WebKit qua `WEBKIT_PATH`. Test chỉ serve checkout review trên localhost, không gửi request Supabase. Không sửa mã Showcase dùng chung.

## Bảo vệ dự án

PR #2 giữ Draft; không merge. Main, GitHub Pages, Supabase/RLS/phòng BA/BUM và ba nhân vật khác không đổi. Không thuê/mua asset. Không thực hiện P3.2, body hoặc sports animation mới. A/B/C/P2 không bị xóa hay ghi đè. Chưa đo hiệu năng iPhone thật; WebKit Linux WPE và Chromium software GPU không đại diện Safari iPhone.
