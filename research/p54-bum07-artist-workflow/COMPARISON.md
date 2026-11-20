# P5.4 — Hai hướng thực hiện BUM 07

Tên hướng A/B trong báo cáo chỉ cách sản xuất; cả hai giữ concept mỹ thuật B, không mở lại concept A/C.

## Kết luận đề xuất

**Ưu tiên nghiên cứu chuyển sang hướng B — Head – Generic Topology của Paul Kotelevets, CC0 — nếu có người thực hiện sculpt thủ công.** Đây là đề xuất đầu vào, chưa là phê duyệt asset hoặc lệnh sản xuất. Base có cage nhẹ và khả năng thay đổi form; không có ngoại hình BUM hoàn thiện. Không chọn một preset anime, thu nhỏ Snow/Scott hay đổi màu rồi coi là BUM.

**Hướng A — sculpt thủ công từ R** vẫn khả thi về thao tác mesh và giữ được scene/tỷ lệ đối chứng. R có môi đầy hơn B1 và silhouette quen thuộc hơn, nhưng đầu quá dày và nhiều component mặt tách rời; phải sửa mỹ thuật lớn, sau đó retopology. B1 không được khuyến nghị làm nền ngoại hình: có lỗi cằm rõ và tóc dạng mũ, nhiều tam giác trên mặt, không có UV đầu/tóc.

Cả A và B đều cần năng lực thiết kế/sculpt bằng tay. Không có base miễn phí nào trong khảo sát chứng minh có thể đạt B chỉ bằng tự động chỉnh tham số. Nếu chưa có người thao tác Blender thủ công (chủ dự án hoặc artist được duyệt sau), nên dừng ở checkpoint chọn hướng, không lặp cách procedural đã thất bại. P5.4 không thuê ai.

## Kiểm chứng trực tiếp các file sẵn có

Audit ngày20/11/2026 bằng Blender4.3.2, autoexec tắt, không lưu/export. SHA trước/sau giữ nguyên. Số raw và evaluated tách riêng; quad không đồng nghĩa edge flow tốt cho biểu cảm.

| Tiêu chí | P5.3A-R | P5.3B.1 |
|---|---|---|
| Đầu raw | 331,714 đỉnh; 331,710 quad | 24,568 đỉnh; 41,200 tri, 3,840 quad, 2 n-gon |
| Đầu evaluated | 663,420 tam giác | 49,132 tam giác |
| Tóc raw / evaluated | 175,600 đỉnh / 351,192 tam giác | 221,766 đỉnh / 443,524 tam giác |
| UV | Đầu có UVMap; tóc chưa có | Đầu/tóc chưa có |
| Rig/facial keys | 0 armature, 0 shape key | 0 armature, 0 shape key |
| Tỷ lệ | Hồ sơ R đo sọ–đất≈5.000675H; chưa phải duyệt mỹ thuật | Chỉ bust, đầu1H; không có phép đo toàn thân5H mới |
| Giá trị giữ lại | Camera/đèn, bộ răng trên8 chiếc, ngữ cảnh cơ thể, so trước/sau | Kết nối orbital, clearance iris, bài học về cằm/hair cap |
| Việc thủ công chính | Sculpt lại form/lids/canthi; nối môi/má phù hợp; tóc phải thiết kế lại, không chỉ smooth rãnh | Sửa sâu profile/cằm, muzzle/lips và tóc; dựng UV/retopo; lợi ích tái sử dụng mỹ thuật thấp hơn R |

Các native mở được và mesh đầu kín theo audit trước, nhưng **chưa thử brush**, chưa đo độ mượt Sculpt Mode, chưa chứng minh deform. R là quad dày đã bake, không có Multires history để trở lại cage thấp. B1 không có production facial loops; hai n-gon là orbital cup, không phải bằng chứng lỗi lỗ mặt. Nhiều phần tai/mí/môi/neck là component riêng; cần đánh giá lại tiếp giáp khi chuyển sang topology deform.

## So sánh quyết định A / B

