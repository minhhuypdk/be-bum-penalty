# BUM tiền đạo 07 — hồ sơ sản xuất và giới hạn hiện tại

## Trạng thái: nghiên cứu kỹ thuật, chưa nghiệm thu mỹ thuật

Bản C **không đạt/chưa được xác nhận đạt 9/10**, không phải nhân vật điện ảnh hoàn chỉnh. Nó là mô hình tạo bằng script Blender với bề mặt đầu được định hình riêng, khối cơ thể/bàn tay hợp nhất, tóc dạng vỏ có rãnh định hướng, trang phục và skeleton FK. Nó không phải sculpt thủ công của họa sĩ. Tóc hiện có thể còn cảm giác mũ/vỏ, mắt/mí và miệng chưa đủ tinh tế; không dùng số polygon hoặc bốn clip làm bằng chứng đạt chất lượng cao.

Không có mesh, texture, rig hoặc animation Snow nào được sao chép vào C. Snow vẫn là bản B để tham khảo kỹ thuật và không được sử dụng làm BUM bằng cách đổi màu/thu nhỏ. Mô hình C và `.blend` được tạo độc lập trong repository này; không mua asset, không nhập font/logo/texture bên ngoài. Logo mặt trời và số 07 dùng hình vector tự dựng. Mô hình gốc cũ A và Snow B được giữ nguyên.

## Phạm vi được phép

Chỉ **BUM tiền đạo số 07**. Các nhân vật BA cầu thủ, BA thủ môn và BUM thủ môn không có bản C và chưa được nâng cấp/nhân rộng. Chuyển sang một trong ba nhân vật đó phải trở về A. Chỉ thực hiện nhân rộng sau khi chủ dự án duyệt BUM 07.

## Thiết kế cần hoàn thiện

- Trẻ em hoạt hình, đầu/thân khoảng 1:3,5–4; sọ tròn, hàm mềm, má có thể tích thật. Không lấy đầu người trưởng thành rồi tăng kích thước.
- Mắt nâu tự nhiên, sclera vừa phải, bờ mí có độ dày, góc mắt/tear duct và mí trên che nhãn cầu hợp lý. Duyệt cả chính diện và nghiêng để loại mắt lồi/dán lên mặt.
- Mũi nhỏ liền bề mặt mặt; môi/mép và khóe miệng có topology biểu cảm, không dùng nét cười phẳng làm sản phẩm cuối.
- Tóc cần sculpt 3–5 mảng lớn có hướng chải và silhouette bất đối xứng, lọn chuyển tiếp vào chân tóc, đường rãnh nhỏ được bake. Không dùng ống cong hoặc một mũ tóc trơn làm tóc hoàn thiện.
- Áo vàng số 07, quần xanh đậm, tất, giày bóng đá; cổ áo, hem/cuff/đường may và folds do chuyển động. Badge riêng cho BUM, không dùng nhãn hàng ngoài.
- Bàn tay năm ngón, móng tay nhỏ, webbing/đốt ngón đúng; bàn chân trong giày, toe roll và cổ chân tự nhiên.

## Pipeline Blender để sản xuất asset chuyên nghiệp

