# P3.1R — báo cáo cấu trúc, va chạm và giới hạn

## Kết luận quan sát ảnh thật

**P3.1R chưa đạt tổng thể Facial Structure Repair.** Cổng che kín nhãn cầu và kiểm tra envelope có thể PASS riêng, nhưng ảnh beauty còn nếp gấp/faceting rõ quanh orbital transition và mí khi nhắm; self-contact chưa phân loại là lỗi chặn. Smile có đường cong và phối hợp má hơn P3.1 nhưng còn môi/khóe không tự nhiên. Tóc không còn dải overlay và đã sửa các lỗ da xuyên rãnh, song vẫn đọc như cap ở vài góc. Không coi là hoàn tất cả ba mục tiêu hoặc đạt9/10.

Giới hạn nằm ở topology/correspondence của cách stitch cut-boundary và các vòng lining/contact procedural. Manifold và zero eye exposure không bảo đảm smooth anatomical curvature. Không đổi ánh sáng, culling hoặc retouch để che nếp gấp; các ảnh nguyên được giữ để nghiệm thu. Cổng `socketSurfaceForm`/`globalFacialDeformation` đánh FAIL riêng.

## Phạm vi và cổng nghiệm thu

Chỉ BUM07 face/hair, trên nguồn P3.1 commit `def4314`. P3.1 không được nghiệm thu và không ghi đè. P3.1R chờ chủ dự án duyệt ảnh; không tuyên bố 9/10. Cổng kỹ thuật Blink và cổng mỹ thuật tách riêng trong `GATES.json`.

1. `blink100`: phải PASS cả ray/triangle-sphere audit và actual GLB ID render tại0°/45° trên hai engine. Bất kỳ mắt đỏ hoặc tam giác xuyên envelope ở100% sẽ tự thành FAIL.
2. `requestedBlinkCollision`: kiểm0/25/50/75/100%; bổ sung midpoint12.5/37.5/62.5/87.5%, không suy ra bảo đảm cho mọi giá trị liên tục.
3. `globalFacialDeformation`: FAIL, chưa đạt chuẩn production vì còn tự giao/tiếp xúc chưa phân loại và root contact head–lip. Không dùng manifold hoặc zero red pixels để đóng cổng này.
4. `artAcceptance`: PENDING_OWNER; chỉ chủ dự án nghiệm thu tạo hình. Không tự chuyển P3.2.

## Đầu, socket và mí

Outer loop của socket giữ nguyên tọa độ boundary vừa cắt trong head P3.1 để tránh ép vượt hàng vertex lân cận. Các vòng chuyển tiếp, lid margin và lining được nối bằng index vào cùng mesh head; không còn annulus object chồng lên mặt. Rigid Head skin binding gốc giữ nguyên.

Globe radius0.089 scene units; envelope va chạm0.090 bao gồm iris/pupil cong. Contact shell cơ sở0.100 và corrective margin tối đa+0.006 ở nhắm kín. Full closure có tiếp xúc/chồng mép mí nhỏ có chủ đích; lining còn có các vùng tự giao chưa được chứng minh hợp lệ, xem số đếm đầy đủ trong source audit. Không gọi là facial retopology production.

Blink giải bằng các pose knot25/50/75/100 và nội suy kề; camera review gọi đúng mapping cho cả Blender report và GLB. Cùng Basis/Smile key không được bật đồng loạt khi kiểm blink. Không thêm blink animation hoặc đổi action body.

## Phép đo va chạm

`assets/source-audit.json` đọc lại file `.blend` độc lập:

- Từng skin triangle gần mắt được đo bằng closest point trên tam giác tới tâm envelope sphere; không chỉ đo khoảng cách vertex. Mọi tam giác xuyên được đếm.
- BVH ray từ hai góc nhìn tới các mẫu disk của hai globe, yêu cầu không mẫu nhãn cầu nào lộ ở100%.
- Thực hiện cùng phép đo cho P3.1 để chứng minh negative control bắt lỗi cũ.
- Self-BVH liệt kê số cặp tam giác không kề nhau overlap ở các mức Blink. Đây là candidate contacts/intersections cần phân loại, **không tự coi tất cả là tiếp xúc mí hợp lệ**.
- Head–lip/oral insert triangle overlap được đếm riêng ở Smile0/50/100%; có root embedding nhưng chưa certified collision-free.