| Hạng mục | A — sửa R bằng tay | B — base ngoài, ưu tiên Head – Generic Topology |
|---|---|---|
| Nhận diện B | Có ngữ cảnh/tỷ lệ, nhưng mặt/tóc chưa đạt | Phải dựng lại nhận diện bằng sculpt thủ công; cage không là concept |
| Khởi đầu chỉnh form | Dense sculpt; khó chỉnh lớn có kiểm soát, thiếu cage thấp | 318 đỉnh/316quad ở base; thuận lợi Edit/Sculpt và thêm Multires sau khi được duyệt |
| Retopology | Dự kiến phải làm lại vùng facial/hair; all-quads không cứu edge flow hiện tại | Có loops để khởi đầu; sau thay tỷ lệ vẫn cần kiểm và sửa loop, không mặc định bỏ retopo |
| Rig | Làm mới; không tái sử dụng kết quả Blink cũ | Làm mới; shape keys mẫu thay thiết kế không phải Blink/Smile |
| Tóc | Không nên giữ rãnh chỉ để giữ topology | Base đề xuất không có tóc, phải sculpt riêng đúng B |
| Pháp lý | Geometry dự án sẵn có; giữ provenance/fonts | CC0 đúng asset được đọc trong metadata/README; giữ notice, không nhập cả rig Rain hoặc gán mọi thành phần CC0 |
| WebGL | Không dùng scene1.18Mtri làm game asset | Base632tri không phải budget cuối; sculpt/rig/UV/material rồi mới đo GLB |
| Rủi ro lớn | Neo vào hình thức cũ, sửa kỹ thuật mà không tiến mỹ thuật | Tin rằng asset tự giải quyết mỹ thuật; chọn preset/đặc điểm trưởng thành hoặc anime lệch B |
| Khả năng khôi phục | Save As bản mới, hash R giữ | Lưu donor nguyên byte và bản làm việc riêng, hash nguồn; không thay model game |

## Ước lượng công việc — giờ của người làm 3D có kinh nghiệm

Đây là khoảng lập kế hoạch, **không phải báo giá, lịch hẹn hoặc giờ chạy Codex**. Chưa có artist thử sculpt, độ tin cậy thấp–trung bình. Bảng chưa gồm dựng animation thể thao hoàn chỉnh, tích hợp multiplayer, thời gian chờ nghiệm thu hoặc thêm nhân vật.

| Nhóm việc | A/R | B/Head Generic |
|---|---:|---:|
| Chuẩn bị/provenance/scene/cage | 2–4h | 4–8h |
| Silhouette + sculpt khuôn mặt | 12–24h | 12–24h |
| Sculpt tóc/hairline | 8–16h | 8–16h |
| Retopo + UV + bake/vật liệu đầu/tóc | 12–24h | 8–20h |
| Facial rig/8 biểu cảm và test | 12–24h | 12–24h |
| Cơ thể5H, tay/chân, kit07 và vật liệu | 20–36h | 24–40h |
| Rig thân + skin/deformation test (chưa animation sản xuất) | 8–16h | 8–16h |
| GLB thử nghiệm + kiểm WebGL/thiết bị | 6–12h | 6–12h |
| **Tổng ước lượng** | **80–156h** | **82–160h** |

Cộng dự phòng20–35% nếu cần lập ngân sách: A≈96–211h, B≈98–216h, chưa cam kết. Riêng checkpoint silhouette/khuôn mặt/tóc: A22–44h, B24–48h, trước retopo/rig/body; có thể dừng sớm nếu không đạt. Base mới không chắc rẻ/nhanh hơn; ưu điểm chính là cấu trúc đầu vào và cách kiểm soát chỉnh form.

Sau mỗi checkpoint phải xin nghiệm thu ảnh riêng. Một vòng sửa nhỏ nằm trong khoảng trên; đổi art direction hoặc làm lại nhiều lần cần ước lượng lại, không tự cộng vô hạn. P5.4 chỉ bàn giao kế hoạch; **chưa bắt đầu bất kỳ giờ sản xuất nào trong bảng**.
