# BUM07 P5.2 — Character Design Specification

**Hướng B/Field Breeze đã được chọn. BộspecP5.2 chưa được nghiệm thu; cổng Blender vẫn đóng.**

Nhánh `research/p52-bum07-design-spec`, từ commit `35997cc84fdba629b347fac4725ddc39bf14a7b0`.

## Bàn giao

- `BUM07-P52-TURNAROUND-AND-GUIDE.pdf`: turnaround, mốc H, tỷ lệ, cấu trúc mặt/vật liệu và trạng tháinghiệm thu.
- `BUM07-P52-EXPRESSIONS.pdf`:8 trạng thái, mỗi trạng thái0°/45°.
- `turnaround/`:6 PNG riêng1024×1536 gốc.
- `expressions/`:16 PNG riêng1024×1536 gốc; Neutralfront trùngbyte với cận mặtturnaround.
- [Model Construction Guide](MODEL-CONSTRUCTION-GUIDE.md).
- [Expression Specification](EXPRESSION-SPECIFICATION.md).
- [Consistency Report](CONSISTENCY-REPORT.md).
- [PASS/FAIL checklist](ACCEPTANCE-CHECKLIST.md).
- `specification/`:JSON/CSV tỷ lệ,màu; sơ đồvector đề xuất và bố cục4 góc với thước H dùngchung.
- `review.html`:tài liệu đọc/in cục bộ, không deploy lênPages.

ẢnhAI concept, **không phải render Blender hoặc bằng chứng cómodel 3D**. Các camera/góc là ýđồorthographic-style; bố cục mốc H làtài liệuđề xuất, không phải phépđomesh. Xem báo cáo các điểmC01–C10 cònphải duyệt. Không cóBlender,rig,GLB sản xuất hoặc phépđohiệu năngP5.2.

`build-specification.py` chỉtạobảng/sơ đồvector tài liệu; `build-review.py` chỉlàmbố cụcPDF. Chúngkhôngtạomesh/rig và khôngchỉnhPNG. DùngHTTP cục bộ để đọcHTML nếu trìnhduyệt chặnfile://.

Không sửa main,Pages,Supabase,PR2,ba nhân vật khác hoặc P4/P4.1/P4.1R/P5.1. Dừng sau bàn giao; chỉtriểnkhaiBlender khi cóphê duyệt rõ ràng.

## Dạng tệp và cách tái tạo tài liệu

PDF được nén JPEG90 để xem thuận tiện; không cố ý downsample trong bước nén. **22PNG gốc vẫn nguyên byte**, có SHA256, không phải ảnh đã cắt từ contact sheet hoặc phóng lớn4K.

Từ repository root: chạy `python3 research/p52-bum07-design-spec/scripts/build-specification.py`, rồi `build-review.py`; xuất PDF bằng `node research/p52-bum07-design-spec/scripts/export-pdf.cjs`. Có thể chạy `optimize-pdf.py` đúng một lần sau khi xuất để nén bản PDF. Cần Playwright/Chromium, Ghostscript nếu nén; các bước này chỉ làm tài liệu, không khởi chạy Blender.
