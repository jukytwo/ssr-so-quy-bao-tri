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
const DRIVE = "https://drive.google.com/drive/folders/1gb8brZ_Bxhc0Jm7wYimdKmsWBnyzQEH8";
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
  const LB = {style: BorderStyle.SINGLE, size: 24, color: NAVY};
  const FILL = {type: ShadingType.CLEAR, color: "auto", fill: "F7F9FC"};
  if (lines.length <= 8) {
    const paras = lines.map(l => P(l, {size: 22, after: l === "" ? 0 : 60, line: 270}));
    return new Table({width: {size: W, type: WidthType.DXA}, columnWidths: [W],
      rows: [new TableRow({cantSplit: true, children: [new TableCell({children: paras, width: {size: W, type: WidthType.DXA},
        shading: FILL, margins: {top: 110, bottom: 70, left: 200, right: 200}, borders: {top: B, bottom: B, right: B, left: LB}})]})]});
  }
  // tin dai: moi doan mot hang, chi ngat trang giua cac doan
  const n = lines.length;
  return new Table({width: {size: W, type: WidthType.DXA}, columnWidths: [W],
    rows: lines.map((l, i) => new TableRow({cantSplit: true, children: [new TableCell({children: [P(l, {size: 22, after: 0, line: 270})],
      width: {size: W, type: WidthType.DXA}, shading: FILL,
      margins: {top: i === 0 ? 110 : 30, bottom: i === n - 1 ? 70 : 30, left: 200, right: 200},
      borders: {top: i === 0 ? B : NONE, bottom: i === n - 1 ? B : NONE, right: B, left: LB}})]}))});
}
function note(parts) {
  return new Table({width: {size: W, type: WidthType.DXA}, columnWidths: [W],
    rows: [new TableRow({children: [new TableCell({children: (Array.isArray(parts[0]) ? parts : [parts]).map((p, i) => P(p, {size: 22, after: 60, b: false})),
      width: {size: W, type: WidthType.DXA}, shading: {type: ShadingType.CLEAR, color: "auto", fill: CREAM},
      margins: {top: 100, bottom: 80, left: 180, right: 180}, borders: {top: NONE, bottom: NONE, right: NONE, left: {style: BorderStyle.SINGLE, size: 24, color: GOLD}}})]})]});
}
const sp = (n = 80) => new Paragraph({children: [], spacing: {before: 0, after: n}});


