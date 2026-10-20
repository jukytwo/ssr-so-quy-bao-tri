// Huong dan gui tai lieu va tin nhan mau cho nhom cu dan - SSR (Word)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, BorderStyle,
  ShadingType, PageNumber, Footer, VerticalAlign, ImageRun, LevelFormat,
} = require("docx");

const FONT = "Times New Roman";
const SZ = 24;                 // 12pt
const W = 9638;                // A4 210mm - 2 x 20mm = 170mm
const NAVY = "1F3864", GOLD = "C8992F", GREY = "DCE6F1", SOFT = "EDF1F7", CREAM = "FBF3DF", LINEC = "BFC8D6";
const LINK = "https://jukytwo.github.io/ssr-so-quy-bao-tri/";
const B = {style: BorderStyle.SINGLE, size: 4, color: LINEC};
const BOX = {top: B, bottom: B, left: B, right: B};
const NONE = {style: BorderStyle.NONE, size: 0, color: "FFFFFF"};

function run(t, o = {}) {
  return new TextRun({text: t, font: FONT, size: o.size || SZ, bold: !!o.b, italics: !!o.i, color: o.c});
}
function runs(parts, o = {}) { return (Array.isArray(parts) ? parts : [parts]).map(p => typeof p === "string" ? run(p, o) : run(p.t, Object.assign({}, o, p))); }
function P(parts, o = {}) {
  return new Paragraph({children: runs(parts, o), alignment: o.al || AlignmentType.LEFT,
    spacing: {before: o.before || 0, after: o.after != null ? o.after : 100, line: o.line || 276},
    keepNext: !!o.keepNext, keepLines: !!o.keepLines, numbering: o.bullet ? {reference: "dot", level: 0} : undefined,
    border: o.border});
}
function H1(t) {
  return new Paragraph({children: [run(t, {b: true, size: 28, c: NAVY})], spacing: {before: 280, after: 120}, keepNext: true,
    shading: {type: ShadingType.CLEAR, color: "auto", fill: GREY}, border: {left: {style: BorderStyle.SINGLE, size: 24, color: GOLD, space: 6}}});
}
function H2(t, note) {
  return new Paragraph({children: [run(t, {b: true, size: 25, c: NAVY})].concat(note ? [run("  " + note, {i: true, size: 21, c: "5B6474"})] : []),
    spacing: {before: 220, after: 80}, keepNext: true});
}
function cell(content, w, o = {}) {
  const paras = (Array.isArray(content) && content.length && (typeof content[0] !== "object" || content[0].t === undefined) ? content : [content])
    .map(c => c instanceof Paragraph ? c : P(c, {size: o.size || 22, b: o.b, i: o.i, c: o.c, after: o.after != null ? o.after : 40, line: 264, al: o.al}));
  return new TableCell({children: paras, width: {size: w, type: WidthType.DXA}, verticalAlign: o.va || VerticalAlign.TOP,
    shading: o.fill ? {type: ShadingType.CLEAR, color: "auto", fill: o.fill} : undefined,
    margins: {top: 70, bottom: 70, left: 110, right: 110}, borders: o.borders || BOX, columnSpan: o.span});
}
function table(head, rows, widths, o = {}) {
  const hdr = new TableRow({tableHeader: true, cantSplit: true, children: head.map((h, i) => cell(h, widths[i], {b: true, fill: NAVY, c: "FFFFFF", size: 21}))});
  const body = rows.map((r, ri) => new TableRow({cantSplit: true, children: r.map((c, i) => cell(c, widths[i], {fill: (o.band && ri % 2) ? "F5F7FA" : (o.first && i === 0 ? SOFT : undefined), b: o.first && i === 0 && !o.firstPlain, size: (o.firstSize && i === 0) ? o.firstSize : undefined}))}));
  return new Table({width: {size: W, type: WidthType.DXA}, columnWidths: widths, rows: [hdr].concat(body)});
}
// khung tin nhan mau: mot o nen nhat, moi doan mot dong
function msg(lines) {
  const paras = lines.map((l, i) => P(l, {size: 23, after: l === "" ? 0 : 90, line: 280}));
  return new Table({width: {size: W, type: WidthType.DXA}, columnWidths: [W],
    rows: [new TableRow({children: [new TableCell({children: paras, width: {size: W, type: WidthType.DXA},
      shading: {type: ShadingType.CLEAR, color: "auto", fill: "F7F9FC"}, margins: {top: 140, bottom: 100, left: 200, right: 200},
      borders: {top: B, bottom: B, right: B, left: {style: BorderStyle.SINGLE, size: 24, color: NAVY}}})]})]});
}
function note(parts) {
  return new Table({width: {size: W, type: WidthType.DXA}, columnWidths: [W],
    rows: [new TableRow({children: [new TableCell({children: (Array.isArray(parts[0]) ? parts : [parts]).map((p, i) => P(p, {size: 22, after: 60, b: false})),
      width: {size: W, type: WidthType.DXA}, shading: {type: ShadingType.CLEAR, color: "auto", fill: CREAM},
      margins: {top: 100, bottom: 80, left: 180, right: 180}, borders: {top: NONE, bottom: NONE, right: NONE, left: {style: BorderStyle.SINGLE, size: 24, color: GOLD}}})]})]});
}
const sp = (n = 80) => new Paragraph({children: [], spacing: {before: 0, after: n}});