1. **Thiết kế và sculpt**: dựng turnaround trước/nghiêng/sau, biểu cảm neutral/smile/focus; sculpt đầu mới bằng symmetry + proportional/Grab/Clay/Crease, giữ volume má/mí/môi. Đây là công việc cần bàn tay và phán đoán của họa sĩ; script hiện tại không thay được bước này. Duyệt clay render không tóc để tránh che lỗi mặt.
2. **Retopology**: lưới quad có vòng liên tục quanh mắt/miệng; đủ loop cho khóe miệng, mũi, mí, cổ và khớp; kiểm tra manifold, normals, UV. Voxel mesh hiện tại chỉ là blockout/nguồn sculpt; không dùng nguyên trạng làm topology biểu cảm cuối.
3. **Tóc và trang phục**: sculpt tóc độc lập trên scalp, bake high-poly xuống mesh có silhouette đúng. Pattern áo/quần, thickness hợp lý, sculpt nếp theo vai/nách/khuỷu/eo, bake normal/AO. File nguồn giữ high-poly và low-poly riêng.
4. **Texture/PBR**: UV atlas không chồng ngoài vùng dùng chung có chủ ý; albedo sRGB, roughness/normal linear; nguồn mặt 4K, runtime mặt 2K và các vùng còn lại 1K khi kiểm tra thấy đủ. Chất liệu da không vẽ highlight giả; vải có weave/roughness, giày có upper/outsole/laces. Bake, kiểm tra dưới ánh sáng trung tính và studio.
5. **Rig hoàn chỉnh**: FK/IK tay/chân, pole controls, foot roll, toe bend; finger controls, twist joints; corrective shape cho vai/khuỷu/gối, blink/jaw/smile/cheeks/focus. Bản C hiện chỉ có skeleton FK có skin weights, chưa có hệ điều khiển/biểu cảm/correctives này.
6. **Animation**: Idle, Run in-place, Kick penalty có chân trụ và tiếp xúc bóng, Celebrate có anticipation/settle. Làm tay trong Blender hoặc dùng nguồn animation có quyền rõ ràng rồi retarget và cleanup. Bốn clip hiện tại là nghiên cứu FK bằng keyframe, không phải animation thể thao đã làm sạch hoặc mocap chuyên nghiệp.
7. **Đóng gói**: lưu `.blend` editable, bake pose/constraints sang deform skeleton khi xuất, GLB 2.0 nhúng texture; kiểm tra lại glTF trong viewer độc lập. Giữ bản gốc chất lượng cao, tạo LOD có bảo vệ vùng mặt và silhouette tóc. Gộp theo vật liệu, atlas và cân nhắc KTX2 sau khi có decoder tương thích; không bật nén chưa kiểm chứng trên Safari.
8. **Nghiệm thu**: render thật cận mặt/toàn thân/chính diện/3⁄4/nghiêng/sau và video bốn chuyển động; kiểm tra foot sliding, toe/hand penetration, mí mắt, áo xuyên người. Đo FPS + context loss/memory trên ít nhất hai iPhone thật, ghi rõ máy/iOS/DPR/LOD/thời gian. Kiểm thử tự động không chấm được 9/10; chủ dự án quyết định duyệt hình ảnh.

## Phương án nguồn và nhân lực

Ưu tiên tiếp tục miễn phí: dùng Blender và bộ nguồn C làm blockout để sculpt/retopo thủ công; Snow CC-BY chỉ dùng đối chiếu topology/rig/PBR. Chưa tìm thấy asset miễn phí sẵn có đúng danh tính, tuổi, áo số 07 và đủ rig/chuyển động để coi là BUM hoàn thiện. Nếu cần họa sĩ hỗ trợ, phạm vi giao việc chính là các bước 1–6, phải có nguồn editable và quyền dùng/sửa/phân phối mesh trên web/repository; chưa thuê hoặc mua bất kỳ dịch vụ nào.

## Tệp và cách kiểm tra

- `bum07-source.blend`: nguồn Blender editable được tạo mới, không chứa script Snow.
- `bum07-study-portrait.glb`, `bum07-study-mobile.glb`: file GLB thật; chỉ phục vụ nghiên cứu thiết kế và kiểm thử.
- `../../../scripts/assets/build-bum07.py` trong repository: script tái lập, dùng `blender -b --factory-startup --disable-autoexec -P ... -- /output`.
- Manifest/build report/audit ghi nguồn, hash và giới hạn. Không gán giấy phép CC-BY của Snow cho mesh C độc lập.

Không merge PR #2, không thay gameplay/mã multiplayer/Supabase, không đổi bản game công khai. A/B/C chỉ được triển khai trên Showcase riêng và có phiên bản trước để khôi phục.
