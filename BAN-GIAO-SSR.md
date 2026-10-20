# Bàn giao toàn bộ SSR sang tài khoản guest@tvnpartners.com.vn

Ngày 20/10/2026, anh Nguyên Vũ chuyển toàn bộ nội dung và hoạt động của Saigon South Residences (SSR) từ tài khoản Claude "Vũ max" sang tài khoản **guest@tvnpartners.com.vn**. Từ ngày này Vũ max không làm việc SSR nữa, chỉ giữ bản dự phòng. Tài liệu này để tài khoản guest nắm đủ bối cảnh, làm tiếp không phải hỏi lại.

Tài liệu công khai này không chứa khóa, mật khẩu, tên thật thành viên Ban Quản trị hay dữ liệu cư dân. Phần nội bộ nằm trong gói riêng anh Vũ gửi trực tiếp (xem mục 6).

## 1. Hai mảng việc

| Mảng | Anh Vũ gọi là | Nội dung |
|---|---|---|
| Quỹ bảo trì | "Sao kê tài chính SSR" | Phân tích độc lập sao kê ba tài khoản quỹ bảo trì từ 15/08/2024 tới 31/05/2026, đối chiếu Quy chế thu chi và Luật Nhà ở 2023. Gồm 10 câu hỏi gửi Ban quản trị, bộ clip, PDF, Excel và công văn kiến nghị. |
| Điều hành | "SSR - công cụ BQT" | Công cụ SSR Điều Hành cho Ban Quản lý, Ban Quản trị: phản ánh cư dân, vận hành và bảo trì, sự cố dịch vụ, tài chính, tuân thủ, kiểm tra pháp lý. Bản offline một tệp, bản Excel có công thức, máy chủ Google Sheets. |

Hai mảng chạy chung **một web app**, chuyển qua lại bằng thanh "SSR · Quỹ bảo trì · Điều hành" ở đầu trang:
- Quỹ bảo trì: https://jukytwo.github.io/ssr-so-quy-bao-tri/
- Điều hành: https://jukytwo.github.io/ssr-so-quy-bao-tri/web/dieu-hanh/
- Nút **Hỏi đáp** nằm trên cả hai mục.

## 2. Tài sản và nơi lưu

