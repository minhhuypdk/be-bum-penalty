# Kết quả kiểm chứng P3.1R

Blink100: **PASS**. Tổng thể Facial Structure Repair: **chưa đạt** vì còn nếp gấp và self-contact chưa xử lý. Không phải duyệt9/10.

Đọc lại:122 mesh gốc và rig/action giữ nguyên. Source candidate SHA-256: `337410b56547447227a8fd9d93a50e117254f2ad504f3be3b6f98d800551db95`.

## Va chạm và deformation

| Blink | Tam giác da xuyên envelope hai mắt | Khoảng cách min | Self-overlap candidates |
| --- | ---: | ---: | ---: |
| 0% | 0 | 0.093673 | 180 |
| 12.5% | 0 | 0.093673 | 185 |
| 25.0% | 0 | 0.093673 | 183 |
| 37.5% | 0 | 0.093673 | 187 |
| 50.0% | 0 | 0.093673 | 187 |
| 62.5% | 0 | 0.093673 | 191 |
| 75.0% | 0 | 0.093673 | 193 |
| 87.5% | 0 | 0.093673 | 203 |
| 100% | 0 | 0.093673 | 1590 |

Envelope radius0.090; distances scene units. Self-overlap là candidates chưa phân loại, không tự coi là contact hợp lệ. Finite/no-zero-area triangles không bảo đảm tạo hình tự nhiên.

## GLB full-blink ID gate

| Engine | Variant | Góc | Pixel mắt đỏ |
| --- | --- | ---: | ---: |
| chromium | P3.1 | 0 | 5751 |
| chromium | P3.1 | 45 | 3460 |
| chromium | P3.1R | 0 | 0 |
| chromium | P3.1R | 45 | 0 |
| webkit | P3.1 | 0 | 5634 |
| webkit | P3.1 | 45 | 3388 |
| webkit | P3.1R | 0 | 0 |
| webkit | P3.1R | 45 | 0 |

P3.1 là negative control phải lộ mắt; R yêu cầu0 pixel. Camera/studio khớp; ảnh ID unlit tách riêng beauty.

## Ngân sách

| Engine | Variant | Góc | Draw calls thực đo | Rendered triangles |
| --- | --- | ---: | ---: | ---: |
| chromium | P3.1 | 0 | 41 | 214596 |
| chromium | P3.1R | 0 | 29 | 195184 |
| chromium | P3.1 | 45 | 42 | 214598 |
| chromium | P3.1R | 45 | 30 | 195186 |
| chromium | P3.1 | 90 | 43 | 214694 |
| chromium | P3.1R | 90 | 31 | 195282 |
| webkit | P3.1 | 0 | 41 | 214596 |
| webkit | P3.1R | 0 | 29 | 195184 |
| webkit | P3.1 | 45 | 42 | 214598 |
| webkit | P3.1R | 45 | 30 | 195186 |
| webkit | P3.1 | 90 | 43 | 214694 |
| webkit | P3.1R | 90 | 31 | 195282 |

Tổng asset P3.1:225446 triangles/71 primitives; P3.1R:206034/59. Không đồng nhất primitives với measured draw calls. GLB R có corrective data lớn hơn; không suy ra FPS iPhone. Xem BUDGET.json cho bytes.

Smile0/50/100 và Blink đủ năm mức có ảnh0°/45°. Shader/decoder và finite geometry đạt kiểm tra hẹp; các nếp gấp, mouth contacts và tóc dạng cap vẫn cần xử lý/nghiệm thu. Không chuyển P3.2.
