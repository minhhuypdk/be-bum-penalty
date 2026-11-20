# P5.3A-R Curve Bounding Box Audit

Nguyên nhân được xác định trước khi sửa model. File5dd8744 vẫn nguyên byte; chẩn đoán không ghi lại baseline.

## Kết luận

Trong fixture Blender4.3.2 của môi trường này, `evaluated.bound_box` của curve là ước lượng quá rộng theo point radius. Mỗi control point có radius1, trong khi bevel chỉ0.0016–0.012H. Transform các curve được hỏi là identity, và các vertex evaluated nằm đúng quanh mắt/tai/miệng. Không có bằng chứng các curve này thật sự kéo dài hơn2H như báo cáo P5.3A cũ.

Không sửa hình học để ép khớp bounding box sai. Audit mới tính min/max từ từng vertex của mesh evaluated nhân matrix_world. Raw bbox Blender vẫn được lưu để đối chiếu.

## Đối chiếu số đo

Width dưới đây là maxX−minX, theo scene unit danh nghĩa1H; không phải bề dày bevel. Bounds3chiều đầy đủ nằm trong JSON.

| Curve | Width báo cáo P5.3A cũ | Width vertex thật trước sửa | Width vertex thật P5.3A-R |
|---|---:|---:|---:|
| Upper_lid_margin_R | 2.202000 | 0.206893 | 0.206460 |
| Ear_helix_R | 2.091779 | 0.115818 | 0.106008 |
| Upper_lid_margin_L | 2.202000 | 0.206962 | 0.206488 |
| Ear_helix_L | 2.091779 | 0.115818 | 0.106008 |
| Closed_mouth_soft_seam | 2.340000 | 0.341942 | 0.340957 |

## Thử nghiệm kiểm soát

`confirm-curve-cause.py` chỉ tạo bản sao tạm trong bộ nhớ, không Save. Với Upper_lid_margin_R:

- Radius1, bevel0.0025: bbox evaluated nới khoảng1H quanh control bounds; actual mesh chỉ nới tương ứng bevel nhỏ.
- Radius0.1, bevel0.0025: bbox evaluated đổi sang nới0.1H, actual bevel nhỏ theo tích radius×bevel.
- Radius1, bevel0.01: bbox evaluated vẫn như case đầu, actual mesh dày hơn đúng bevel.

Các test tách ảnh hưởng point radius khỏi bevel và transform. Kết luận này giới hạn ở build/fixture được kiểm tra, không khẳng định mọi Blender/version đều như vậy.

## Thay đổi mỹ thuật khác với sửa audit

P5.3A-R giữ nguyên point radius. Control point của mí/tai/đường miệng đi theo sculpt đầu và bevel dịu hơn vì yêu cầu mỹ thuật; đó không phải cách sửa bounds. `lineage-audit.json` kiểm point radius không đổi, camera/đèn không đổi. Sau chỉnh, raw evaluated bbox có thể vẫn quá rộng; chỉ bounds từ vertex là kết quả audit hình học dùng để nghiệm thu.

Nguồn: `curve-diagnosis-before.json`, `curve-cause-controlled-test.json`, `curve-diagnosis-after.json` và script tương ứng. Không có mesh bị ẩn hoặc ép scale để vượt kiểm tra. Audit bounds PASS không phải PASS mỹ thuật, Blink hoặc khả năng rig.
