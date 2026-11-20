# P5.3B.1 — Báo cáo kỹ thuật và mỹ thuật

Ngày: 20/11/2026 (Asia/Saigon). Baseline `cebfbe1`; chỉ đầu/tóc BUM 07, cổ/vai làm ngữ cảnh. P5.3A-R được chấp nhận kỹ thuật trước đó, chưa được chấp nhận mỹ thuật. Kết luận của vòng này **FAIL_ARTISTIC_OBJECTIVE**, chờ chủ dự án xem ảnh; không đề nghị mặc nhiên duyệt và không chuyển giai đoạn.

## Tham chiếu và giới hạn phép so sánh

- Nguồn nhận diện chính: concept B/P5.1 và P5.2R đã chấp nhận có điều kiện. Sao lưu ảnh B và cận mặt P5.2R trong `reference/`. Đây là concept AI, không phải model 3D hoặc phép đo từ mesh.
- Bản R nguyên byte được giữ ở `reference/bum07-p53ar-preserved.blend`; provenance có SHA-256 đối chiếu file nguồn. Không lấy mesh Scott.
- R và B1 front/45 dùng cùng camera ORTHO 1.5H, đèn, world, AgX và look. R before PNG được sao chép nguyên byte từ hồ sơ cũ. B1 là bust nên ánh sáng gián tiếp có thể khác vì thân dưới bị cắt; vật liệu da/tóc/iris thay đổi có chủ đích. Không tuyên bố hai scene hoàn toàn giống nhau.
- B1 90/back là góc kiểm tra bổ sung từ cùng model, không gán là cặp trước/sau cận mặt mà R chưa bàn giao. Concept không đăng ký cùng camera/pixel với render Blender.
- Không hình AI thay render, không chỉnh sửa PNG sau render. Các ảnh preview ít samples chỉ là chứng cứ chẩn đoán, không phải bộ cuối.

## Thay đổi hình học thực

| Vùng | Thao tác trong file nghiên cứu mới | Kết quả quan sát / giới hạn |
|---|---|---|
| Đầu, trán, má, mũi, môi, cằm | Thay mặt cũ bằng surface mới có phân bố điểm riêng quanh mũi/môi, trường hình khối liên tục và back surface; nối kín | Có thay hình học thật. Nhưng mặt trước vẫn phẳng, khối môi/má thiếu chuyển tiếp tinh tế; cằm nhô bất thường ở profile. Không đạt mục tiêu sculpt mỹ thuật |
| Hốc mắt/mí/khóe | Hai orbital patch nối với đầu, thành hốc kín sau nhãn cầu; globe nhỏ hơn và nằm sâu; waterline mảnh | Giảm dạng hốc tròn cũ nhưng mắt vẫn thiếu thần thái, khóe chưa mềm và mí chưa dày tự nhiên. Độ đẹp/ánh nhìn: FAIL |
| Nhãn cầu/iris | Globe cầu, cap iris/pupil quay quanh tâm thay vì dịch độc lập; iris nâu UV procedural, specular thấp hơn | Có khoảng cách xuyên tâm dương. Không suy ra Blink hoặc biểu cảm đã đạt: vòng này không có shape keys/rig |
| Tai | Mesh trước/sau liền với concha và helix relief thay vòng dây cũ | Ít dạng dây hơn nhưng relief còn thô/đều; tai vẫn là component riêng, chưa nối biến dạng |
| Tóc | Xóa cấu trúc rãnh cũ trong file mới. Dựng volume theo đường mọc, bốn cụm mái bất đối xứng, voxel union và làm mềm | Đã thay topology thật, nhưng silhouette vẫn như mũ và mái như dải chồng. Không đạt tóc mềm tự nhiên của B |
| Cổ/vai | Giữ hình học cổ và crop phần vai/áo cũ ở Z=3.40H | Chỉ ngữ cảnh; không cải thiện trang phục hoặc nối đầu–cổ để deform |

Màu anchor giữ hướng đã duyệt: da `#D9A078`, tóc `#241D1A`, iris `#4E331D`; màu áo/navy kế thừa R. Tint môi/má là biến thiên vật liệu, không phải lý do tuyên bố sculpt đạt. Số 07/toàn bộ outfit vẫn nằm trong bản R; bust hiện tại không cố tái dựng số trên phần áo đã crop.

## Kiểm tra hình học

Dữ liệu gốc: `evidence/native-audit.json`; đếm trên mesh evaluated, không dùng bbox curve bị nới giả.