// ------------------------------------------------------------------ trang 1: anh quy trinh; cac trang sau: tin nhan mau
const proc = fs.readFileSync("/home/claude/ssr/a4/quy_trinh_drive.png");
const IMGW = 640, IMGH = Math.round(640 * 2546 / 1800);
function T(no, title, meta) {
  return new Paragraph({children: [run("Tin mẫu " + no + "  ", {b: true, size: 26, c: GOLD}), run(title, {b: true, size: 26, c: NAVY})].concat(meta ? [run("   " + meta, {i: true, size: 21, c: "5B6474"})] : []),
    spacing: {before: 200, after: 80}, keepNext: true});
}
const body = [
  new Paragraph({children: [new ImageRun({type: "png", data: proc, transformation: {width: IMGW, height: IMGH}})], alignment: AlignmentType.CENTER, spacing: {after: 0}}),
  new Paragraph({children: [run("TIN NHẮN MẪU", {b: true, size: 32, c: NAVY})], pageBreakBefore: true, spacing: {after: 60}}),
  P([{t: "Dùng theo ảnh quy trình ở trang 1. ", b: true}, "Chỗ có dấu … là chỗ cần điền. Số trong ngoặc (1.1, 1.4…) là số thư mục trong link Google Drive chung."], {size: 22, after: 60}),
  P([{t: "Link Google Drive chung (toàn bộ tài liệu): ", b: true}, DRIVE], {size: 22, after: 40}),
  P([{t: "Đường dẫn dashboard: ", b: true}, LINK], {size: 22, after: 120}),
  T(1, "Mời ký công văn", "Bước 1 · gửi riêng người được mời ký · kèm công văn (1.2) và ảnh Hiểu đúng vấn đề (1.4)"),
  msg(["Chào anh/chị,",
       "Nhóm cư dân đã rà soát sao kê quỹ bảo trì chung cư Nam Sài Gòn Residences (15/08/2024 – 31/05/2026). Trên sao kê tiền không biến mất, nhưng có 3 điểm làm trái quy định, quỹ sinh lời kém hơn mức có thể, và 1,69 tỷ còn phải có chứng từ mới khẳng định được là không mất.",
       "Nhóm đã soạn công văn đề nghị Ban quản trị cung cấp hồ sơ và giải trình trong 15 ngày (file đính kèm). Công văn chỉ đề nghị cung cấp thông tin, không quy kết cá nhân nào.",
       "Toàn bộ tài liệu để anh/chị đọc trước: " + DRIVE,
       "Nếu đồng ý, anh/chị vui lòng ký vào danh sách (họ tên, căn hộ, block) tại … trước ngày …/…/2026. Cảm ơn anh/chị."]),
  T(2, "Gửi Ban quản trị", "Bước 2 · email hoặc tin kèm bản giấy · đính kèm công văn PDF (1.2), báo cáo đầy đủ (1.1), file Excel (1.3)"),
  msg(["Kính gửi Ban Quản trị nhà chung cư Nam Sài Gòn Residences,",
       "Thay mặt các chủ sở hữu, người sử dụng ký tên tại Phụ lục 2, chúng tôi gửi Ban Quản trị Văn bản kiến nghị số …/2026/KN-CSH ngày …/…/2026 về việc cung cấp hồ sơ, giải trình và khắc phục trong quản lý, sử dụng kinh phí bảo trì phần sở hữu chung.",
       "Tài liệu kèm theo: (1) Báo cáo phân tích sao kê quỹ bảo trì; (2) Tệp Excel sao kê tổng hợp và phân tích; (3) Phụ lục 1: Danh mục hồ sơ đề nghị cung cấp; (4) Phụ lục 2: Danh sách ký tên.",
       "Kính đề nghị Ban Quản trị xác nhận đã nhận văn bản và phản hồi trong thời hạn 15 ngày kể từ ngày nhận. Mọi trao đổi xin gửi về đại diện liên hệ: Ông/Bà …, căn hộ …, điện thoại …, email ….",
       "Trân trọng."]),
  T(3, "Đăng nhóm chung", "Bước 3 · nhóm có cả cư dân và Ban quản trị · kèm ảnh Mười câu hỏi và ảnh Hiểu đúng vấn đề (1.4)"),
  msg(["QUỸ BẢO TRÌ NAM SÀI GÒN RESIDENCES: 10 CÂU HỎI ĐÃ GỬI BAN QUẢN TRỊ",
       "Ngày …/…/2026, … chủ sở hữu đã gửi Ban quản trị công văn đề nghị cung cấp hồ sơ và giải trình về quỹ bảo trì, hạn trả lời 15 ngày.",
       "Hiểu đúng vấn đề trong 4 ý:",
       "Trên sao kê, tiền không biến mất: 198 giao dịch khớp số dư tới từng đồng.",
       "Có 3 điểm làm trái quy định: 986,9 triệu tiền quỹ đi qua tài khoản vận hành, 1,71 tỷ tiền khu vực chung nằm ngoài quỹ, 1,40 tỷ chi không qua quy trình của quỹ. Theo quy định, các điểm này phải được khắc phục.",
       "Quỹ sinh lời kém hơn mức có thể: bỏ lỡ tới 0,96 tỷ tiền lãi (thiệt hại cơ hội, tiền gốc không mất).",
       "1,69 tỷ còn chờ chứng từ mới khẳng định được là không mất; có chứng từ hợp lệ thì coi như đã giải trình xong, không có thì phải hoàn lại quỹ (Điều 10.1 Quy chế thu chi).",
       "10 câu hỏi: xem ảnh đính kèm.",
       "Báo cáo đầy đủ, hỏi đáp và tình trạng từng hồ sơ: " + LINK,
       "Toàn bộ tài liệu (báo cáo, công văn, Excel, ảnh, clip, sao kê gốc): " + DRIVE,
       "Kính mời Ban quản trị phản hồi ngay tại nhóm này và bằng văn bản theo công văn.",
       "Cư dân có góp ý, bổ sung thông tin hay giấy tờ liên quan, xin bình luận dưới bài hoặc nhắn cho … (đầu mối).",
       "Đây là phân tích độc lập phục vụ giám sát của cư dân; các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc. Nhóm sẽ cập nhật khi Ban quản trị trả lời."]),
  T(4, "Đăng clip, ảnh phân loại", "Bước 4 · đăng vào cùng nhóm, mỗi ngày một nội dung · kèm clip toàn bộ vấn đề (1.5); ngày sau kèm ảnh Phân loại (1.4)"),
  msg(["Clip 11 phút 11 giây gói toàn bộ vấn đề của quỹ bảo trì: điều đã kiểm tra được, năm vấn đề xem theo lưu đồ dòng tiền, mức độ và nguyên nhân, mười câu hỏi đã gửi Ban quản trị ngày 29/09/2026, và ba phương án Hội nghị quyết định.",
       "Clip có mốc chương, muốn xem phần nào thì bấm tới phần đó; có bản dọc để xem trên điện thoại.",
       "Đây là đánh giá sơ bộ của nhóm cư dân, sẽ xem lại khi Ban quản trị cung cấp chứng từ; các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.",
       "Chi tiết: " + LINK]),
  P([{t: "Ngày sau, cùng nhóm: ", b: true}, "ảnh Phân loại nguyên nhân."], {size: 22, before: 80, after: 60}),
  msg(["16 dấu hiệu được xếp theo nguyên nhân: thiếu năng lực, lỡ tay thật, hay chưa loại trừ lỡ tay có chủ đích; kèm cách hỏi dần ba vòng để chốt kết luận.",
       "Chi tiết: " + LINK]),
  T(5, "Nhắc Ban quản trị", "Bước 6 · chỉ khi chưa có phản hồi · gửi bằng văn bản, nhắc cùng nội dung trong nhóm"),
  msg(["Kính gửi Ban Quản trị,",
       "Ngày …/…/2026, Ban Quản trị đã nhận Văn bản kiến nghị số …/2026/KN-CSH của các chủ sở hữu về kinh phí bảo trì. Đến nay chúng tôi chưa nhận được phản hồi.",
       "Kính đề nghị Ban Quản trị cho biết thời điểm dự kiến trả lời và cung cấp trước ba hồ sơ ưu tiên tại mục II của văn bản. Hạn trả lời theo văn bản là ngày …/…/2026.",
       "Theo Điều 6.1.f và Điều 10.1 Quy chế thu chi, mọi khoản chi từ kinh phí bảo trì phải có hóa đơn, chứng từ; khoản nào không có chứng từ hợp lệ thì phải bồi hoàn quỹ.",
       "Trân trọng."]),
  T(6, "Cập nhật trong nhóm chung", "Bước 7 · sau 15 ngày"),
  msg(["CẬP NHẬT QUỸ BẢO TRÌ SAU 15 NGÀY",
       "Ban quản trị đã trả lời ngày …/…/2026 (hoặc: đến nay chưa trả lời).",
       "Đã nhận: …",
       "Chưa nhận: …",
       "Đánh giá sơ bộ: …",
       "Bước tiếp theo: …",
       "Nếu Ban quản trị không trả lời hoặc không khắc phục: nhóm kiến nghị Ủy ban nhân dân phường, Sở Xây dựng xem xét, xử lý theo Nghị định 339/2026/NĐ-CP, và gom đơn của tối thiểu 50% đại diện chủ sở hữu để đề nghị họp Hội nghị nhà chung cư bất thường, xem xét bãi nhiệm (Điều 16, Điều 26 Quy chế quản lý, sử dụng nhà chung cư).",
       "Chi tiết và tình trạng từng hồ sơ: " + LINK,
       "Tài liệu đầy đủ: " + DRIVE]),
];

