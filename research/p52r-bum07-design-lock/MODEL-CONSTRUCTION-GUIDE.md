# P5.2 — BUM07 Field Breeze: Model Construction Guide

**Thiết kế B đã được chủ dự án chọn. P5.2 chưa được nghiệm thu và chưa được phép triển khai Blender.** Đây là tài liệu để người dựng dùng sau khi có phê duyệt rõ ràng, không phải báo cáo đã dựng model.

Nguồn: commit `35997cc84fdba629b347fac4725ddc39bf14a7b0`, concept `research/p51-bum07-art-direction/concepts/B-gio-san-co.png`. Nhánh riêng P5.2 bắt đầu đúng commit này. Không dùng Scott làm ảnh tham chiếu/khuôn mặt; không trộn tóc xoăn, khe răng chủ ý của C hoặc mặt tròn/chỏm cong của A.

## 1. Thứ tự ưu tiên tài liệu

1. Nhận diện đã chốt của B: oval mềm, mắt hạnh nhân, tóc ngắn rẽ lệch thấp, cầu thủ nhí, vàng07/navy.
2. Bảng số đo **đề xuất** trong `specification/design-spec.json` và CSV. Đây là hợp đồng thiết kế dự kiến, cần chủ dự án duyệt; không phải số đo từ mesh.
3. Bản chính diện `turnaround/01-front-000.png` làm mốc nhận diện P5.2; A-pose dùng cùng mốc. Các ảnh45/90/180 diễn giải khối và chất liệu.
4. Nếu ảnh mâu thuẫn số đo hoặc khác nhau về hairline/răng, ghi vấn đề để duyệt; không tự kéo giãn ảnh, lấy trung bình vô điều kiện hay ép mesh theo cả hai ảnh mâu thuẫn.

Tất cả PNG là **ảnh AI concept**, không phải render Blender. Hiện không có mesh, rig, UV, topology hay camera thật cho nhân vật P5.2. Không đưa chỉ số từ P4.1R vào để chứng nhận thiết kế mới.

## 2. Đơn vị và hướng nhìn

- **1H = đỉnh sọ đến cằm ở neutral, không tính tóc.** Chiều cao từ đỉnh sọ đến đất đề xuất5 H; tóc cho phép nhô thêm tối đa0,20H. Không suy ra kích thước thật bằng mét từ ảnh.
- Tọa độ tài liệu đề xuất: +Z lên, −Y hướng mặt, +X là bên trái giải phẫu của nhân vật. Camera0° ở trước; đi về bên phải giải phẫu để đến45° và90°. Mũi hướng sang phải trang ở45/90. Camera180° nhìn sau lưng.
- Công thức camera tương lai: `x=-R*sin(theta), y=-R*cos(theta)`, cùng target và orthographic scale cho cả0/45/90/180; đây là **đề xuất**, chưa có camera được thiết lập hoặc đo.
- Dáng đứng: tay cách thân12°, bàn chân cách tâm nhau0,80H; A-pose: tay35° so với phương dọc, khuỷu mềm khoảng5°, cổ tay thẳng, ngón thả nhẹ.
- Ảnh turnaround dùng cùng canvas1024×1536 và không bị kéo giãn riêng. `turnaround-measurement-layout.svg` đặt chúng1:1 trên thước H đề xuất: đất tại y1408, đỉnh sọ đề xuất y96,1 H = 262,4pixel của **bố cục tài liệu**. Các mốc này không phải kết quả tìm đỉnh sọ bị tóc che trong ảnh AI.

## 3. Tỷ lệ thân và chi

| Bộ phận / mốc | Đề xuất | Ghi chú |
|---|---:|---|
| Sọ–cằm |1,00H|Neutral; khi mở hàm cằm có thể hạ, không kéo dài sọ |
| Rộng sọ / sâu sọ |0,74 /0,78H|Không tính tai và phần nhô mũi |
| Rộng cả tai |0,92H|Tai nhỏ vừa, không phóng thành mascot A |
| Khoảng hai tâm vai |1,05 H|Vai trẻ em, không vai/cơ hàm người lớn |
| Rộng ngực / hông giải phẫu |1,00 /0,95 H|Bề mặt vải còn khoảng hở riêng |
| Tâm vai / hông / gối / cổ chân, từ đất |3,85 /2,55 /1,50 /0,28H|Không dùng gấu quần thay mốc khớp hông |
| Đáy chậu |2,15 H|Khác tâm hông; kiểm tra khoảng động chân sau này |
| Tay trên / cẳng tay / bàn tay |0,82 /0,65 /0,44H|Dài theo chi, không phải chỉ khoảng chênhZ |
| Đùi / cẳng chân |1,05 /1,22H|Từ tâm khớp đến tâm khớp; chưa kiểm chứng chuyển động |
| Rộng bàn tay |0,24H|Năm ngón, ngón cái có khối gốc tự nhiên |
| Dài / rộng giày |0,82 /0,34H|Không đo chiều dài giày từ góc chính diện |

