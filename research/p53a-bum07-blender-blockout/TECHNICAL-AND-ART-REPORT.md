# BUM07 P5.3A — Báo cáo kỹ thuật và mỹ thuật

Ngày19/11/2026. Baseline4218375. Chỉ BUM07; P5.2R được chấp nhận có điều kiện làm tài liệu định hướng, không phải phê duyệt mỹ thuật P5.3A.

**Kết luận: có blockout Blender chỉnh sửa được và render thật để nghiệm thu. Chưa đạt chất lượng mỹ thuật hoàn thiện của conceptB, không tự đánh giá9/10. Dừng P5.3A.**

## Cấu trúc model

- Tạo hình mới bằng Blender Python; không import Scott hoặc mesh người có sẵn. Đầu xây từ bề mặt oval liên tục với thể tích mũi/má/cằm. Hốc mắt được cắt hình học, vành mí có bề dày rồi nối/remesh vào đầu.
- Nhãn cầu, iris và pupil là cấu trúc3D riêng nằm trong hốc, dùng chung ở mọi góc. Không ẩn đối tượng hay thay mesh/camera để che lỗi. Không có shape key/action/driver điều khiển góc nhìn.
- Tóc có ngôi trái giải phẫu, mái thấp quét sang phía phải nhân vật; các khối thể tích được hợp nhất/remesh. Chưa có tóc sợi, sculpt tinh hoặc hair cards production.
- Thân, cổ, tay năm ngón, chân và kit dùng nhiều bộ phận blockout. Một cấu trúc/model được giữ nguyên giữa các góc **không đồng nghĩa một mesh production liên thông**.
- Cung răng trên: đúng một object, tám thành phần theo UR4/UR3/UR2/UR1/UL1/UL2/UL3/UL4; độ rộng theo cùng một dãy tỷ lệ P5.2R. Không có khe giữa chủ ý. Các răng là các thành phần riêng trong cùng object, chưa kiểm tra khớp cắn hoặc khoảng tiếp xúc phục vụ rig. Miệng neutral đóng; không lấy render miệng đóng để tuyên bố răng/facial animation đạt.
- Vật liệu nền dùng10 mã sRGB và roughness P5.2R, metallic0. Tông phụ cho bóng hốc, mày, tóc phụ chỉ hỗ trợ blockout. PNG không bắt buộc trùng mã sRGB vì được chiếu sáng và qua AgX. Đọc `evidence/palette-readback.json`: kiểm trực tiếp node vật liệu của file .blend với10mã nền P5.2R, roughness trong khoảng và metallic0.

## Lỗi đã xử lý trong P5.3A

| Lỗi | Thay đổi thật | Bằng chứng |
|---|---|---|
| 07 kéo thành vệt dài | Tính chiều cao theo mặt phẳng chữ trước khi xoay, bake transform đúng | Bounds chiều cao chữ trong audit |
| 07/BUM nổi khỏi áo | Mesh chữ được chiếu theo trục lên shirt evaluated, offset0.0015H; bỏ extrude gây mặt trùng | Khoảng cách BVH từng vertex, nhiều góc PNG |
| Sclera lộ ngoài mí / vòng mí rời | Đặt lại độ sâu globe, sửa hướng mặt vành mí, bề dày và overlap; nối mí vào head | Lưới tia0/45/90 và ảnh cận mặt |
| Cổ V bị thân áo che | Tạo vành vai/cổ biến thiên cao độ, ranh V theo đoạn thẳng ở phía trước, chiếu dải cổ lên garment; sau bo | Full/face0/45/90/back |
| Piping bay ngoài áo | Đưa đường viền về bề mặt garment thật | PNG nhiều góc; vẫn chưa phải đường may production |
| Da chân xuyên tất ở preview | Tăng thể tích tất và dải bo để bao calf blockout | Full0/45/90/back; chưa kiểm thử chuyển động |

`evidence/pre-repair/` giữ preview/source debug ban đầu. Những ảnh này có lỗi đã nêu, không phải bản cuối. Không có thêm giai đoạn nghiên cứu mới ngoài P5.3A.

## Đo kiểm và giới hạn bằng chứng

Đọc `evidence/proportion-comparison.csv` để phân biệt số đo đề xuất/thực/không so sánh được, và `evidence/mesh-camera-audit.json` cho toàn bộ số đo, từng object và thông số camera. Mốc5H được đo từ bbox đầu và đáy studs, không chỉ đọc các empty mốc.