| Tài sản | Nơi lưu | Ghi chú |
|---|---|---|
| Kho mã và trang | GitHub `jukytwo/ssr-so-quy-bao-tri` (công khai, GitHub Pages nhánh `main`) | Cấu trúc ở `README.md`. Anh Vũ cũng đẩy bằng GitHub Desktop, bản sao tại máy: OneDrive\Documents\GitHub\ssr-so-quy-bao-tri. Luôn `git fetch` trước khi đẩy. |
| Máy chủ Hỏi đáp | Google Apps Script "SSR - Hỏi đáp" trên Drive jukytwo@gmail.com, Script ID `1bIO3QkebBIVQ6z7HDmedRb33YPhehZJSFCu2TMwnaN0M3RQXtOIosNDY` | Mã nguồn: `web/hoi-dap/may-chu/HoiDap.gs`. Địa chỉ `/exec` nằm trong `web/hoi-dap/config.js`. |
| Khóa Gemini | Script Properties của dự án Apps Script: `GEMINI_API_KEY` | Thuộc dự án Gemini "SSR - Quy bao tri va van hanh" (gen-lang-client-0175987888), gói free. Khóa không bao giờ nằm trong kho, trang hay tin nhắn. Có thể thêm `DAILY_LIMIT` (mặc định 300 câu AI mỗi ngày) và `GEMINI_MODEL` (danh sách mô hình, cách nhau dấu phẩy). |
| Giọng đọc clip | Gemini TTS, giọng **Achernar**, cũng dự án "SSR - Quy bao tri va van hanh" | Ưu tiên gói free; chỉ khi hết hạn mức free mới dùng gói trả phí. Không đổi giọng. |
| Máy chủ Google Sheets cho Điều hành | `web/dieu-hanh/tai-ve/google/` (Code.gs, Portal.html, Field.html, HUONG-DAN-GOOGLE-SHEETS.md) | Bảng tính chứa dữ liệu cư dân: chỉ chia sẻ cho Ban Quản lý, Ban Quản trị, không bao giờ để "ai có link". |
| Excel | `web/dieu-hanh/tai-ve/*.xlsx`; Excel sao kê nhúng trong trang Quỹ | Mọi số đều có công thức, không nhập số cứng. |
| Clip Quỹ bảo trì | `web/v/` (34 clip 720p), danh mục `web/clips.json`; bản 1080p trong thư mục chia sẻ SSR trên Drive (mục 1.5 Clip) | Đã dựng lại ngày 17/10 với câu chữ an toàn pháp lý. |
| Trang trên claude.ai (thuộc Vũ max) | SSR Điều Hành https://claude.ai/artifact/A8XH73Bt3A31EgZxA7MhYp · Sổ quỹ bảo trì SSR https://claude.ai/artifact/5ZrS77qvrnpcY3R3bXqGGe · SSR Hội nghị: Quỹ bảo trì https://claude.ai/artifact/4L8FayGNKheeDgin1pkEvj · Quản lý vận hành và tài chính https://claude.ai/artifact/KEGhfULFytZNCKTVUbWz8P · Phản ánh và vận hành https://claude.ai/artifact/XqnQ4C3VYYojBfGx47bDvG · Giới thiệu công cụ quản lý https://claude.ai/artifact/RQLCFusCTPh8md4KFxvtZ4 · Cách làm clip minh bạch quỹ bảo trì https://claude.ai/artifact/5aPPjB3j7RxotmVAxFRVN9 | Anh Vũ chia sẻ cho tài khoản guest bằng nút Share của từng trang. Muốn guest tự sửa thì guest đăng lại bản của mình; link mới phải báo lại cho cư dân. Trang dùng chính cho cư dân là GitHub Pages, không phải các trang này. |
| Thư mục chia sẻ SSR | Google Drive jukytwo@gmail.com, chia theo chủ đề | Anh Vũ cho mọi người có link đọc, tải. Tài khoản guest kết nối Drive bằng jukytwo@gmail.com nên đọc thẳng được. |

## 3. Nguyên tắc bắt buộc

**Nhận diện**
- SSR dùng nhận diện riêng: logo Phú Mỹ Hưng – Saigon South Residences, tông xanh lục đậm và vàng kim. Tuyệt đối không đặt logo, khẩu hiệu hay khối liên hệ TVN.

**Câu chữ an toàn pháp lý**
- Viết dạng câu hỏi, đề nghị làm rõ bằng hồ sơ, chứng từ, nghiệm thu, hậu kiểm. Không khẳng định.
- Không bao giờ viết "tiền chưa mất", "tiền không mất": trả đúng hợp đồng mà nhận thiếu hàng vẫn là thiệt hại cho cư dân.
- Không suy đoán động cơ, không phân loại "cố ý", "có chủ đích". Không quy lỗi thay cơ quan có thẩm quyền.
- Mọi chế tài (phạt, đề nghị hoàn trả về quỹ, bãi nhiệm) đều kèm điều kiện "nếu cơ quan có thẩm quyền xác định là vi phạm". Việc xem xét trách nhiệm thuộc Hội nghị nhà chung cư. Trang không đánh giá trách nhiệm hình sự.
- Dùng từ chuyên nghiệp, trang trọng. Không dùng từ nhấn mạnh hay hàm ý như "do chính", "vòng qua", "chắc chắn".
- Ba lớp lọc tự động nằm trong `src/ngon_tu.py` (R, R2, R3, danh sách cấm `CAM`); lời đọc clip đi qua `src/ngon_tu_clip.py`. Mọi nội dung mới phải đi qua hai tệp này.

**Miễn trừ trách nhiệm**
- Đoạn miễn trừ trách nhiệm nguyên văn của anh Vũ nằm ở cuối mọi trang, chèn qua `src/ssr_switch.html`. Không sửa câu chữ đoạn này.

