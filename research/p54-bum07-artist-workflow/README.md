# BUM 07 — P5.4 Artist Workflow & Base Mesh Evaluation

Tên hướng A/B trong báo cáo chỉ cách sản xuất; cả hai giữ concept mỹ thuật B, không mở lại concept A/C.

Baseline `928d212` · Nhánh `research/p54-bum07-artist-workflow` · 20/11/2026 (Asia/Saigon).

**Đề xuất để chủ dự án lựa chọn:** ưu tiên xem xét **hướng B: sculpt thủ công từ Head – Generic Topology (Paul Kotelevets, CC0)**; dùng concept B/P5.2R làm chuẩn mỹ thuật và R làm thước/camera đối chứng. Hướng A là sculpt trực tiếp từ bản R. B1 chỉ nên là đối chứng về cấu trúc orbital và những lỗi đã biết, không là ngoại hình chuẩn.

Đổi base mesh không thay được công việc sculpt có phán đoán mỹ thuật. Cả hai hướng đều cần người thao tác Blender thủ công; chưa có bằng chứng Codex tự động có thể đạt chất lượng mong muốn. **Chưa chọn thay chủ dự án, chưa bắt đầu sản xuất, không tuyên bố 9/10.**

## Bộ bàn giao

- [PDF tổng hợp để xem trên iPhone](BUM07-P54-WORKFLOW-EVALUATION.pdf).
- [So sánh hai hướng, khả năng sửa R/B1 và ước lượng công việc](COMPARISON.md).
- [Năm ứng viên, nguồn, giấy phép, đối chiếu concept B](ASSETS-LICENSES.md).
- [Kế hoạch artist workflow với checkpoint riêng](ARTIST-WORKFLOW.md).
- [Tiêu chí nghiệm thu và checklist phạm vi P5.4](ACCEPTANCE.md).
- [Dữ liệu ứng viên có cấu trúc](candidates.json), [đăng ký nguồn](evidence/source-register.json), [audit R/B1/Tiby](evidence/read-only-mesh-audit.json), [audit bundle Blender](evidence/human-bundle-audit.json).

## Đã làm / chưa làm

Đã mở **chỉ đọc**, tắt autoexec, file R, B1, Tiby gốc và Human Base Meshes v1.4.1. Kiểm tra SHA trước/sau xác nhận không thay đổi các file. Tiby và bundle Blender được tải miễn phí từ nguồn chính thức vào `/tmp` để khảo sát; **không đưa binary bên thứ ba vào repo**. Dossier lưu URL/hash để kiểm tra lại. Các trang phát hành Tiby/Boy/Spring/Quaternius được đọc trực tiếp; license ghi trong hồ sơ gắn với đúng asset, không suy từ giá miễn phí.

Không tạo đầu procedural mới, sculpt thử, model thích nghi BUM, rig, animation hoặc GLB. Chưa kiểm thử deformation/runtime/iPhone, chưa mua hoặc thuê ai. Không thay game, main, Pages, Supabase, PR #2 Draft, ba nhân vật khác hoặc lịch sử. Không tạo PR/merge. Chỉ thêm hồ sơ nghiên cứu này và dừng chờ chủ dự án chọn A/B.

## Tái kiểm tra

`read-only-mesh-audit.py` và `inspect-human-bundle.py` chỉ đọc native với autoexec tắt, không có lệnh lưu/export/sculpt. Hai asset mới cần tải đúng URL/hash trong acquisition JSON và giải nén đúng đường dẫn `/tmp` ghi ở script; R/B1 đọc từ lịch sử repository. Dùng Blender4.3.2, `--disable-autoexec --python-exit-code 1`. Máy khác có thể sửa đường dẫn trong **bản sao script**, không sửa bản bàn giao.

PDF do script dựng tài liệu từ dữ liệu khảo sát; ảnh trong PDF chỉ là concept AI/Blender render lịch sử đã gắn nhãn. Không có render nhân vật P5.4 mới. Chạy `python3 scripts/build-review.py` rồi `NODE_PATH=/opt/codex/cua_node/lib/node_modules node scripts/export-pdf.cjs` từ môi trường tương ứng. `python3 scripts/verify-dossier.py` kiểm checksum/phạm vi dữ liệu; không nghiệm thu nghệ thuật.
