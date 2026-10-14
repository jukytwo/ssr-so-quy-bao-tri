# Sổ quỹ bảo trì SSR

Web app phân tích Quỹ bảo trì chung cư Nam Sài Gòn Residences (Saigon South Residences): sao kê ba tài khoản từ 15/08/2024 tới 31/05/2026, đối chiếu Quy chế thu chi tài chính và Luật Nhà ở 2023, kèm bộ clip có thuyết minh.

Phân tích độc lập phục vụ giám sát của cư dân, không phải văn bản của chủ đầu tư, Ban quản trị hay đơn vị quản lý vận hành. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `web/index.html` | Trang web app, bản trực tuyến. Tệp PDF tải về nằm riêng trong `web/f/`, ảnh poster clip trong `web/p/`. |
| `web/so_quy_bao_tri_offline.html` | Bản offline một tệp, nhúng sẵn mọi tài liệu tải về; mở thẳng bằng trình duyệt. |
| `web/clips.json` | Danh mục bộ clip, thời lượng, lời thuyết minh theo thời gian, mã QR. |
| `src/` | Mã dựng trang: `build_dash3.py` ghép `src/d3/` (giao diện, CSS, JavaScript) với dữ liệu JSON. |
| `src/luudo2.py` | Dữ liệu tab Đường đi của tiền: năm trường hợp, từng chặng Lẽ ra và Thực tế, kết luận. |
| `src/video25/` | Bộ dựng clip, nén clip cho web, ảnh chủ đề, mốc thời gian lời thuyết minh từng clip. |
| `src/qr/` | Ảnh mã QR in dán bảng tin và chiếu Hội nghị. |

## Các tab trên điện thoại

Tổng quan (câu trả lời ngắn và năm vấn đề), Clip, Đường tiền, 10 câu hỏi, Mục lục (báo cáo đầy đủ bảy phần).

## Ghi chú

- Tệp clip (`web/v/*.mp4`, khoảng 176 MB) không đưa vào kho; bản gốc 1080p ở thư mục chia sẻ, mục 1.5 Clip. Muốn chạy đủ tab Clip khi tự lưu trữ trang, chép 34 tệp clip 720p vào `web/v/`.
- Phông chữ (Be Vietnam Pro, Cormorant Garamond, giấy phép OFL) không đưa vào kho; tải từ Google Fonts nếu cần dựng lại ảnh, clip.
- Mã dựng dùng đường dẫn tuyệt đối của môi trường dựng (`/home/claude/...`); đổi lại cho máy mới trước khi chạy.
- Kho chứa số tài khoản ngân hàng, tên nhà thầu và giao dịch của quỹ: giữ ở chế độ riêng tư (private).