Mốc đầu/eo/cổ áo, khoảng mắt, số07 và các kích thước khác có trongCSV. Đây là điểm khởi đầu để dựng sau duyệt; không khẳng định ảnh AI đã tuân thủ tuyệt đối mọi giá trị.

## 4. Đầu, tóc và hairline

- Giữ oval mềm; trán đầy vừa, gò má nhẹ, hàm dưới thu gọn nhưng cằm bo, không vuông trưởng thành hoặc tròn bé sơ sinh. Mũi có sống nhỏ và đầu mũi mềm; nếp má lúm tiết chế.
- Khối tóc chính ngắn, thấp, ôm hộp sọ nhưng có chiều sâu giữa các lớp. Ngôi ở **bên trái nhân vật**, tức bên phải trên ảnh0° và bên trái trên ảnh180°. Mái quét sang phải nhân vật; không mirror bản45/90 để tiết kiệm dựng.
- Đề xuất5–7 cụm lớn: phần đỉnh, mái quét chính, mái phụ, hai thái dương và gáy; vài cụm phụ có kiểm soát. Đây là cách phân khối, không yêu cầu5–7object hoặc số lượngpolygon cụ thể.
- Hairline đi liên tục từ trán qua thái dương tới gáy; gáy ngắn phía trên cổ áo. Xoáy đỉnh nhỏ tự nhiên, không biến thành các vòng xoăn của C. Không có chỏm dựng của A.
- Không dựng tóc như vỏ mũ trơn, hàng ống nhựa, hàng trăm sợi/cylinder rời hoặc tràn xuống che toàn bộ chân mày. Chốt đường rãnh và silhouette trước sợi nhỏ; từng sợi thấy trong AI không phải yêu cầu geometry.

## 5. Hốc mắt — nhãn cầu — mí

Tham khảo sơ đồvector `face-construction-guide.svg`; đây là sơ đồ đề xuất, không phải wireframe thật.

- Hai tâm mắt cách0,32H; khe mắt neutral rộng0,19H, nhãn cầu đường kính0,22H, iris0,10H. Không tăng kích thước iris/globe để tạo Surprised.
- Globe nằm trong socket; vành mí dày tham chiếu0,008–0,012H ôm mặt cầu, khóe trong/ngoài có mô nối liên tục. Sclera ngà, không trắng phát sáng.
- Mí trên và dưới cùng bám cấu trúc socket; Blink chủ yếu từ mí trên, mí dưới đi ít hơn. Giữ thể tích cầu dưới mí và vị trí khóe mắt. Không đóng mắt bằng hide/globe shrink hoặc lớp phủ trang trí.
- Iris là vật liệu/UV của đúng bề mặt cầu hoặc cấu trúc có tiếp xúc được kiểm tra; tránh patch iris có bán kính khác globe như lỗi lịch sử. P5.2 chưa tạo phương án mesh nào.
- Khi được dựng sau này mới kiểm tra contact ở0/25/50/75/100% từ0°/45° và các góc bổ sung; ảnh Blink AI chỉ mô tả hình dáng đích, không chứng minh hết xuyên mesh.

## 6. Môi — răng — má — hàm

- Miệng neutral rộng0,34H, môi có vành dày và chuyển tiếp mềm vào má; khóe miệng là khối, không phải đầu của một đường vẽ phẳng. Philtrum và cằm vừa đủ đọc, không cường điệu nếp người lớn.
- Tách ý đồ chuyển động: hàm xoay ở vùng khớp hàm, môi/khóe trượt lên khối má; không kéo cả sọ hoặc thay chiều rộng mũi giữa các biểu cảm.
- Chốt **một bộ cung răng** cho toàn nhân vật. Đề xuất8 răng trên phía trước được đơn giản hóa; cung răng dưới tương thích, lộ tùy độ mở miệng. Không tạo khoảng hở chủ ý giữa răng cửa như C. Không biến các đốm răng AI thành8object đặt thẳng hàng không có cung.
- Răng trên gắn với hàm trên; răng dưới và lưỡi đi theo hàm dưới. Miệng cần khoang tối, bề mặt trong môi và lưỡi có thể tích; không dán dải trắng lên miệng.
- Happy nâng khóe nhẹ; Big Smile nâng má/mí dưới và mở hàm vừa; Celebration cười rộng hơn, mày nâng, mắt hẹp do má nâng. Khác biệt phải đến từ cùng khối mặt chứ không đổi người.
- Ảnh hiện còn khác nhỏ về răng/viền mí/nếp mũi; xem báo cáo nhất quán. Bộ cung răng đề xuất và cường độFocused cần chủ dự án duyệt trước khi dùng làm cấu trúc cuối.

