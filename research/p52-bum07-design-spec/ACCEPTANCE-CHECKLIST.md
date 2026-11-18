# P5.2 — Tiêu chí PASS / FAIL và cổng nghiệm thu

**B/Field Breeze là quyết định đã chốt. P5.2 vẫn chờ chủ dự án xem ảnh.** PASS kiểm tra hồ sơ không tự động là PASS mỹ thuật hoặc quyền triển khai Blender.

| ID | PASS khi… | FAIL khi… | Trạng thái hiện tại / bằng chứng |
|---|---|---|---|
| D01 |Nhánh riêng từ35997cc, chỉ thêmP5.2/đóng gói hồ sơ |Sửa lịch sử/main/Pages/PR2/Supabase/nhân vật khác |Kiểm tra phạm viGit và snapshot bảo vệ; không truy cậpSupabase |
| D02 |Có6 PNG turnaround0/45/90/180,A-pose,cậnneutral |Thiếu góc, dùng cùng góc gắn nhãn khác hoặc cắt mấtchi |PASS về đủ tệp; danh mụcảnh ghi kích thước gốc1024×1536 |
| D03 |Có8 trạng thái×2 góc, mỗi góc mộtPNG |Thiếu trạng thái/góc, gọi ảnh AI làrender Blender |PASS về đủ16 PNG; tất cả được đánh dấuDESIGN ONLY |
| D04 |Cùngcanvas/thước H, không kéo giãnriêng đểkhớp |Dùng khácscale/phối cảnh mà giấu trongbáocáo |PASS về bố cục tài liệu1:1; cameraorthographic thậtNOT_VERIFIED |
| D05 |Có bảng tỷ lệ/màu/cấu trúc và phân biệtproposed/mesh |Ghi sốmesh hoặcFPS không có thật |PASS tài liệu; `meshMeasurementsExist=false` |
| D06 |PDF mở đủ trang/ảnh,PNG không hỏng vàcóchecksum |PDF thiếu ảnh/cắt nội dung,PNG giảđịnhupscale4K |Kiểm tra readbackPDF/PNG; không nội suy phóng lớnPNG |
| A01 |Chủ dự án thấy cùngB ở mọi góc/biểu cảm |MặtScott, tóc A/C, tuổi/hàm/eye identity đổi rõ |Quan sát giữ nhận diệnB; **OWNER_PENDING** |
| A02 |Chốt5 H,địnhnghĩaH và độ nhôtóc; contour tương thích |Lấy ảnh AI làđo3D, tỷ lệtrôi không đượcgiảiquyết |**PROPOSED / OWNER_PENDING**; dùng thước H, xemC02 |
| A03 |Ngôi/hairline thống nhất, mái thấp, không curls/cowlick |Mirror ngôi giữa ảnh hoặc tóc thànhthiếtkếkhác |Khóa quyước ngôi trái; rãnh/độ phồng còn cầnduyệt,C03 |
| A04 |Mắt/socket/lid, tai/mũi/má đọc như cùng khối |Globe/khoảngmắt/khốisọ đổi đểtạo biểu cảm |Ý đồ giữ; **NOT_VERIFIED_IN_3D**,C04/C09 |
| A05 |Một cung răng, lips/jaw/cheeks chuyển hợp lý |Răng/miệng thànhmẫu khác hoặc nụ cườiđườngphẳng |**NEEDS_REVIEW**,C05; chưa cómesh đểxácnhận |
| A06 |Blinkđíchđóngkín,Focused/Surprised/Disappointed/Celebration rõ vàphùhợp |Blinkhởtrongthiếtkế, biểu cảmquáhungdữ/khôngphânbiệt |Cóảnhđích; cường độ**OWNER_PENDING**; không phảiocclusionPASS |
| A07 |CổVtrước/bo sau,07/2dảitất/kit đúng vàmặt sauđược duyệt |Vởsaugáy,đổi07,thêmnhãnhiệu,viềnvảimâu thuẫn |Quan sátđúngnhận diện; vị trítext/nếp vải/mặt sau**NEEDS_REVIEW**,C07/C08 |
| A08 |Chủ dự án duyệt palette/material direction |Coi HEX/roughness là shaderđãkiểmthử |**PROPOSED_NOT_SAMPLED / OWNER_PENDING** |
| G01 |Có phê duyệt P5.2 rõ ràng trước Blender |Tựdựngmesh/rig/xuấtGLB/tích hợp game/chấm9/10 |**CỔNG ĐÓNG — CHƯA ĐƯỢC PHÉP BLENDER** |

Không tự đổiNOT_VERIFIED/OWNER_PENDING thành PASS. Nếu có mâu thuẫn lớn về nhận diện/tỷ lệ/cung răng, tiêu chíA tương ứng phảiFAIL ởvòng nghiệm thu và ghi điều cần sửa. Có thể duyệt cóđiềukiện một vài chi tiết nhỏ nhưng quyết định và phạm vi được duyệt phải do chủ dự án ghi rõ.

Các kiểm tra mesh/rig/UV/normals/skin/collision/FPS chỉ có thể đặt cho giai đoạn sau khi cómodel; P5.2 không thực hiện và không mượn kếtquảP4.1R. Không tự merge PR2 hoặc chuyển giai đoạn sau bàn giao.
