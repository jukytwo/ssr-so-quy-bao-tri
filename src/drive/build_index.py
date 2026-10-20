# -*- coding: utf-8 -*-
"""Muc luc thu muc Google Drive chia se (ban cong khai). Nhan dien SSR, khong nhan dien TVN, khong neu ten ca nhan."""
import base64, os, sys
sys.path.insert(0, "/home/claude/ssr")
os.chdir("/home/claude/ssr")
from report_kit import CSS, E, nd, table

TODAY = "04/10/2026"
LOGO = base64.b64encode(open("crops/logo_192.png", "rb").read()).decode()
DASH = "https://jukytwo.github.io/ssr-so-quy-bao-tri/"
DIEUHANH = "https://jukytwo.github.io/ssr-so-quy-bao-tri/web/dieu-hanh/"

USE = ["Bấm vào file để xem ngay trên Google Drive; muốn lưu về máy thì chọn Tải xuống.",
       "File .html là trang tương tác: tải về rồi mở bằng Chrome, Edge hoặc Safari (Drive không xem trước được).",
       "Đường dẫn thư mục: https://drive.google.com/drive/folders/1gb8brZ_Bxhc0Jm7wYimdKmsWBnyzQEH8"]

S1 = [("1.1 Báo cáo phân tích", "Bản đầy đủ 60 trang, bản tóm tắt 25 trang (PDF)", "Năm câu hỏi kết luận, phân loại nguyên nhân, 16 dấu hiệu kèm hệ quả pháp lý."),
      ("1.2 Công văn gửi Ban quản trị", "Công văn kiến nghị, Word và PDF; ảnh đề nghị hợp tác", "Đề nghị cung cấp 15 hồ sơ, giải trình, khắc phục; kèm danh sách ký tên."),
      ("1.3 Dữ liệu Excel", "Sao kê tổng hợp và phân tích", "8 sao kê, 32 phép kiểm tra, Năm câu hỏi, ngưỡng từng hợp đồng, theo dõi hồ sơ."),
      ("1.4 Ảnh cho cư dân", "3 ảnh trọng tâm, ảnh Phân loại, Mười câu hỏi", "Ảnh khổ A4 để đăng nhóm; bản PDF để in dán bảng tin; bản Word để chỉnh sửa."),
      ("1.5 Clip", "Bộ clip theo chủ đề: 1 bản đầy đủ 22 phút 33 giây, 6 phần ngang, 11 clip dọc; 2 clip 11 phút trước đó", "Bản đầy đủ có mốc chương; 6 phần để chiếu từng đoạn tại Hội nghị; 11 clip dọc, mỗi clip một chủ đề, gửi lẻ được; ảnh danh mục kèm thời lượng."),
      ("1.6 Sổ quỹ bảo trì", "Bản offline, HTML", "Năm câu hỏi, toàn bộ phân tích, hỏi đáp, tải file."),
      ("1.7 Hướng dẫn phối hợp", "Quy trình 7 bước, tin mẫu, Hỏi dần, Phân loại", "Thứ tự gửi tài liệu, mẫu tin từng bước, cách ghi nhận và phân loại câu trả lời."),
      ("1.8 Tài liệu gốc", "Sao kê, hồ sơ Ban quản trị, Bộ quy chế 26/05/2024", "Bản gốc để đối chiếu từng con số trong báo cáo."),
      ("1.9 Trình bày Hội nghị", "Slide Hội nghị 11 trang; lời nói kèm", "Bộ slide trình chiếu tại Hội nghị và ghi chú cho người trình bày theo từng slide.")]
S2 = [("2.1 Giới thiệu công cụ", "Trang giới thiệu, 5 ảnh 4:5", "Tính năng cho Ban quản trị, Ban quản lý, cư dân."),
      ("2.2 Công cụ bản offline", "3 công cụ, bản HTML", "SSR Điều Hành (trung tâm quản trị); Quản lý vận hành và tài chính; Theo dõi phản ánh và vận hành.")]

EXTRA = """
.hd { display:flex; justify-content:space-between; align-items:center; border-bottom:2pt solid #1F3864; padding-bottom:6pt; }
.hd .br { display:flex; gap:10pt; align-items:center; } .hd img { width:15mm; height:15mm; border-radius:50%; }
.hd .l1 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:800; letter-spacing:.12em; color:#1F3864; }
.hd .l2 { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:600; color:#5a6475; }
.hd .dt { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:700; color:#fff; background:#1F3864; border-radius:10pt; padding:2.5pt 9pt; }
.t1 { font-family:'Be Vietnam Pro',sans-serif; font-size:19pt; font-weight:800; color:#1F3864; line-height:1.18; margin-top:6pt; }
.t2 { font-family:'Be Vietnam Pro',sans-serif; font-size:10pt; color:#3d4656; margin-top:4pt; line-height:1.45; }
.sh { font-family:'Be Vietnam Pro',sans-serif; display:flex; align-items:center; gap:8pt; background:#DCE6F1; border-radius:4pt; padding:4pt 9pt; margin:7pt 0 4pt 0; break-after:avoid; }
.sh .no { font-size:13pt; font-weight:800; color:#C8992F; } .sh h2 { font-size:12pt; font-weight:800; color:#1F3864; }
table.ix td { font-size:8.5pt; line-height:1.32; vertical-align:top; padding-top:1.6pt; padding-bottom:1.6pt; } table.tn td:nth-child(2) { font-weight:700; color:#1F3864; } table.ix td:first-child { font-family:'Be Vietnam Pro',sans-serif; font-weight:700; color:#1F3864; }
.own { font-family:'Be Vietnam Pro',sans-serif; font-size:9.4pt; color:#3d4656; margin-top:2pt; } .own b { color:#1F3864; }
.lk { font-family:'Be Vietnam Pro',sans-serif; font-size:8.8pt; margin:6pt 0 0 0; line-height:1.5; }
.lk a { color:#1F3864; font-weight:700; }
.ft { font-family:'Be Vietnam Pro',sans-serif; word-spacing:.14em; font-size:7.8pt; color:#5b6474; line-height:1.45; border-top:0.8pt solid #cfd8e6; padding-top:5pt; margin-top:6pt; }
"""

