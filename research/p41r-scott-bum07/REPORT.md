# BUM07 P4.1R — Scott Final Repair Prototype

**Chờ chủ dự án nghiệm thu hình ảnh. Không tự chấm9/10. Không phải asset đã được duyệt để thay vào game.**

Bắt đầu từ `ea273ab94459525c34af07f4022d6ef52ff2e904`, nhánh `research/p41r-scott-bum07`. Nguồn Scott của **Mish7913 /3DMish**, CC BY4.0: [nguồn, giấy phép và toàn bộ thay đổi](ATTRIBUTION.md). Scott gốc và P4.1 không bị ghi đè.

## Kết quả đã kiểm chứng

| Hạng mục | Kết quả trong phạm vi kiểm thử |
|---|---|
| Iris sọc/giao nhau | Bỏ hoàn toàn các patch iris/pupil chồng lên globe; iris là UV artwork trên chính bề mặt nhãn cầu. Ảnh cận mặt không còn vòng giao nhau như P4.1 |
| Blink100 | **PASS Chromium và WebKit**,0 pixel nhãn cầu lộ ở0°/45°, cả desktop DPR1 và viewport390×844 DPR2 |
| Không thu nhỏ/ẩn mắt |4.070 đỉnh globe có độ dịch chuyển tối đa **0** giữa Blink0/Blink100; mesh/material vẫn tồn tại và open-control cho hàng nghìn pixel mắt. Sửa tiếp xúc trên mesh mí hiện có |
| Smile | GLB thực tế được render0/50/100% ở0°/45° trong cả hai engine; thay đổi tọa độ/native pose có kiểm chứng. Tính tự nhiên vẫn chờ duyệt ảnh |
| Số07/trang phục | Có ảnh GLB thực tế:07 rõ trên áo vàng; cổ áo mới, không còn dây buộc cũ; cạp quần không xuyên gấu áo ở bản cuối. Quần navy, tất, giày bóng đá được giữ |
| Skin tay | Giữ370 joints, toàn bộ weights và Preserve Volume; giải quyết khác biệt DQS/LBS qua adapter nghiên cứu. CPU/native và GPU/readback đạt ngưỡng1e-4 ở12 tư thế |
| Topology/UV | Không phát hiện cạnh>2mặt, winding không thống nhất, mặt suy biến, normal không hữu hạn hoặc UV có diện tích bằng0. Các đường biên hợp lệ liệt kê riêng |
| Chất lượng mỹ thuật | **CHƯA NGHIỆM THU**. Không có tuyên bố9/10 hoặc xác nhận chất lượng điện ảnh |
| iPhone thật | **CHƯA KIỂM THỬ**, không suy diễn từ WebKit Linux/viewport emulation |

Bằng chứng tổng hợp: [summary.json](evidence/summary.json), [PDF ảnh](BUM07-P41R-Render-Review.pdf), [gallery](gallery.html). Tất cả ảnh rawPNG có SHA256; contact sheet chỉ ghép/thu nhỏ, không sửa đẹp khuôn mặt hoặc xóa pixel lỗi.

## Sửa đúng cấu trúc

**Mắt/mí:** P4.1 ghép các mảng cầu iris có bán kính khác globe nên bị giao nhau. P4.1R dùng UV theo ellipsoid của globe gốc và texture iris nâu tự tạo; không thêm lớp mesh che lỗi. Probe trên native Blink100 tìm thấy6 tia lộ ở mỗi khóe trong. Hai corrective `P41R_CanthusContact_L/R` tác động lên105 đỉnh mí mỗi bên, hỗ trợ bán kính0.055 và tăng tiếp xúc phía trước tối đa0.01 đơn vị nguồn. Driver smoothstep hoạt động cuối nhịp Blink; globe giữ nguyên, không đổi visibility/culling để vượt test.

**Mặt/biểu cảm/tóc:** giữ cấu trúc mặt liên tục và facial rig của Scott, các sửa nose/cheek từ nền P4.1, thay hệ iris và sửa contact mí; Smile lấy từ native facial controls. Tóc được làm kín shell, remesh/smooth/decimate và chuyển toàn bộ weights gần bề mặt gốc, không chỉ nâng polygon hay đổi đèn. Đây vẫn là dựng procedural, không phải sculpt thủ công cao cấp; ngoại hình và chuyển tiếp biểu cảm cần chủ dự án xem ảnh.

**Trang phục:** xóa hẳn bản sao áo Scott có dây buộc khỏi prototype, dựng áo bóng đá từ topology thân donor, tạo cổ liền mạch, chiếu07/BUM trong cùng hệ tọa độ WORLD và giữ chiều dày chữ. Hàn cap của chữ, đóng đầu dây giày, sửa khoảng hở áo–thân và áo–cạp quần. Các bề mặt tóc/giày được làm kín và chuyển weights; không sửa Scott gốc.

