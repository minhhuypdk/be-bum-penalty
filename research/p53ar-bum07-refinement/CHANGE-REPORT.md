# BUM07 P5.3A-R Geometry and Art Report

Ngày20/11/2026. Baseline5dd8744. P5.3A được chấp nhận kỹ thuật, mỹ thuật chưa duyệt. File P5.3A-R là refinement của native hiện có; chưa được gọi là nhân vật hoàn thiện hoặc đạt9/10.

## Thay đổi hình học

| Vùng | Chỉnh sửa trên model hiện có | Giới hạn |
|---|---|---|
| Nhãn cầu/iris | Dịch cả nhãn cầu vào hốc0.017H, giữ cầu đường kính0.212H; iris/pupil theo cùng chiều sâu, chỉnh hướng nhìn bằng quay quanh tâm globe và độ cong cap iris | Chưa có rig/gaze tracking; không suy ra khả năng xoay hoặc Blink đã đạt |
| Hốc/mí/má | Recess vùng orbital, làm dịu bọng mí; thư giãn cục bộ mesh, thêm độ đầy má | Khóe mắt và chuyển tiếp mí còn cần nghiệm thu hình ảnh |
| Mũi | Rút đầu mũi/bridge, mở ngang tip, giữ nostril đi cùng bề mặt | ROI đỉnh mũi trước giảm reach từY≈−0.4255H xuống≈−0.3613H; không phải số đo giải phẫu từ concept |
| Cằm/hàm/môi | Mở mềm vùng cằm thấp mà không đổi cao độ sọ–cằm; môi có thêm thể tích, đường miệng nhỏ và dịu hơn | Nụ cười vẫn neutral; không facial animation/biểu cảm production |
| Tóc | Thư giãn mesh tóc cũ, giảm mép cứng, chỉnh mái thấp và bất đối xứng; làm mềm gáy | Vẫn là các cụm blockout, chưa tóc sculpt chuyên nghiệp hoặc sợi tóc |
| Tai/cổ | Làm nhỏ/êm shell và helix, flaring nhẹ cổ trên vào hàm | Mesh đầu/cổ vẫn là thành phần riêng, chưa nối để deform |
| Cổ/piping/gấu | Dải trim theo boundary mặt áo thực, thay phần tube bị chiếu xẹp bằng ribbon mỏng; gấu áo được nới cục bộ để bao quần | Không pattern may hoặc mô phỏng vải; toàn thân vẫn blockout |

Sau làm mềm, audit phát hiện6mặt tóc bị co về diện tích0. Giữ3% vị trí gốc trong bước thư giãn đã khôi phục khoảng cách vertex; audit cuối còn0mặt dưới ngưỡng1e-12H², không xóa/thêm face hoặc đổi connectivity.

Không tạo lại mesh đầu, tóc hoặc nhân vật. `lineage-audit.json` kiểm topology hash head/hair/thân áo trước/sau, tên toàn bộ object và dữ liệu camera/đèn. Số07/BUM và object tám răng không đổi hình học. Thay đổi topology chỉ ở sáu dải trim cục bộ, không retopology thân/đầu/tóc để rig.

## Lỗi gấu áo và phép kiểm tra

Lỗi không chỉ ở dải viền: phần trên quần đứng trước áo ở cùng vị trí chiếu. Trước sửa, tạiZ=2.442H,24/41tia front gặp quần trước áo. Sau nới hai vòng thấp của thân áo,41/41tia ở mỗi cao độ2.442/2.47/2.49/2.51H gặp áo trước quần. `hem-baseline.json` là kiểm tra riêng từ file5dd8744, `hem-after.json` từ native R; không đánh đồng các kết quả khác nguồn.

Các phép tia chỉ là mẫu tĩnh trên dảiX=−0.44..0.44H, không chứng minh mọi giao cắt hoặc biến dạng khi chạy. Số07 vẫn nằm trên áo; audit ghi khoảng cách tới surface, chiều cao trước0.38H/sau0.42H và kiểm tra riêng không để chữ bị vải nuốt.

## Ngân sách hình học và tỷ lệ

| Chỉ số | P5.3A | P5.3A-R |
|---|---:|---:|
| Tam giác evaluated Blender | 1.183.138 | 1.180.578 |
| Sọ–đất/H thực | 5.0006749 | 5.0006749 |
| Cao tính tóc/H thực | 5.1621987 | 5.1332721 |