def sh(no, t): return f'<div class="sh"><span class="no">{no}</span><h2>{E(t)}</h2></div>'
rows = lambda R: [[E(a), E(b), E(c)] for a, b, c in R]
head = (f'<div class="hd"><div class="br"><img alt="Logo Saigon South Residences" src="data:image/png;base64,{LOGO}"><div>'
        '<div class="l1">TÀI LIỆU CHIA SẺ · CHUNG CƯ NAM SÀI GÒN RESIDENCES</div><div class="l2">Saigon South Residences, Phú Mỹ Hưng</div></div></div>'
        f'<span class="dt">Cập nhật {TODAY}</span></div>'
        '<div class="t1">Mục lục thư mục tài liệu</div>'
        '<div class="t2">Hai nhóm tài liệu tách riêng: phân tích sao kê quỹ bảo trì và bộ công cụ quản lý vận hành.</div>'
        '<div class="own">Chủ sở hữu thư mục: <b>Nguyên Vũ</b> · jukytwo@gmail.com</div>')
TN = [("1", "1 - Năm vấn đề (5 phút)", "Năm vấn đề, số tiền và tình trạng từng vấn đề; điều đã kiểm tra được; ba phương án Hội nghị quyết định."),
      ("2", "2 - Lưu đồ dòng tiền (10 phút)", "Năm trường hợp thiếu minh bạch: tiền đi đường nào, hở ở khâu nào, trái điều nào, cần chứng từ gì."),
      ("3", "3 - Bản tóm tắt (25 trang)", "Đủ 16 dấu hiệu, 13 khoản chi trên 50 triệu, nguyên nhân, hệ quả pháp lý, câu hỏi đã gửi Ban quản trị.")]
KT = [("Chứng cứ từng giao dịch, bảng đối chiếu từng điều Quy chế", "Báo cáo đầy đủ (60 trang)", "1.1 Báo cáo phân tích"),
      ("Tự kiểm tra từng con số, 198 giao dịch", "Sao kê tổng hợp và phân tích (Excel)", "1.3 Dữ liệu Excel"),
      ("Bản gốc sao kê, Quy chế, hồ sơ Ban quản trị", "Các file gốc", "1.8 Tài liệu gốc"),
      ("Xem thay vì đọc", "Bộ clip theo chủ đề: bản đầy đủ, 6 phần ngang, 11 clip dọc", "1.5 Clip")]
S0 = [("0. Cư dân đọc trước - 3 file", "Năm vấn đề; lưu đồ dòng tiền; bản tóm tắt", "Đọc theo thứ tự 1, 2, 3 là nắm đủ mọi vấn đề; mặt sau file 1 là phiếu ý kiến dùng tại Hội nghị.")]
body = (head + sh("", "Cư dân chỉ cần đọc 3 file, theo thứ tự, trong thư mục 0")
        + table(["", "File", "Đọc xong sẽ biết"], rows(TN), widths=["5%", "30%", "65%"], esc=False, tcls="ix tn")
        + '<p class="lk">Ba file nêu đủ mọi vấn đề đã phát hiện, kể cả phần chưa kết luận được. Bản đầy đủ không có dấu hiệu nào ngoài 16 dấu hiệu trong bản tóm tắt; nó chỉ thêm chứng cứ chi tiết.</p>'
        + sh("", "Muốn kiểm tra tới tận gốc")
        + table(["Bạn cần", "Mở file", "Nằm trong thư mục"], rows(KT), widths=["36%", "37%", "27%"], esc=False, tcls="ix tn")
        + nd(USE, label="CÁCH DÙNG THƯ MỤC NÀY", gold=True)
        + sh("0", "Cư dân đọc trước: 3 file")
        + table(["Thư mục", "File", "Nội dung"], rows(S0), widths=["23%", "29%", "48%"], esc=False, tcls="ix")
        + sh("1", "Sao kê tài chính SSR: phân tích quỹ bảo trì")
        + table(["Thư mục", "File", "Nội dung"], rows(S1), widths=["23%", "29%", "48%"], esc=False, tcls="ix")
        + f'<p class="lk">Xem online, luôn là bản mới nhất: <a href="{DASH}">Sổ quỹ bảo trì SSR</a> ({DASH}).</p>'
        + sh("2", "SSR - Công cụ BQT: quản lý vận hành")
        + table(["Thư mục", "File", "Nội dung"], rows(S2), widths=["23%", "29%", "48%"], esc=False, tcls="ix")
        + nd(["Bản offline lưu dữ liệu ngay trên máy đang mở; dữ liệu mẫu có nút xóa khi dùng thật.",
              f"Bản online của SSR Điều hành, luôn là bản mới nhất: {DIEUHANH}"], label="LƯU Ý VỀ CÔNG CỤ")
        + '<div class="ft">Phần sao kê là phân tích độc lập của cư dân, không phải văn bản của chủ đầu tư hay Ban quản trị; các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.</div>')
fonts = open("bvp_fonts.css").read()
doc = f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{fonts}{CSS}{EXTRA}@page{{size:A4;margin:14mm 18mm 12mm 18mm}}</style></head><body>{body}</body></html>'
import ngon_tu as _NT; doc = _NT.soften(doc)
open("drive/muc_luc.html", "w", encoding="utf-8").write(doc)
print("ok", len(doc))
