# P5.2 — Kiểm tra nhất quán và khác biệt còn lại

**B đã được chọn, nhưng P5.2 chưa được chủ dự án nghiệm thu.** Đây là đánh giá ảnh và tính đầy đủ tài liệu, không phải auditmesh. Không tự chấm9/10, không tự cho phép triển khaiBlender.

## Những điểm đã giữ được ở mức quan sát2D

- 6 PNG turnaround riêng:0°,45°,90°,180°,A-pose và cận mặtneutral. Tất cả1024×1536 gốc, không nội suy/phóng to file hoặc kéo giãn riêng để làm tỷ lệ trông khớp.
- 16 PNG biểu cảm:8 trạng thái×2 góc. Neutral front trùng byte với cận mặtturnaround, giữ một mốc neutral. Các portrait được tạo từ mốcneutral tương ứng, không dùngScott/A/C làm ảnh đầu vào.
- Mặt oval, mũi mềm, mắt hạnh nhân, mái ngắn thấp và hướng quét tóc; không thêmchỏm cong hoặc tóc xoăn của A/C. Bản sau lưng đã bỏ các cuộn tóc quá tròn ở nháp.
- Áo vàng07, cổV nông trước/cổbo sau, navy, hai dải tất, giày bóng đá giữ xuyên bộ. Hình sau lưng/07 sau lưng là đề xuất mới, không coi đã có phê duyệt từP5.1.
- DángA-pose cuối dùng lại khung dọc và mốcfront, không dùng nháp khungngang có thể làm đầu trông nhỏ. Camera0/45/90/180 dùng cùng dáng đứng, không thêm bóng hoặc gócngẩng/cúi để che tỷ lệ.
- Happy/BigSmile/Celebration có mức mởhàm/mí/mày khác nhau; Blink vẽ hai mắt đóng, không phát hiện phầniris lộ bằng quan sát thông thường. Đây **không phải phép đo occlusion**.

## Những điểm chưa được chứng minh hoặc còn cần xử lý

| ID | Điểm cần chốt | Trạng thái ởP5.2 | Hướng xử lý sau duyệt hoặc vòng sửa thiết kế |
|---|---|---|---|
| C01 |Camera orthographic thật/cùng mesh |NOT_VERIFIED |Hiện chỉ orthographic-style và bố cục thước H; không cócamera/mesh để đo góc 45 chính xác |
| C02 |Tỷ lệ5 H tuyệt đối trênmọi góc |PROPOSED / OWNER_PENDING |Sọ bị tóc che nên không suy ra số đo3D từPNG; dùng bảng H và mốcfront đểchốt. 5 H không tínhtóc, tốiđa5,2 H tínhtóc là đề xuất |
| C03 |Hairline/phân cụm tóc duy nhất |NEEDS_REVIEW |Rãnh tóc vàđộ phồng thái dương/gáy thayđổi nhẹ giữa45/90/180. Khóa ngôi trái/hairline, khôngcoi từng sợiAI làgeometry |
| C04 |Tai, chiều sâu má, nhô mũi |NEEDS_REVIEW |Góc nghiêng là diễn giảiAI, chưa thểkhẳngđịnhcùng khốivới0°. Cầnchốtcontour khiownerxemcạnhnhau |
| C05 |Cung răng nhất quán |NEEDS_REVIEW |Bềrộng/thứtự tooth silhouettes khác nhỏ ởBigSmile/Celebration; đề xuất8răng trên, không khechủý, cầnmột templaterăngtrước khi dựng |
| C06 |Focused/Disappointed/Celebration intensity |OWNER_PENDING |Focused hơi cau mày; Celebration nheo khá rõ. Không tựcoi đây làcường độcuối |
| C07 |CổV, piping, nếp vải, 07 |NEEDS_REVIEW |Nếpvải/viềncổ và vị trí projectedtext cóđộ trôi giữa ảnh. Dùngtemplate/địnhvịtrongguide, khôngcopychữphốicảnh trực tiếp |
| C08 |Mặt sau/gáy/back07 |NEW_PROPOSAL_PENDING |Không cóảnhsau gốcP5.1; cầnnghiệm thu riêng |
| C09 |Mí–globe, deformation, topology, UV |NOT_TESTED_NO_MESH |Không cómodel/rig. Tuyệtđốikhông kếthừaPASS Blink/skin củaP4.1R |
| C10 |Màu vàroughness |PROPOSED_NOT_SAMPLED |ẢnhAI cóshadingấm/độ bóngkhácnhẹ; HEX/matlàđề xuất, không phảiđo thực |

Không dùng histogram, sốpixel trongảnh AI hoặc việcghi chữ45° để chứng nhận mô hình học 3D. Nhữngđiểmchưađược chứng minh không được tựđổi thành PASS.

## Bản đo kèm theo thực sự thể hiện điều gì

`turnaround-measurement-layout.svg` là bố cục tài liệu vector, đặt 4 PNG đúng 1024×1536, không thayđổi tỉ lệ từngảnh, rồi vẽ thước H đề xuất dùng chung. Đất đặtởy1408, đỉnhsọ giảđịnhy96;1 H = 262,4pixel trongbố cục. Thước giúp thấy chênh lệch, **không phải phép đo giải phẫu từ mesh hoặc camera orthographic đã được kiểm chứng**. Các sơ đồmắt/môi/màu cũng làđề xuất2D.

## Kết luận bàn giao

Tài liệu đã đủ các loại ảnh/bảng/hướng dẫn được yêu cầu để **chủ dự án xem và nghiệm thu thiết kế**. Chưa có căn cứ xác nhận tất cả các góc là một khối3D tuyệt đối hoặc đã đủ nghiệm thu sản xuất. Chủ dự án cần duyệt các điểmC01–C10 phù hợp trước khi cho phép Blender. Không dựngmesh/rig/GLB hay tích hợp game trongP5.2.