// ------------------------------------------------------------------ dau trang
const logo = fs.readFileSync("/home/claude/ssr/crops/logo_192.png");
const head = new Table({width: {size: W, type: WidthType.DXA}, columnWidths: [1100, W - 1100], borders: {top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE},
  rows: [new TableRow({children: [
    new TableCell({width: {size: 1100, type: WidthType.DXA}, borders: {top: NONE, bottom: NONE, left: NONE, right: NONE}, verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({children: [new ImageRun({type: "png", data: logo, transformation: {width: 58, height: 58}})]})]}),
    new TableCell({width: {size: W - 1100, type: WidthType.DXA}, borders: {top: NONE, bottom: NONE, left: NONE, right: NONE}, verticalAlign: VerticalAlign.CENTER,
      children: [P("NHÓM CƯ DÂN GIÁM SÁT QUỸ BẢO TRÌ", {b: true, size: 20, c: NAVY, after: 20}), P("Chung cư Nam Sài Gòn Residences · tài liệu làm việc", {size: 20, c: "5B6474", after: 0})]})]})]});

const body = [
  head,
  new Paragraph({children: [], border: {bottom: {style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 4}}, spacing: {after: 160}}),
  P("HƯỚNG DẪN GỬI TÀI LIỆU VÀ TIN NHẮN MẪU", {b: true, size: 34, c: NAVY, after: 60}),
  P("Quỹ bảo trì chung cư Nam Sài Gòn Residences · cập nhật ngày 29/09/2026", {i: true, size: 22, c: "5B6474", after: 160}),
  note([["Dùng cho nhóm điều phối: gửi gì, gửi khi nào, cho ai, và nhắn gì cho từng đối tượng."],
        ["Trong tài liệu, ", {t: "N", b: true}, " là ngày nộp công văn cho Ban quản trị. Tin nhắn mẫu ở mục 4, chỗ có dấu … là chỗ cần điền."],
        ["Mọi nội dung gửi đi là đề nghị làm rõ, không phải cáo buộc; không nêu tên cá nhân."]]),

  H1("1. Bộ tài liệu và nơi để"),
  P("Thư mục Ket qua phan tich có ba thư mục con, chia theo người nhận.", {after: 80}),
  table(["Thư mục", "Tệp", "Dùng khi nào"], [
    ["1_Gui_Ban_quan_tri", "Công văn kiến nghị (Word để điền và in; PDF để xem)", "In, lấy chữ ký ở Phụ lục 2, nộp Ban quản trị ngày N"],
    ["", "Báo cáo phân tích đầy đủ (PDF, 40 trang)", "Tài liệu kèm theo số (1) của công văn"],
    ["", "Sao kê tổng hợp và phân tích (Excel)", "Tài liệu kèm theo số (2) của công văn"],
    ["2_Cho_cu_dan", "Mười câu hỏi: ảnh để đăng nhóm, PDF khổ A4 để in", "Đăng từ N+1, sau khi Ban quản trị đã nhận công văn"],
    ["", "Ba ảnh trọng tâm (ảnh 1 là Hiểu đúng vấn đề)", "Ảnh 1 kèm tin mời ký và bài đăng N+1"],
    ["", "Bản tóm tắt (PDF, 13 trang)", "Gửi người muốn đọc kỹ mà chưa cần bản đầy đủ"],
    ["", "Clip dọc Mười câu hỏi (87 giây)", "Đăng N+2 hoặc N+3 trên Zalo, TikTok, Reels"],
    ["", "Clip dọc ngắn (64 giây), clip ngang (3 phút 51 giây)", "Giải thích bốn ý; clip ngang hợp Facebook, YouTube"],
    ["", "Dashboard bản offline", "Chỉ gửi riêng cho ai không mở được đường dẫn"],
    ["3_Tai_lieu_lam_viec", "Phân loại nguyên nhân; Hỏi dần", "Nhóm điều phối dùng để hỏi tiếp và đánh giá câu trả lời; không kèm công văn"],
    ["Dashboard (đường dẫn)", LINK, "Kênh chính cho cư dân: báo cáo, mười câu hỏi, hỏi đáp, tình trạng từng hồ sơ"],
  ], [2750, 3550, 3338], {first: true, firstSize: 20}),

  H1("2. Quy trình bảy bước"),
  table(["Bước", "Khi nào", "Việc làm", "Tin mẫu"], [
    ["1", "Trước N, 2 – 3 ngày", ["Điền số, ngày, người đại diện vào công văn; lấy chữ ký ở Phụ lục 2 (họ tên, căn hộ, block).",
                                  "Chỉ gửi công văn và ảnh trọng tâm 1 cho người được mời ký; chưa đăng nhóm lớn."], "Mẫu 1"],
    ["2", "Ngày N, thứ Hai tới thứ Tư, giờ hành chính", ["Nộp bản giấy có chữ ký cho Ban quản trị, xin ký nhận vào bản lưu.",
                                  "Gửi thêm email kèm công văn PDF, báo cáo đầy đủ, file Excel.",
                                  "Gửi một bản cho đơn vị quản lý vận hành (công văn ghi để phối hợp)."], "Mẫu 2"],
    ["3", "N+1", ["Đăng nhóm cư dân: bài tóm tắt, ảnh Mười câu hỏi đã điền ngày gửi, ảnh trọng tâm 1, đường dẫn dashboard.",
                  "In PDF Mười câu hỏi dán bảng tin nếu được phép."], "Mẫu 3"],
    ["4", "N+2 hoặc N+3", ["Đăng clip dọc Mười câu hỏi; clip ngang cho Facebook, YouTube.", "Mỗi ngày một nội dung, không đăng dồn một lúc."], "Mẫu 4"],
    ["5", "Từ N+1 tới N+15", ["Cập nhật tình trạng từng hồ sơ trên dashboard.",
                              "Mỗi lần Ban quản trị trả lời: ghi vào mẫu ghi nhận trong file Hỏi dần, sửa nhóm trong file Phân loại."], "Mục 5"],
    ["6", "N+7", ["Nếu chưa có phản hồi, gửi tin nhắc lịch sự, đề nghị cung cấp trước ba hồ sơ ưu tiên."], "Mẫu 5"],
    ["7", "N+16", ["Đăng bài cập nhật cho cư dân.",
                   "Còn thiếu hồ sơ: gửi công văn vòng 2, đề nghị kiểm toán đột xuất (Điều 8.8.b Quy chế thu chi).",
                   "Vẫn không được đáp ứng: kiến nghị UBND phường và Sở Xây dựng, hoặc gom đơn của tối thiểu 50% đại diện chủ sở hữu căn hộ để đề nghị họp Hội nghị nhà chung cư bất thường (Điều 16 Quy chế kèm Thông tư 05/2024/TT-BXD)."], "Mẫu 6"],
  ], [700, 1900, 5838, 1200], {first: true}),

  H1("3. Nên và không nên"),
  table(["Nên", "Không nên"], [
    ["Gửi Ban quản trị trước, rồi mới đăng nhóm cư dân.", "Đăng ảnh hay clip Mười câu hỏi khi Ban quản trị chưa nhận công văn."],
    ["Giữ bản công văn có chữ ký nhận của Ban quản trị.", "Kèm file Phân loại hoặc Hỏi dần vào bộ hồ sơ gửi Ban quản trị."],
    ["Một người làm đầu mối liên hệ; mọi trao đổi bằng văn bản.", "Trích riêng nhãn chưa loại trừ (3) đem lên nhóm, tách khỏi điều kiện đổi nhóm."],
    ["Mời Ban quản trị trả lời công khai trên cùng kênh.", "Nêu tên cá nhân, đoán động cơ, bình luận công kích."],
    ["Đưa đường dẫn dashboard để cư dân tự đọc và tra cứu.", "Gửi file Excel hay dashboard offline vào nhóm lớn."],
  ], [4819, 4819], {band: true}),

  H1("4. Tin nhắn mẫu"),
  H2("Mẫu 1. Mời ký công văn", "gửi riêng người được mời ký · kèm công văn PDF và ảnh trọng tâm 1"),
  msg(["Chào anh/chị,",
       "Nhóm cư dân đã rà soát sao kê quỹ bảo trì chung cư Nam Sài Gòn Residences (15/08/2024 – 31/05/2026). Tóm gọn: trên sao kê tiền không biến mất, nhưng có 3 điểm làm trái quy định, quỹ sinh lời kém hơn mức có thể, và 1,69 tỷ còn phải có chứng từ mới khẳng định được là không mất.",
       "Nhóm đã soạn công văn đề nghị Ban quản trị cung cấp hồ sơ và giải trình trong 15 ngày (file đính kèm). Công văn chỉ đề nghị cung cấp thông tin, không quy kết cá nhân nào.",
       "Nếu đồng ý, anh/chị vui lòng ký vào danh sách (họ tên, căn hộ, block) tại … trước ngày …/…/2026. Cảm ơn anh/chị!"]),
  H2("Mẫu 2. Gửi Ban quản trị", "email hoặc tin kèm bản giấy · đính kèm công văn PDF, báo cáo đầy đủ, file Excel"),
  msg(["Kính gửi Ban Quản trị nhà chung cư Nam Sài Gòn Residences,",
       "Thay mặt các chủ sở hữu, người sử dụng ký tên tại Phụ lục 2, chúng tôi gửi Ban Quản trị Văn bản kiến nghị số …/2026/KN-CSH ngày …/…/2026 về việc cung cấp hồ sơ, giải trình và khắc phục trong quản lý, sử dụng kinh phí bảo trì phần sở hữu chung.",
       "Tài liệu kèm theo: (1) Báo cáo phân tích sao kê quỹ bảo trì; (2) Tệp Excel sao kê tổng hợp và phân tích; (3) Phụ lục 1: Danh mục hồ sơ đề nghị cung cấp; (4) Phụ lục 2: Danh sách ký tên.",
       "Kính đề nghị Ban Quản trị xác nhận đã nhận văn bản và phản hồi trong thời hạn 15 ngày kể từ ngày nhận. Mọi trao đổi xin gửi về đại diện liên hệ: Ông/Bà …, căn hộ …, điện thoại …, email ….",
       "Trân trọng."]),
  H2("Mẫu 3. Đăng nhóm cư dân", "ngày N+1 · kèm ảnh Mười câu hỏi và ảnh trọng tâm 1"),
  msg(["📌 QUỸ BẢO TRÌ NAM SÀI GÒN RESIDENCES: 10 CÂU HỎI ĐÃ GỬI BAN QUẢN TRỊ",
       "Ngày …/…/2026, … chủ sở hữu đã gửi Ban quản trị công văn đề nghị cung cấp hồ sơ và giải trình về quỹ bảo trì, hạn trả lời 15 ngày.",
       "Hiểu đúng vấn đề trong 4 ý:",
       "✅ Trên sao kê, tiền không biến mất: 198 giao dịch khớp số dư tới từng đồng.",
       "⚠️ Có 3 điểm làm trái quy định: 986,9 triệu tiền quỹ đi qua tài khoản vận hành, 1,71 tỷ tiền khu vực chung nằm ngoài quỹ, 1,40 tỷ chi không qua quy trình của quỹ.",
       "📉 Quỹ sinh lời kém hơn mức có thể: bỏ lỡ tới 0,96 tỷ tiền lãi (thiệt hại cơ hội, không phải bị lấy đi).",
       "📄 1,69 tỷ còn chờ chứng từ mới khẳng định được là không mất.",
       "👉 10 câu hỏi: xem ảnh đính kèm.",
       "👉 Báo cáo đầy đủ, hỏi đáp và tình trạng từng hồ sơ: " + LINK,
       "Đây là phân tích độc lập phục vụ giám sát của cư dân; các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc. Nhóm sẽ cập nhật khi Ban quản trị trả lời, và rất mong Ban quản trị phản hồi công khai để cư dân cùng nắm."]),
  H2("Mẫu 4. Đăng clip", "ngày N+2 hoặc N+3 · kèm clip dọc Mười câu hỏi"),
  msg(["🎬 90 giây: 10 câu hỏi đã gửi Ban quản trị về quỹ bảo trì. Hạn trả lời 15 ngày. Theo dõi câu trả lời và tình trạng từng hồ sơ tại: " + LINK]),
  H2("Mẫu 5. Nhắc Ban quản trị", "ngày N+7, nếu chưa có phản hồi"),
  msg(["Kính gửi Ban Quản trị,",
       "Ngày …/…/2026, Ban Quản trị đã nhận Văn bản kiến nghị số …/2026/KN-CSH của các chủ sở hữu về kinh phí bảo trì. Đến nay chúng tôi chưa nhận được phản hồi.",
       "Kính đề nghị Ban Quản trị cho biết thời điểm dự kiến trả lời và cung cấp trước ba hồ sơ ưu tiên tại mục II của văn bản. Hạn trả lời theo văn bản là ngày …/…/2026.",
       "Trân trọng."]),
  H2("Mẫu 6. Cập nhật cho cư dân sau 15 ngày", "ngày N+16"),
  msg(["📌 CẬP NHẬT QUỸ BẢO TRÌ SAU 15 NGÀY",
       "Ban quản trị đã trả lời ngày …/…/2026 (hoặc: đến nay chưa trả lời).",
       "✅ Đã nhận: …",
       "⏳ Chưa nhận: …",
       "Đánh giá sơ bộ: …",
       "Bước tiếp theo: …",
       "Chi tiết và tình trạng từng hồ sơ: " + LINK]),

  H1("5. Khi Ban quản trị trả lời"),
  P("Ghi ngày nhận, hình thức trả lời và chép nguyên văn ý chính vào mẫu ghi nhận ở cuối file Hỏi dần.", {bullet: true, after: 60}),
  P("Đối chiếu với ba dòng (1), (2), (3) của vấn đề tương ứng để có đánh giá tạm, rồi soạn câu hỏi vòng sau nếu còn thiếu.", {bullet: true, after: 60}),
  P("Cập nhật tình trạng hồ sơ trên dashboard: chưa nhận, nhận một phần, đã nhận đủ.", {bullet: true, after: 60}),
  P("Khi điều kiện ở cột Đổi phân loại khi của file Phân loại xảy ra, sửa nhóm tương ứng trong file đó.", {bullet: true, after: 60}),
  P("Báo nhóm cư dân bằng Mẫu 6, chỉ nêu dữ kiện: đã nhận gì, còn thiếu gì, bước tiếp theo.", {bullet: true, after: 60}),
];