## Blink và Smile trên GLB mới

Ảnh: `evidence/{webkit,chromium}/p41-blink-*.png`, `p41-smile-*.png`; bảng ghép [Blink](comparisons/blink-levels.jpg), [Smile](comparisons/smile-levels.jpg).

| Engine / viewport | Blink100,0° | Blink100,45° |
|---|---:|---:|
| WebKit Linux, desktop DPR1 |0|0|
| Chromium Linux, desktop DPR1 |0|0|
| WebKit Linux,390×844 DPR2 |0|0|
| Chromium Linux,390×844 DPR2 |0|0|

Eye-ID pass tô globe thật màu đỏ, skin màu xanh, dùng depth test và **cùng shader skinning** như render đẹp. Open control bắt buộc>100pixel mắt để tránh một phép thử trống. Góc0° WebKit có10.591/8.916/5.090/1.250/0pixel ở Blink0/25/50/75/100; góc45° có7.035/5.997/3.406/818/0. Dữ liệu riêng của Chromium và DPR2 ở JSON, không dùng lại Blink P3.1R hay kết quả P4.1.

[glb-roundtrip.json](evidence/glb-roundtrip.json) giải mã buffer/sparse morph/skin từ **GLB được bàn giao**, đối chiếu source vertex IDs với Blender. Sai lệch lớn nhất khoảng1.575e-6 ở neutral và6 facial snapshots. Kiểm tra tọa độ không thay thế kiểm tra che phủ mắt; hai phép đo được tách riêng. Smile là biến dạng thực tế, nhưng không đồng nghĩa một facial animation system hoàn chỉnh hoặc một nụ cười đã được duyệt mỹ thuật.

## Skin deformation — nguyên nhân và giới hạn tương thích

Scott dùng **Preserve Volume / dual-quaternion skinning** trên body/face và một số trang phục. GLB/Three.js thông thường dùng linear skinning. Vì vậy chỉ giữ nhiều weights hơn vẫn không khắc phục hết sai lệch tay. P4.1R:

- Giữ đủ370 joints; tập tên joints giống P4.1, không xóa hoặc gộp joint.
- Giữ toàn bộ influences, tối đa27 sau subdivision; không âm thầm cắt còn4 hoặc chuẩn hóa riêng WEIGHTS_0.
- Giữ native Preserve Volume trong Blender. GLB chứa mọi JOINTS_n/WEIGHTS_n và cờ `extras.P41R_skinning`.
- Adapter nghiên cứu dùng texture highp để đọc toàn bộ weights, tính DQS trong asset space rồi áp dụng transform của viewer. Beauty, shadow, Eye-ID và GPU probe dùng cùng adapter. Per-mesh LBS được giữ cho mesh vốn dùng LBS.

**Đây là hợp đồng của viewer nghiên cứu, không phải hỗ trợ DQS mặc định của core glTF.** Một viewer chỉ đọc4weights/LBS hoặc bỏ qua extras sẽ không tái tạo chuyển động gốc. Không xác nhận GLB là drop-in cho game hoặc mọi phần mềm khác. Không tắt Preserve Volume để làm bài kiểm tra đạt.

[native-deformation.json](evidence/native-deformation.json):12 tư thế thực sự thay đổi bone matrices (hai tay, gập tay mạnh, chân, đầu và tổ hợp đầu/tay), đối chiếu tất cả vertex của17 primitives với native evaluated mesh. Sai lệch tối đa **2.2641e-5**, dưới ngưỡng **1e-4**. Dịch chuyển native ở ArmL_55 khoảng0.6335 và HeadArm khoảng0.6119, nên đây không phải các test rig bất động. Check tay đại diện trong builder giảm từ0.0096927 ở P4.1 xuống cỡ2e-6.

GPU probe dùng float render target đọc vị trí vertex từ **shader đang chạy**, không dùng phép tính CPU thay cho GPU. Mỗi engine có36 lượt readback (body/globe/shirt ở12 tư thế), lấy mẫu theo source vertex IDs và so với fixture Blender. Max error:

- WebKit: **2.26594e-5**.
- Chromium: **2.26441e-5**.

Không dùng corrective của tư thế tay để ép kết quả; chỉ có facial snapshots/corrective mí đã mô tả. [Ảnh tư thế](comparisons/skin-poses.jpg) và rawPNG đi kèm.

**Chưa chứng minh mọi motion của rig:** constraints/drivers của Blender không phải chức năng native glTF. `Bone.Hair.008/009` và `Bone.Tongue.002` có Bendy-Bone segments ở donor; hành vi uốn segment tùy ý chưa được tái tạo/kiểm chứng trong adapter. Rig gốc trong Blender vẫn giữ nguyên.12 pose kiểm thử không phải toàn bộ animation thể thao, cũng không phải chứng nhận mọi tổ hợp facial/IK. Chưa xuất run/kick/celebration clips trong vòng sửa này.

