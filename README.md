# SSR: Quỹ bảo trì và Điều hành

Một web app chung cho Saigon South Residences, gồm hai mục lớn, chuyển qua lại bằng thanh **SSR · Quỹ bảo trì · Điều hành** ở đầu trang:

| Mục | Đường dẫn | Nội dung |
|---|---|---|
| Quỹ bảo trì | `index.html`, `web/` | Phân tích sổ quỹ bảo trì (mô tả bên dưới) |
| Điều hành | `web/dieu-hanh/` | Công cụ SSR Điều Hành cho Ban Quản lý, Ban Quản trị: phản ánh, bảo trì, sự cố dịch vụ, tài chính, tuân thủ, kiểm tra pháp lý |

## Mục Quỹ bảo trì

Web app phân tích Quỹ bảo trì chung cư Nam Sài Gòn Residences (Saigon South Residences): sao kê ba tài khoản từ 15/08/2024 tới 31/05/2026, đối chiếu Quy chế thu chi tài chính và Luật Nhà ở 2023, kèm bộ clip có thuyết minh.

Phân tích độc lập phục vụ giám sát của cư dân, không phải văn bản của chủ đầu tư, Ban quản trị hay đơn vị quản lý vận hành. Các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.

## Câu chữ an toàn pháp lý (17/10/2026)

Mọi câu chữ đi qua hai lớp lọc trong `src/ngon_tu.py`: lớp 1 (15/10) chuyển khẳng định sang đặt nghi vấn; lớp 2 (17/10) không suy đoán động cơ, không quy lỗi thay cơ quan có thẩm quyền, mọi chế tài gắn điều kiện "nếu cơ quan có thẩm quyền xác định là vi phạm", trang không đánh giá trách nhiệm hình sự. Lời đọc và chữ trên hình của clip đi qua `src/ngon_tu_clip.py` rồi tới hai lớp trên.

Khi không có môi trường dựng đầy đủ: `src/ap_ngon_tu_web.py` áp lớp lọc lên trang đã dựng, `src/ap_ngon_tu_files.py` áp lên file Word và Excel nhúng trong trang.

Tạm rút trong lúc chờ dựng lại bằng bộ dựng clip và báo cáo (`src/clip_an_toan.py`): Phần 1, 3, 4, 5, 6; clip dọc 1, 2, 3, 9; chương 11 bản đầy đủ; PDF báo cáo đầy đủ, tóm tắt, phân loại nguyên nhân, hỏi dần; ảnh A4 tóm tắt và phân loại. Dựng lại xong thì thêm lại vào `web/clips.json` và khối FILES.

Bản Điều hành trên web dùng dữ liệu mẫu nên thay tên thật sáu thành viên Ban Quản trị bằng "Thành viên BQT 1" tới "6"; bản offline gửi riêng Ban Quản trị giữ tên thật.

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

## Mục Điều hành

| Tệp | Nội dung |
|---|---|
| `web/dieu-hanh/index.html` | Công cụ SSR Điều Hành, một tệp, chạy được cả khi không có mạng |
| `web/dieu-hanh/tai-ve/*.xlsx` | File Excel Dashboard vận hành (có công thức) và file dữ liệu xuất từ công cụ |
| `web/dieu-hanh/tai-ve/google/` | Mã Google Sheets (Code.gs, Portal.html, Field.html) và hướng dẫn cài đặt |
| `src/ssr_switch.html` | Thanh chuyển hai mục, `build_dash3.py` tự chèn khi dựng lại trang Quỹ bảo trì |

- Bản trên GitHub Pages đang chạy **dữ liệu mẫu** (có ghi chú trên từng trang). Dữ liệu thật do Ban Quản lý nhập chỉ lưu trong trình duyệt của máy nhập, hoặc trong Google Sheets của Ban Quản lý; không bao giờ đưa lên kho này.
- Mã PIN quản trị mặc định chỉ để dùng thử, phải đổi trước khi dùng thật.
- Khóa quản trị, khóa xem Google Sheets chỉ gửi riêng, không ghi vào kho.

## Nút Hỏi đáp (cả hai mục)

| Tệp | Nội dung |
|---|---|
| `web/hoi-dap/hoidap.js` | Nút và khung hỏi đáp; tìm câu trả lời có sẵn trên trang trước, chỉ hỏi AI khi trang chưa có |
| `web/hoi-dap/kb.json` | Kho nội dung dựng từ trang Quỹ bảo trì và thư viện quy định, hướng dẫn của mục Điều hành (không lấy dữ liệu mẫu); dựng bằng `node src/hoidap/build_kb.js` |
| `web/hoi-dap/config.js` | Địa chỉ máy chủ hỏi AI; để trống thì chỉ trả lời từ nội dung trang |
| `web/hoi-dap/may-chu/HoiDap.gs` | Máy chủ Google Apps Script gọi Gemini miễn phí, giữ khóa API, giới hạn lượt mỗi ngày |
| `web/hoi-dap/tai-lieu/` | Toàn văn quy chế, nội quy (tệp .txt) muốn đưa thêm vào kho |

Hướng dẫn bật phần AI: `web/hoi-dap/HUONG-DAN-HOI-DAP.md`. Khi sửa nội dung trang Quỹ bảo trì, chạy lại `build_kb.js` để kho hỏi đáp khớp nội dung mới.

## Ghi chú

- Trang chạy trên GitHub Pages: https://jukytwo.github.io/ssr-so-quy-bao-tri/ (tệp `index.html` ở gốc kho chuyển thẳng tới `web/`). Trên GitHub Pages trang ở chế độ chỉ xem: không sửa tình trạng mười câu hỏi, không có hỏi đáp bằng AI; muốn cập nhật thì dựng lại và tải lên tệp `web/index.html` mới.
- `web/v/` là 34 clip 720p cho tab Clip (khoảng 176 MB); bản gốc 1080p ở thư mục chia sẻ, mục 1.5 Clip.
- Phông chữ (Be Vietnam Pro, Cormorant Garamond, giấy phép OFL) không đưa vào kho; tải từ Google Fonts nếu cần dựng lại ảnh, clip.
- Mã dựng dùng đường dẫn tuyệt đối của môi trường dựng (`/home/claude/...`); đổi lại cho máy mới trước khi chạy.
- Kho chứa số tài khoản ngân hàng, tên nhà thầu và giao dịch của quỹ: giữ ở chế độ riêng tư (private).