**Nêu tên và số liệu**
- Đối tác đã biết tên (nhà thầu, nhà cung cấp, đơn vị quảng cáo, ngân hàng) thì nêu đích danh.
- Không nêu tên cá nhân thành viên Ban Quản trị trên bản công khai.
- Mọi số phải truy được về sao kê gốc.

**Câu móc và xác minh**
- Mọi trang, báo cáo, clip mở bằng câu móc: phát hiện mạnh nhất có số, đặt dưới tiêu đề hoặc ở 5–10 giây đầu clip. Không giật tít.
- Theo Bộ nguyên tắc xác minh thông tin của anh Vũ: không bịa số, nguồn, trích dẫn; không suy nhân quả từ tương quan; thiếu căn cứ thì nói rõ chưa đủ dữ liệu.
- Hỏi đáp AI đã cài sẵn các nguyên tắc này trong `HD_SYS` của `HoiDap.gs`.

**Dữ liệu và bảo mật**
- Dữ liệu cư dân thật, khóa quản trị, PIN, mật khẩu Excel chỉ gửi riêng. Không đưa vào kho công khai, không gửi cho AI miễn phí.
- PIN mặc định của Điều hành chỉ để dùng thử, phải đổi trước khi dùng thật.

**Cách làm việc với anh Vũ**
- Viết tiếng Việt, ngắn gọn, giọng người Việt, không dấu vết AI.
- Tự quyết theo phương án hợp lý cho việc anh đã giao, làm xong báo kết quả. Anh chỉ hỏi so sánh, xem xét thì trả lời đúng câu hỏi, không tự làm thêm.
- Trang Quỹ bảo trì phải dễ xem trên điện thoại. Anh thích tab Clip nhất: mọi màn hình nên có trọng tâm rõ như tab đó.

## 4. Cách cập nhật

**Trang Quỹ bảo trì**
- Mã dựng `src/build_dash3.py` ghép `src/d3/` với dữ liệu JSON. Mã dựng trang, clip (`src/video_ssr_25.py`) và PDF dùng đường dẫn tuyệt đối của môi trường dựng cũ: `/home/claude/ssr`, `/home/claude/vtpl`, `/home/claude/gv`, `/home/claude/vshim`. Các thư mục này không có trong kho; chúng nằm trong gói `ssr_ma_nguon.tar.gz` (kèm bộ đệm giọng đọc `ssr_bo_dem_giong_doc.tar.gz`) ở thư mục `SSR - Sao kê\Bàn giao cho guest - 20.10.2026` trên máy anh Vũ. Cách bung và quy trình dựng ở `BAN-GIAO-SSR-cho-guest.md` cùng thư mục.
- Khi chưa có môi trường dựng, sửa thẳng trang đã dựng:
  - `src/ap_ngon_tu_web.py` áp lớp lọc câu chữ lên `index.html` và `web/index.html`.
  - `src/ap_ngon_tu_files.py` áp lên Word, Excel nhúng.
  - `src/clip_an_toan.py` gỡ, thêm clip và tệp tải về.
- Sửa nội dung trang thì chạy lại `node src/hoidap/build_kb.js` để kho Hỏi đáp (`web/hoi-dap/kb.json`) khớp nội dung mới.
- `index.html` ở gốc kho là bản sao của `web/index.html`, hai tệp phải giống nhau.

**Trang Điều hành**
- `web/dieu-hanh/index.html` là bản chuẩn.
- Phiên ngày 17/10 đã sửa thẳng trên bản này: bỏ toàn bộ dữ liệu mẫu (hàm `realOnly`). Khi chưa có số liệu thật thì không chấm điểm, không báo động (`hasData`), chỉ hiện "Chưa có số liệu vận hành được công bố". Bản công khai ghi "Thành viên BQT 1" tới "6".
- Bộ dựng cũ (orig.html, hook.js, inject.py, build_web.sh) nằm trong gói nội bộ. Bộ dựng này chưa có ba thay đổi trên. Nếu dùng lại thì phải đưa ba thay đổi vào trước khi dựng, không thì lần dựng sau sẽ đè mất.