## 7. Trang phục và dấu nhận diện

- Áo vàng, cổV nông navy ở trước; sau cổ là đường bo vòng, **không cóV sau gáy**. Tay raglan với piping navy, cổ/tay có dải bo. Không thêm dây buộc, áo giáp hay logo nhà tài trợ.
- Dải cổ rộng0,045 H; đáyV ở3,78H, cổ ngoài gần4H. Nếp vải tập trung hợp lý ở nách, khuỷu vai, eo; không bake bóng đổ hoặc noise to vào màu vải.
- Số **07** navy mặt trước: cao0,38H, bố cục rộng0,50H, tâmZ~3,33H; nằm trên ngực chứ không chuyển ra hông ở góc nghiêng. Tạo template riêng, không lấy hình chữ bị phối cảnh trong ảnh AI làm hình chuẩn.
- ChữBUM nhỏ, thuần chữ, tại ngực trái nhân vật (+X), cao~0,08H; không underline/swoosh. Sau lưng đề xuấtBUM trên vai và07cao0,42H, tâmZ~3,37H. Mặt sau là chi tiết mới phải duyệt, không suy ra đã có trong P5.1.
- Quần navy, cạp~2,48H, gấu~1,82H. Gấu áo~2,43H có phần che cạp; cần khoảng hở giữa cơ thể/áo/quần để không xuyên nhau. Chưa có collision test.
- Tất ngà, **hai dải navy** gần đầu tất dưới gối. Giữ vị trí và độ rộng hai dải đồng nhất; không sinh thêm dải khi đổi góc.
- Giày bóng đá navy, dây vàng, viền/đinh vàng tiết chế; không dùng logo công ty. Mũi/gót/đế là khối thật khi dựng, không chỉ texture. Bảng vật liệu không phải xác nhậnshader đã chạy trên iPhone.

## 8. Màu và vật liệu

[palette.csv](specification/palette.csv) / [material-palette.svg](specification/material-palette.svg) là màu nền sRGB đề xuất, **không lấy mẫu từ vùng đã chiếu sáng trong PNG**.

| Vùng | Màu nền đề xuất | Roughness đề xuất |
|---|---|---|
| Áo vàng |`#F6C744`|0,70–0,85|
| Navy cổ/quần/số |`#182B45`|0,70–0,85|
| Tất |`#F2EBDD`|0,80–0,95|
| Giày |`#1C2D42`|0,45–0,65|
| Da |`#D9A078`|0,45–0,60|
| Môi |`#B97465`|0,45–0,60|
| Tóc |`#241D1A`|0,45–0,65|
| Iris / sclera |`#4E331D` /`#EFE7DA`|0,20–0,35|
| Răng |`#EDE3D2`|0,30–0,45|

Metallic đề xuất0. Da có sắc ấm và blush nhẹ, không lỗ chân lông/noise quá rõ hoặc lớp nhựa bóng. Tóc có highlight theo khối, mắt có catchlight do ánh sáng, không vẽ highlight cố định để che hướng nhìn sai. Chưa khóaSSS, texture resolution, LOD hay ngân sáchGPU ở P5.2.

## 9. Những điểm phải tránh khi dựng/rig ở bước tương lai

Không thay đầu/hàm/tóc sang Scott để tận dụng rig. Không gộp mí thành lớp phủ, rút sphere lúcBlink, cắt skin influences hoặc xóa joint để ép test đạt. Không cố định răng vào môi, smile dạng đường phẳng, jaw mở bằng scale cả mặt, cổ tay bẻ quá mức hoặc ngón cái gắn cùng mặt phẳng với ngón khác. Không kéo texture chữ07 xuyên cổ/sườn hoặc để cạp xuyên áo.

Retopology, UV, rig, blendshapes, collision, weights và GLB export **chưa thực hiện**. Không có polycount/FPS/skin-error của P5.2. Tất cả ví dụ rigging trong tài liệu này là hướng dẫn phòng tránh, không phải tác vụ đã làm.

## 10. Điểm dừng

Chủ dự án cần xem turnaround,8 cặp biểu cảm, bảng số đo và báo cáo khác biệt; ký duyệt P5.2 hoặc yêu cầu chỉnh. **Chỉ khi được phê duyệt rõ ràng mới được triển khai Blender.** Không tự chuyển sang sculpt, mesh, rig, GLB hoặc game.