- Tổng bust: **574,016 tam giác**. Đây là sculpt nghiên cứu nặng, **không phải budget game/iPhone**.
- Đầu gồm orbital: **49,132**; tóc voxel: **443,524**; tai R/L: **9,028 / 9,026**. Số còn lại là mắt/curve/phần vai/cổ. Không so tổng này với R toàn thân để tuyên bố tối ưu.
- Đầu/tóc/tai/globe: volume signed dương sau recalc normals, 0 cạnh non-manifold và 0 mặt diện tích dưới `1e-12 H²` trong phép kiểm tra này; tọa độ finite. Đây không phải chứng minh không tự giao hoặc topology animation đạt.
- Iris/pupil/brow/curve đầu mở và piping/crop áo có biên hợp lệ theo cấu tạo. Audit ghi tất cả; không gọi các biên này là mesh kín hoặc xóa để vượt kiểm tra.
- Lỗi đường nối đầu phát hiện khi build: 482 cạnh biên do tọa độ float32 CDT đi qua hàm lũy thừa tạo sai số Y mặt trước/sau. Chẩn đoán trong `head-seam-diagnosis.json`. Sửa bằng nhận diện đúng input contour và ép cùng Y seam, không weld toàn đầu bằng ngưỡng lớn. Sau sửa đầu kín, không thay ảnh để che lỗi.
- Iris/pupil: 0 vertex nằm dưới bán kính globe; clearance cụ thể trong JSON. Đây chỉ là kiểm tra khoảng cách xuyên tâm, không phải kiểm tra va chạm hoàn chỉnh hoặc pass Blink.
- Sọ từ Z=4 đến Z=5: **1H**; tóc cao nhất Z≈5.14135. Giữ hệ tọa độ thiết kế nominal 5H, nhưng **không có model toàn thân B1 để xác nhận tỷ lệ toàn thân thực đo 5H**.
- B1 chỉ có miệng khép neutral, chưa dựng khoang miệng/cung răng mới. Cấu trúc răng lịch sử vẫn giữ trong native R riêng; không lấy neutral làm bằng chứng Smile/teeth đã đạt.
- Không có armature/action/shape-key facial rig. Không test skin deformation, Blink, Smile, sports animation, WebKit/Chromium GLB, FPS iPhone hoặc draw calls game; các việc này ngoài phạm vi và không được suy diễn từ render CPU.
- Mesh dựng dạng triangulated/voxel, không phải edge-loop facial production hoặc retopology hoàn chỉnh; UV đầy đủ cho toàn đầu/tóc chưa triển khai. Iris có UV riêng. Không tuyên bố sẵn sàng GLB production.

## Đánh giá mỹ thuật so với B

1. **Đầu/profile chưa đạt:** chẩm/đỉnh còn cồng, mặt và trán chuyển tiếp đơn giản; cằm nhô thành mấu ở 90°, thiếu oval mềm của concept. Phải sculpt silhouette thủ công, không sửa bằng ánh sáng.
2. **Mắt chưa đạt:** giảm hốc/lồi kiểu cũ nhưng khoảng trắng/iris, bờ mí và chuyển tiếp góc 45° còn đồ chơi; ánh nhìn thiếu cảm xúc. Catchlight ít hơn không đồng nghĩa có hồn hơn.
3. **Mũi/môi/má chưa đạt:** tip mũi và môi có volume nhưng môi còn như đường cười mảnh, thiếu khóe/pillows; má và rãnh mũi–má quá ít chuyển tiếp.
4. **Tóc chưa đạt:** các cụm đã union, song khối nền giống mũ, hướng tóc chưa thuyết phục ở profile/back. Không nên coi remesh là sculpt nghệ thuật thành công.
5. **Tai/cổ chưa đạt:** tai bớt dạng dây nhưng còn relief cứng; đầu/cổ tách component và đường cằm nối cổ chưa tự nhiên.

So trực tiếp R/B1 cho thấy một số chi tiết còn kém hơn R: môi B1 mờ/ít volume hơn, tóc B1 bớt rãnh nhưng tăng cảm giác mũ. Vì vậy không mô tả mọi thay đổi là cải thiện. Không có cơ sở xác nhận “bước tiến lớn”, “cao cấp”, hoặc 9/10. Đây là thất bại đạt mục tiêu mỹ thuật của phương pháp procedural trong vòng thử có giới hạn; vẫn có file và render thực tế để kiểm chứng. Không tiếp tục vô hạn các vòng tham số.

## Vì sao cách procedural này chưa đủ

- Mặt được tham số hóa theo mặt phẳng X/Z rồi tính độ sâu Y. Các trường lồi/lõm trơn giúp tạo volume liên tục nhưng không tự thiết kế được mặt phẳng xương mềm, phần môi cuộn vào trong, cánh mũi hay quan hệ má–khóe như một sculpt có chủ đích. Ghép trước/sau tại contour cùng tham số còn tạo đường cằm nhọn ở profile dù mesh kín.
- Band orbital nội suy từ da tới khẩu độ globe xử lý kết nối kỹ thuật; nó không tự sinh các lớp giải phẫu mí/khóe đủ tinh tế hoặc ánh nhìn hấp dẫn.
- Tóc xuất phát từ một khối scalp gần ellipsoid, cộng relief theo đường và các mái rồi voxel-union. Remesh chỉ hợp nhất vật chất; không phá được cảm giác cap nếu silhouette/khối chính chưa được artist thiết kế tốt. Tăng mật độ voxel không sửa nguyên nhân này.
- Audit finite/manifold và số tam giác không đánh giá các quyết định nghệ thuật trên. Vì vậy dừng thử theo hướng này sau một cấu trúc chính; chỉ sửa lỗi seam số học đã xác định, không kéo dài bằng nhiều bản tham số.

## Hướng xử lý khi được chủ dự án cho phép

Xem `MANUAL-SCULPT-WORKFLOW.md`: giữ scene/camera/thước H, sculpt thủ công khối chính bằng Grab/Clay/Smooth; chốt silhouette rồi mới orbital/lips/hair. Codex có thể tự động reference layout, lưu phiên bản, render đa góc, audit và đóng gói. Codex trong môi trường hiện tại không cung cấp thao tác sculpt bằng tay có phán đoán nghệ thuật tương đương artist. Chưa thực hiện workflow thủ công, chưa có artist được thuê, chưa tạo giai đoạn kế tiếp.

## Kiểm tra hồ sơ

PDF gồm 8 trang, đã trích văn bản và kiểm tra bounding text nằm trong trang; xem trực tiếp trang so sánh và trang kỹ thuật. Poppler có cảnh báo ICCBased profile của ảnh tham chiếu nhúng, nhưng các trang kiểm tra hiển thị/đọc được. PNG Blender nguồn giữ nguyên. Native mở lại thành công, không library/image/font ngoài chưa đóng gói; kiểm tra này chứng minh khả năng mở file, không nghiệm thu mỹ thuật. Xem `evidence/handoff-verification.json`.