- Tỷ lệ sọ–đất: khoảng5.0007H; tính tóc: khoảng5.1622H, dưới mức đề xuất5.2H. Đây là số đo model này, khác số đo đề xuất trong ảnh AI.
- Camera full: ORTHO5.8, cùng target(0,0,2.6); face: ORTHO1.5, cùng target(0,-0.01,4.53). Góc0/45/90/180 có cùng model và tọa độ +X trái giải phẫu, forward−Y, up+Z. Test đoạn1H ở hai độ sâu xác nhận không đổi độ phóng đại.
- Thông số tác giả trước remesh của mắt chưa trùng tuyệt đối đề xuất: khẩu độ ngang0.202H so0.19H (+6.3%), globeD0.212H so0.22H (−3.6%), irisD0.096H so0.10H (−4%). Đây là lựa chọn cấu trúc blockout để sửa hốc/mí, **chưa được chủ dự án duyệt làm thay đổi thiết kế**. Không gọi chúng là số đo hậu remesh của khẩu độ; xem `evidence/face-parameter-deviations.json`.
- Lưới ray mắt90×90/mắt/góc, bước0.003146H; báo cáo cả điểm ngoài khẩu độ danh nghĩa lẫn dung sai0.004H. Đây là kiểm tra hình học tĩnh lấy mẫu, không chứng minh từng pixel, mọi góc liên tục hoặc Blink/Smile. PNG0/45/90 là bằng chứng quan sát bổ sung, không thay thế đo kiểm.
- Chữ áo: bounds07 trước0.38H/sau0.42H; khoảng cách lớn nhất tới áo khoảng0.00152H, trong giới hạn0.003H. Không suy thành số đo mm vì chưa khóa scale mét.
- Số tam giác là evaluated Blender, không phải GLB/draw calls. Model blockout có 1,183,138 tam giác evaluated (khoảng1.18 triệu); đọc JSON cho số chính xác. Chưa retopology/UV/LOD, không tối ưu hoặc đo iPhone. Không có FPS để báo cáo.
- Mesh đầu/tóc/cung răng có0cạnh non-manifold và0mặt zero-area trong audit. Biên cổ/gấu/piping và các bộ phận chồng nhau được liệt kê trong audit; không đánh đồng tất cả boundary với lỗi mesh. Tuy nhiên đây vẫn không phải topology deform-ready, chưa kiểm tra skin/rig hoặc tất cả giao cắt.
- CyclesCPU,64samples,1200×1600, AgX Medium High Contrast. Blender build không có OpenImageDenoise nên denoise tắt; có thể còn noise. PNG lưu trực tiếp, không dùng AI để làm đẹp hoặc che hình học.
- `render-metadata.json` ghi fingerprint mesh/transform/material, ánh sáng cố định và SHA từng PNG. Bảy render độc lập; A-pose alias trùng front0° có công bố rõ, không có rig hoặc thay dáng bí mật.

## Mỹ thuật: đối chiếu conceptB/P5.2R

| Phần | Đã thể hiện | Còn chưa đạt |
|---|---|---|
| Tỷ lệ/nhận diện | BUM trẻ em, oval,5H, vàng07/navy | Cảm giác duyên và cá tính chưa ngang concept; cần chủ dự án xem cả front/profile |
| Mắt/mí | Hốc, globe, iris/pupil và khẩu độ hạnh nhân, mí có thể tích | Khóe và bọng mí còn đơn giản; gaze trung tính còn thiếu sinh động. Ở45°, catchlight còn quá rộng và mắt vẫn có cảm giác lồi: đây là lỗi thị giác/mỹ thuật chưa đạt, dù kiểm tra tia khẩu độ đã qua. Không coi hết lộ sclera lấy mẫu là đạt ngoại hình |
| Tóc | Ngôi trái, mái thấp, thể tích nhất quán360° | Các khối/rãnh còn cứng và đều, hairline/gáy chưa tự nhiên như concept; **FAIL tiêu chuẩn tóc hoàn thiện** |
| Mũi/má/cằm | Thể tích gắn vào mặt, silhouette thật | Tip/alar, má và cằm chưa có sculpt tinh; profile còn cần mềm hơn theo nhận xét chủ dự án |
| Môi/tai/cổ | Môi có thể tích, tai/helix, cổ nối vào đầu | Miệng vẫn hơi đồ họa, tai còn sơ đồ, cổ và đường hàm cần cân chỉnh mỹ thuật; không phải facial sculpt cuối |
| Kit/tay/giày | Đúng nhóm màu,07/cổV/cổ sau/tất/giày, năm ngón | Thiếu nếp vải/chất vải, form tay/ngón và giày còn đơn giản; đường vai chưa tự nhiên như đồ may thật. Cổ/piping, gấu áo và đầu dải navy trên tất còn mép bậc/không đều sau phép chiếu: lỗi finishing cần ghi nhận, không coi là chi tiết may hợp lệ |

Ảnh B/P5.2R là AI concept, camera và dáng đứng không được chứng minh là orthographic chính xác. Không thể đăng ký pixel hoặc dùng chênh lệch ánh sáng để kết luận tỷ lệ3D. PDF đặt cạnh nhau để chủ dự án đánh giá ngoại hình, không xóa các sai khác này.

## Phạm vi bảo vệ và điểm dừng

Chỉ thêm thư mục P5.3A và workflow đóng gói chỉ đọc cho nhánh này. Không sửa main/Pages/Supabase/PR#2, ba nhân vật khác hoặc các bản lịch sử. Không rig hoàn chỉnh, DQS, sports animation, GLB sản xuất hay tích hợp game. Xem `evidence/protection-check.json` và SHA manifest.

**Chủ dự án nghiệm thu trực tiếp ngoại hình. Chưa tự triển khai P5.3B hoặc sửa tiếp ngoài phạm vi đã giao.**