Giảm2.560tam giác, không tăng subdivision để tạo cảm giác chi tiết. Counts là evaluated mesh trong Blender, không phải GLB hoặc draw calls.1H danh nghĩa là một scene unit, chưa khóa số mét. Số đo H thực lấy từ bbox vertex mesh đầu và đáy studs, không chỉ empty mốc.

## Vật liệu và so sánh render

Giữ10màu nền P5.2R; roughness nằm trong khoảng đã đề xuất, metallic0. Iris/pupil/sclera được chỉnh phản xạ và coat, tóc giảm highlight cứng, môi bớt bóng. Camera, đèn, world, AgX và look giữ nguyên so với P5.3A. Không vẽ catchlight lên PNG.

Bộ before là sáu PNG thật từ5dd8744, kiểm SHA khớp nguồn. After là sáu render thật1200×1600,64samples CyclesCPU, không denoise hoặc retouch. Metadata kiểm cùng model trước/sau từng render, cùng camera/ánh sáng với before. PDF P5.2R là AI concept có camera chưa kiểm chứng; chỉ P5.3A và R là cặp camera/đèn3D đối chiếu trực tiếp.

`glare-proxy.json` dùng hull iris chiếu từ3D và một ngưỡng sáng cố định để đếm vùng trắng. Đây là chỉ báo ảnh, có thể chứa vùng bị mí che, không phải specular render pass hoặc bằng chứng ánh nhìn tự nhiên. Xem số liệu cùng PNG và tự nghiệm thu, không lấy giảm glare làm PASS mỹ thuật.

## Khoảng hở iris và sclera

Ảnh cận lớn của bản R trung gian phát hiện iris bị sclera cắt mép: dịch cap bằngX/Z khiến16vertex mỗi iris lọt dưới mặt cầu, clearance tối thiểu−0.000383H. Đã thay bằng phép quay iris/pupil quanh tâm globe, giữ cap ở ngoài cầu. Audit cuối:0vertex dưới globe, clearance iris tối thiểu≈0.000892H và pupil≈0.006115H. Đây là kiểm tra riêng, không mượn PASS của ray aperture để thay thế.

`optical-clearance-pre-repair.json` là chẩn đoán trung gian, `optical-clearance-final.json` là native cuối. Camera và đèn không thay đổi.



Trong4ROI iris, proxy vùng sáng trung tính từ20.53–39.54% xuống10.82–12.86%; cả4ROI đều giảm. Đây không phải tỷ lệ năng lượng phản xạ hoặc điểm mỹ thuật; threshold/mask và từng mắt nằm trong glare-proxy.json.

## Bounding box curve

Nguyên nhân đã được tái hiện trước khi chỉnh model: `evaluated.bound_box` của curve trong Blender4.3.2 dùng một ước lượng nới theo point radius, phóng bounds rất lớn so với bevel thật. Vertex evaluated và transform không có lỗi tương ứng. Không dùng số liệu này để thu nhỏ hoặc kéo curve về gốc. Chi tiết ở `CURVE-BOUNDS-AUDIT.md`, gồm thử nghiệm ba trường hợp trên bản sao trong bộ nhớ và bounds thật trước/sau.

Point radius giữ nguyên. Control point và bevel của mí/tai/miệng có thay đổi vì yêu cầu mỹ thuật, được tách khỏi sửa phương pháp audit. Audit mới đo bounds trực tiếp từ vertex evaluated, vẫn lưu bbox sai/ước lượng của Blender để không che nguyên nhân.

## Những phần chưa đạt

- Tóc mềm hơn nhưng vẫn có rãnh dài/khối lớn, hairline và gáy chưa có độ tự nhiên của conceptB. Không đánh dấu tóc hoàn thiện PASS.
- Mắt bớt glare và đã lùi vào hốc, nhưng ánh nhìn, khóe mí và cảm giác sống động vẫn cần chủ dự án duyệt. Kiểm tra hình học tĩnh không chứng minh mắt đẹp hoặc hết mọi lỗi ở từng pixel.
- Môi/tai/cằm và tiếp giáp cổ chưa phải sculpt cuối; model vẫn có dáng và bề mặt blockout. Trang phục chưa chất vải/nếp gấp đẹp; tay, giày và dải tất không nằm trong refinement lần này.
- Chưa skin/rig, facial animation, DQS, UV/retopology production, GLB, kiểm biến dạng hoặc đo iPhone. Không tự mở rộng sang P5.3B.

**Đầu ra để chủ dự án nghiệm thu ngoại hình. Không tự tuyên bố đạt9/10 hoặc coi audit/đóng gói thành công là nghiệm thu mỹ thuật.**
