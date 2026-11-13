# BUM 07 — P3.1R Facial Structure Repair

**P3.1R chưa đạt tổng thể: còn nếp gấp/faceting mí và tự giao chưa xử lý. P3.1 chưa được nghiệm thu. P3.1R là bản sửa nghiên cứu, chờ chủ dự án duyệt ảnh. Không đạt/không tự chấm 9/10, không chuyển P3.2.** Chỉ sửa mắt–mí/socket, miệng–má và tóc BUM tiền đạo số 07. Không thay game công khai.

## Bàn giao

- [Blender editable](assets/bum07-p31r-workbench.blend), Blender 4.3.2, không cần Auto Run. Collection mới `05_P31R_FACIAL_STRUCTURE`; C/P2/P3.1 giữ trong file ở các collection gốc, ẩn để đối chiếu. Các file nguồn cũ nguyên byte.
- [GLB thử nghiệm](assets/bum07-p31r-experimental.glb): skin Head, action C và morph corrective bank nhúng; chưa tích hợp gameplay/Showcase dùng chung.
- `renders/chromium`, `renders/webkit`: 38 ảnh beauty/engine, 20 ảnh ID diagnostic/engine và browser report. Hai variant P3.1/P3.1R, neutral 0°/45°/90°, Blink 0/25/50/75/100% từ 0° và45°, Smile 0/50/100% từ hai góc.
- `comparison/`: bảng ảnh trước/sau, ảnh PNG thật đặt cạnh nhau, không retouch, không đổi kích thước từng render.
- [Kết quả máy dễ đọc](CHECK-RESULTS.md), [báo cáo kỹ thuật](TECHNICAL-REPORT.md), `issues.csv`, source/GLB/contact/deformation reports, `BUDGET.json`, `GATES.json`, manifest và SHA-256 gói.

## Thay đổi cấu trúc

P3.1 có mesh mí riêng phủ trên mặt. P3.1R cắt vùng orbital trong head, dùng chính boundary indices để nối các vòng mí và lớp lining của socket vào **cùng một mesh đầu**. Không thêm miếng che trang trí. Hai globe có iris/pupil cong theo bề mặt, loại lens phẳng nhô ra. Mỗi trạng thái Blink được giải theo envelope nhãn cầu và lưu corrective shape key; không chỉ kéo vài đỉnh theo đường thẳng.

Môi trên/dưới có volume mới, oral interior đi cùng; một Smile map phối hợp môi, khóe, cheek uplift và bề mặt đầu. Tóc thay nền +8 leaf overlays bằng một volume liên tục có lobe, rãnh, hairline bất đối xứng và silhouette thay đổi. Đây là procedural study, không giả là sculpt/retopology chuyên nghiệp. Tạo hình và self-contact còn cần nghiệm thu/cleanup.

## Cách dùng morph đúng

- `FH_Blink25`, `FH_Blink50`, `FH_Blink75` là pose corrective tại 25/50/75%; `FH_Blink` là 100%.
- Nội suy giữa **hai pose kề nhau**; tổng weight1 (Basis là weight ngầm ở đoạn0→25). Không bật đồng thời tất cả keys hoặc chỉ tăng `FH_Blink` tuyến tính rồi cho rằng đã dùng đúng contact solver.
- Smile dùng `FH_Smile` trên head/lips/oral interior, cùng một giá trị. Mở từng key riêng trong Blender để kiểm tra; browser review có adapter riêng cho mapping này.
- Mapping chưa được đưa vào runtime game công khai. Morph kiểm tra không phải facial animation production hoặc lipsync.

## Kiểm chứng và giới hạn

Xem `GATES.json`: kết quả Blink không dựa vào ảnh nhìn có vẻ kín. Cần đồng thời không có skin triangle trong envelope mắt và render ID trên **GLB xuất thật** không có pixel mắt đỏ ở100% tại0°/45°. P3.1 cũ là negative control: detector phải bắt được mắt lộ.

Mesh manifold/normal/UV và dữ liệu morph được kiểm riêng. Báo cáo vẫn đếm các cặp tự giao/tiếp xúc không kề nhau của head và va chạm head–lip; không coi toàn bộ là contact hợp lệ hoặc tuyên bố collision-free. Cổng Blink đạt không thay thế nghiệm thu mỹ thuật hoặc rig tổng thể.

## Tái lập

Chạy từ repository root; cần Blender4.3.2, Python3, Node và Playwright với Chromium/WebKit dependencies:

```sh
blender -b --disable-autoexec research/bum07-p31/assets/bum07-p31-workbench.blend -P scripts/assets/build-bum07-p31r.py -- /tmp/bum07-p31r
blender -b --factory-startup --disable-autoexec -P tests/p31r-source.py -- research/bum07-p31/assets/bum07-p31-workbench.blend /tmp/bum07-p31r/bum07-p31r-workbench.blend /tmp/bum07-p31r/source-audit.json
python3 tests/p31r-glb.py /tmp/bum07-p31r/bum07-p31r-experimental.glb
python3 tests/stage-p31r-review.py /tmp/bum07-p31r-review /tmp/bum07-p31r
node tests/p31r-browser.cjs /tmp/bum07-p31r-review /tmp/bum07-p31r-images/chromium chromium
node tests/p31r-browser.cjs /tmp/bum07-p31r-review /tmp/bum07-p31r-images/webkit webkit
```

Nếu dùng browser/runtime đã cài ở đường dẫn riêng, đặt `BROWSER_EXECUTABLE` hoặc `WEBKIT_PATH`. Chỉ chạy localhost review clone; không chỉnh mã Showcase dùng chung. Bộ ảnh/quy trình nằm trên nhánh phát triển PR#2, không phải deployment game.

## Giữ nguyên

C/P2/P3.1, hồ sơ artist, main, GitHub Pages công khai, Supabase/RLS/phòng BA/BUM, body/trang phục/action gốc và ba nhân vật khác. PR#2 Draft, không merge. Không thuê artist hoặc mua asset. Không chuyển P3.2 trước chủ dự án duyệt. Browser Linux không phải Safari iPhone thật, không suy ra FPS từ GPU/user-agent strings.

Baseline P3.1 trong lần xuất cuối có thể tái dùng từ lượt render đã hoàn tất: chỉ khi hash GLB, studio JS và từng PNG khớp. Report ghi `baselineEvidenceReused`; tất cả ảnh/ID của P3.1R được render lại từ GLB cuối. Không tái dùng ảnh R cũ.