GLB được kiểm độc lập bằng unlit ID pass: chỉ skin head/lids xanh lá và globe/iris/pupil đỏ; vật khác ẩn, material tạm thời rồi phục hồi. Đếm mọi pixel đỏ, không crop bỏ góc mắt hay dùng tolerance để bỏ điểm lộ. Open-eye control phải có>100 pixel mắt và P3.1 full-blink phải lộ; nếu không detector không hợp lệ. Beauty PNG được chụp với studio gốc; ID PNG chỉ là diagnostic, không phải chỉnh ảnh beauty.

Giới hạn: sphere envelope/ray sampling không phải arbitrary-mesh collision solver toàn nhân vật. Không đo liên tục mọi blend hoặc chứng minh self-intersection-free. Các contact chưa phân loại vẫn là lỗi mở.

## Miệng và má

Tái tạo môi có độ dày, khóe, vermilion và oral interior; dùng Smile map chung cho head/cheeks/lips/interior. Khóe nâng và mở rộng, cheek lên/trước, môi dưới mở nhẹ thay nét cười phẳng. Source audit ghi finite geometry, zero-area triangles và bounds môi ở0/50/100%; GLB có ảnh cả0°/45°.

Dạng môi vẫn procedural và có thể lộ đường nối/khóe hoặc nếp V không tự nhiên. Không tuyên bố expression đạt phim hoạt hình; head–lip contacts trong audit chưa được xử lý thành oral topology liên tục.

## Tóc

Thay chín object tóc (foundation+8 leaves) bằng một volume closed có lobes/grooves/side-sweep và hairline biến thiên bất đối xứng; thay silhouette thật, không tăng số lớp trang trí. Tóc vẫn có thể đọc như khối cap ở một số góc, cần người dùng duyệt ảnh. Chưa có groom strands, texture bake art hoặc artist sculpt; không lấy một mesh kín làm bằng chứng tạo hình đạt.

## Kiểm tra dữ liệu và ngân sách

- Read-back bảo toàn122 mesh gốc (gồm C/P2/P3.1), rig/rest matrices/action curves. Bản sao ear/brow trong R giữ geometry gốc, không redesign.
- New collection15 objects; head/socket/lid một mesh. `mesh` trong source audit có manifold, boundary, winding, signed volume và UV hữu hạn. Không chứng nhận UV overlap/distortion.
- `assets/glb-audit.json`:206034 triangles/59 primitives toàn asset; P3.1:225446/71. Primitive là đơn vị draw tiềm năng, **không đồng nghĩa draw calls đo thực tế**.
- `BUDGET.json` ghi draw calls và rendered triangle count theo engine/góc/frame thực tế từ Three renderer. Frustum culling, studio và pass ảnh hưởng số đo; không quy đổi thành FPS iPhone.
- Custom GLB audit đọc cả sparse morph, bounds/index/accessor finite, normals/weights. Đây không phải Khronos certification. Bốn ear/brow mesh sao chép nguyên dữ liệu dùng tên data P31, các geometry mới dùng P31R và được audit riêng.

## Giao thức so sánh

Cùng GLB studio đã dùng ở P3.1:35° vertical FOV, viewport1500×1100 DPR1, Idle time0, target/camera/angle khóa theo P3.1 (sai số<1e-6). Cả hai asset normalize height2.2 theo cùng importer review. Canvas ghi riêng từng engine; không so pixel giữa Chromium và WebKit. Không đổi lighting/exposure/grading hoặc resize từng ảnh để tạo cảm giác cải thiện.

Hai engine Linux chạy import/render thật, không gửi request Supabase. ID/material override chỉ dùng diagnostic và được phục hồi trước beauty ảnh tiếp theo. Không công bố FPS hay xác nhận phần cứng Apple từ GPU/user-agent string.

## Hạn chế còn lại

Gates kỹ thuật hẹp đạt không chứng minh mỹ thuật9/10, facial rig production hay không tự giao toàn đầu. Các self-contact/overlap, eyelid volume, lip seam, natural expression và silhouette tóc vẫn phải đánh giá bằng ảnh và report. Không chuyển P3.2 hoặc tự mở rộng body/animation/ba nhân vật khác.