const doc = new Document({
  creator: "Nhóm cư dân giám sát quỹ bảo trì", title: "Quy trình và tin nhắn mẫu",
  styles: {default: {document: {run: {font: FONT, size: SZ}}}},
  numbering: {config: [{reference: "dot", levels: [{level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: {paragraph: {indent: {left: 460, hanging: 260}}, run: {color: GOLD}}}]}]},
  sections: [{
    properties: {page: {size: {width: 11906, height: 16838}, margin: {top: 900, bottom: 900, left: 1134, right: 1134}}},
    footers: {default: new Footer({children: [new Paragraph({alignment: AlignmentType.LEFT, border: {top: {style: BorderStyle.SINGLE, size: 4, color: GOLD, space: 4}},
      children: [run("SỔ QUỸ BẢO TRÌ SSR  ", {b: true, size: 17, c: NAVY}), run("Tài liệu làm việc của nhóm cư dân; các nhận định là dấu hiệu cần làm rõ, không phải cáo buộc.   Trang ", {size: 17, c: "5B6474"}),
                 new TextRun({children: [PageNumber.CURRENT], font: FONT, size: 17, color: "5B6474"}), run("/", {size: 17, c: "5B6474"}),
                 new TextRun({children: [PageNumber.TOTAL_PAGES], font: FONT, size: 17, color: "5B6474"})]})]})},
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("/home/claude/ssr/cv/tin_nhan_mau_drive.docx", b); console.log("ok", b.length); });