**Máy chủ Hỏi đáp**
1. Sửa `web/hoi-dap/may-chu/HoiDap.gs` trong kho.
2. Dán toàn bộ vào Code.gs của dự án Apps Script "SSR - Hỏi đáp".
3. Vào Deploy, chọn Manage deployments, sửa bản đang chạy, chọn New version. Địa chỉ `/exec` giữ nguyên.
4. Chạy thử hàm `kiemTraHoiDap` để kiểm tra.

Lưu ý khi sửa:
- Gói free của Gemini không cho tra Google (lỗi 429). Máy chủ tự bỏ phần tra Google và nhớ trong 6 giờ.
- Mô hình đang dùng theo thứ tự: gemini-3.8-flash, 3.5-flash, flash-latest, 3.1-flash-lite.

## 5. Tình trạng ngày 20/10/2026 và việc còn dở

**Đã xong**
- Miễn trừ trách nhiệm.
- Ba lớp lọc câu chữ an toàn pháp lý.
- 4 PDF (báo cáo đầy đủ, tóm tắt, phân loại nguyên nhân, hỏi dần), ảnh A4 và Excel đã xuất lại.
- 34 clip đã dựng lại (bản đầy đủ 16 chương, 6 phần ngang, 11 clip dọc, tóm tắt).
- Điều hành chỉ hiện số liệu thật.
- Hỏi đáp AI đang chạy.

**Việc còn dở**
1. **Clip 11 phút "toàn bộ vấn đề"**: đã dựng lại xong ngày 20/10 (ngang 11 phút 25 giây và dọc), đã thay ở mọi thư mục trên máy anh Vũ. Trang web không dùng clip này.
2. **Môi trường dựng:** đã đóng gói xong (xem mục 4). Tài khoản guest bung gói vào `/home/claude` là dựng lại được trang, clip, PDF từ nguồn.
3. **Toàn văn Quy chế:** đã xong ngày 20/10/2026. Năm văn bản của bộ đã thông qua tại Hội nghị nhà chung cư ngày 26/05/2024 (Quy chế bầu Ban Quản trị, Quy chế họp Hội nghị nhà chung cư, Quy chế thu chi tài chính, Quy chế hoạt động Ban Quản trị, Nội quy) nằm ở `web/hoi-dap/tai-lieu/*.txt`, chuyển chữ từ bản chụp gốc `1.8 Tài liệu gốc/Quy chế đã thông qua` nên khi trích dẫn cần đối chiếu bản gốc. `kb.json` đã dựng lại (thêm 144 mục).
4. **Lịch sử git:** kho công khai còn giữ clip, PDF cũ và tên thật Ban Quản trị ở bản Điều hành trước. Muốn xóa hẳn phải viết lại lịch sử kho. Việc này không đảo ngược được, chỉ làm khi anh Vũ quyết.
5. **Khóa Gemini lộ:** khóa Gemini đầu tiên anh Vũ dán trong chat ngày 17/10 đã lộ. Nên xóa trong AI Studio nếu chưa xóa.
6. **Theo dõi 10 câu hỏi:** cập nhật tình trạng trả lời của Ban quản trị khi có. Hạn trả lời công văn là 15 ngày.

## 6. Gói nội bộ (anh Vũ gửi trực tiếp, không đưa lên kho)

- `SSR_ban_giao_noi_bo.zip`:
  - Bản offline Điều hành có tên thật Ban Quản trị.
  - Bộ dựng Điều hành.
  - Công cụ "Quản lý vận hành và tài chính" bản cũ, kèm Excel mẫu và máy chủ Google Sheets.
  - Hồ sơ giới thiệu công cụ.
- `NHAP_BO_NHO_SSR.md`: dán vào một chat mới của tài khoản guest (đã bật Memory) và nhờ "nhập vào bộ nhớ".