const doc = new Document({
  creator: "Nhóm cư dân giám sát quỹ bảo trì", title: "Hướng dẫn gửi tài liệu và tin nhắn mẫu",
  styles: {default: {document: {run: {font: FONT, size: SZ}}}},
  numbering: {config: [{reference: "dot", levels: [{level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: {paragraph: {indent: {left: 460, hanging: 260}}, run: {color: GOLD}}}]}]},
  sections: [{
    properties: {page: {size: {width: 11906, height: 16838}, margin: {top: 1020, bottom: 1020, left: 1134, right: 1134}}},
    footers: {default: new Footer({children: [new Paragraph({alignment: AlignmentType.LEFT, border: {top: {style: BorderStyle.SINGLE, size: 4, color: GOLD, space: 4}},
      children: [run("SỔ QUỸ BẢO TRÌ SSR  ", {b: true, size: 17, c: NAVY}), run("Tài liệu làm việc của nhóm cư dân; các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.   Trang ", {size: 17, c: "5B6474"}),
                 new TextRun({children: [PageNumber.CURRENT], font: FONT, size: 17, color: "5B6474"}), run("/", {size: 17, c: "5B6474"}),
                 new TextRun({children: [PageNumber.TOTAL_PAGES], font: FONT, size: 17, color: "5B6474"})]})]})},
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("/home/claude/ssr/cv/Huong_dan_gui_tai_lieu_va_tin_nhan_mau.docx", b); console.log("ok", b.length); });