## Topology, UV, normals

[geometry-audit.json](evidence/geometry-audit.json) kiểm tra editable runtime meshes sau sửa:

| Phép kiểm | P4.1 | P4.1R |
|---|---:|---:|
| Cạnh non-manifold không tính boundary |18|0|
| Mặt có diện tích bằng0 |301|0|
| UV face có diện tích bằng0 |1.094|0|
| Normal không hữu hạn |0|0|
| Cạnh có winding không thống nhất |Chưa đo riêng|0|

P4.1R còn **400 boundary edges được phân loại**, không gọi đó là một mesh watertight:

- Body:104 cạnh ở hai vòng mắt và seam cổ/oral kế thừa donor.
- Quần:108 cạnh ở eo và hai gấu quần.
- Áo:188 cạnh thuộc4 vòng cắt có chủ đích — cổ, gấu, hai tay áo.
- Tóc, giày, cổ áo, chữ07/BUM, tất và dây giày mới: không còn boundary hở.

UV mới cho bề mặt procedural dùng mapping theo mặt để lặp vật liệu; hợp lệ cho texture hiện tại, **chưa phải atlas không chồng lấn để bake production**. Normals/winding hữu hạn và nhất quán không đồng nghĩa đã retopology quad đẹp hoặc chứng minh không self-intersect ở mọi animation. Không có tuyên bố kiểm định toàn bộ va chạm triangle–triangle trên mọi pose.

## Ngân sách và tính khả thi iPhone

| Chỉ số | P4.1 | P4.1R |
|---|---:|---:|
| Asset triangles |103.798|104.791|
| Material primitives |21|17|
| Joints |370|370|
| GLB bytes |7.167.624|11.857.720|
| Full-body draw calls, gồm studio |24|20|
| Full-body triangles, gồm studio |105.336|106.329|

Tăng tam giác khoảng0.96%; sửa lỗi không dựa vào tăng độ phân giải đơn thuần. GLB lớn hơn khoảng65% do full weights và dữ liệu mesh/texture mới. Texture tra cứu weights khoảng7.66MiB, **chưa phải tổng VRAM**, chưa tính geometry, morphs, texture thường, shadow map hoặc các framebuffer.

Bench idle3giây,1180×857,DPR1,shadow2048, trong **Linux render phần mềm và tải kiểm thử đồng thời**:

- WebKit: **1.08FPS**.
- Chromium/SwiftShader: **0.51FPS**.

Đây là số đo thấp thật của môi trường test; không giấu hoặc biến thành cam kết iPhone. WebKit launcher đặt `LIBGL_ALWAYS_SOFTWARE=1`; Chromium chạy SwiftShader. Chuỗi GPU “Apple GPU” của WebKit không phải bằng chứng có iPhone/Apple GPU thật. Cấu hình và kết quả thô nằm trong báo cáo browser/runtime.

**Chưa kết luận chạy mượt trên iPhone.** Chưa đo Safari thiết bị thật, RAM/thermal/context loss, chưa có LOD hoặc KTX2 production. Full-weight DQS có chi phí cao hơn stock four-weight LBS; giảm draw calls không chứng minh FPS cao hơn. Cần nghiệm thu ảnh trước, sau đó mới quyết định có tiếp tục nền Scott và đo thiết bị thật hay không. Vòng này không tự chuyển sang tối ưu/animation/nhân rộng tiếp theo.

## Bàn giao và bảo vệ dự án

[Blender](assets/scott-bum07-p41r-editable.blend), [GLB](assets/scott-bum07-p41r-prototype.glb), [hướng dẫn rebuild/chỉnh sửa](README.md), [PDF](BUM07-P41R-Render-Review.pdf),5 ảnh so sánh cùng camera/ánh sáng, đủ Blink/Smile và ảnh5tư thế đại diện từ bộ12pose kiểm thử. Bộ ZIP còn có original Scott, P4.1 tham chiếu và viewer nghiên cứu độc lập; không triển khai viewer này lên Pages production.

Main `c3567aff87ce54adfa251895cecc2247c4d4b705`, PR2 Draft/head `7ef321881935874e4349b486f8f2a7f4836920cd`, public HTML SHA256 `6477b3465f5ef71ea7ca2632da3856ff3bf282918e69069b775dc57100acf587` được kiểm tra chỉ đọc. Không có request Supabase trong browser tests; không thay RLS/dữ liệu phòng. Không chỉnh ba nhân vật khác, không thay model game thật, không mua asset/subscription hoặc thuê artist.

**Kết luận để chủ dự án đánh giá:** các lỗi kỹ thuật được đo đã sửa trong pipeline nghiên cứu, nhưng mỹ thuật9/10, tính tương thích rig tổng quát và hiệu năng iPhone vẫn chưa được nghiệm thu. Dừng tại P4.1R; chờ quyết định bằng hình ảnh.
