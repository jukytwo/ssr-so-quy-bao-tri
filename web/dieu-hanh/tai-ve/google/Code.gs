/**
 * SSR Điều Hành, máy chủ dữ liệu chung trên Google Sheets (bản riêng, không dùng chung với công cụ khác).
 * Cách cài: xem file HUONG-DAN-GOOGLE-SHEETS.md. Sau khi dán mã, chạy hàm caiDat() một lần.
 */
const TZ = 'Asia/Ho_Chi_Minh';
const SH_MSG = 'TinNhan', SH_NT = 'BangTin', SH_LOG = 'NhatKy';
const MSG_COLS = ['Mã tin', 'Thời điểm gửi', 'Họ tên', 'Căn hộ', 'Điện thoại', 'Loại', 'Nội dung', 'Công khai', 'Mã theo dõi', 'Trạng thái', 'Đọc lúc', 'Người đọc', 'Phản hồi', 'Phản hồi lúc', 'Người phản hồi', 'Mã phản ánh', 'Cập nhật lúc'];
const K = { id: 0, t: 1, name: 2, unit: 3, phone: 4, type: 5, content: 6, pub: 7, track: 8, status: 9, readAt: 10, readBy: 11, reply: 12, replyAt: 13, replyBy: 14, ticket: 15, upd: 16 };
const NT_COLS = ['Mã', 'Tiêu đề', 'Nội dung', 'Loại', 'Phạm vi', 'Từ ngày', 'Đến ngày', 'Ghim'];
const TYPES = ['Phản ánh sự cố', 'Góp ý', 'Hỏi đáp', 'Khác'];
const STATUSES = ['Đã gửi', 'Đã đọc', 'Đang xử lý', 'Đã phản hồi', 'Đã xong'];
const LOCK_MIN = 10;

function P_() { return PropertiesService.getScriptProperties(); }
function ss_() { return SpreadsheetApp.getActiveSpreadsheet(); }

/** Chạy một lần sau khi dán mã: tạo các sheet và sinh khóa truy cập. Khóa hiện ở mục Nhật ký thực thi. */
function setup() {
  const ss = ss_();
  ensure_(ss, SH_MSG, MSG_COLS); ensure_(ss, SH_NT, NT_COLS); ensure_(ss, SH_LOG, ['Thời điểm', 'Người', 'Thao tác', 'Chi tiết']);
  const p = P_();
  if (!p.getProperty('ADMIN_KEY')) p.setProperty('ADMIN_KEY', 'QT-' + rnd_(12));
  if (!p.getProperty('VIEW_KEY')) p.setProperty('VIEW_KEY', 'XEM-' + rnd_(10));
  Logger.log('Khóa quản trị (chỉ đưa cho người được sửa dữ liệu): ' + p.getProperty('ADMIN_KEY'));
  Logger.log('Khóa xem (đưa cho Ban Quản trị, nhân viên chỉ xem): ' + p.getProperty('VIEW_KEY'));
  setupV3_();
}
/** Đổi khóa khi nghi bị lộ. Khóa cũ hết hiệu lực ngay. */
function doiKhoa() { P_().deleteProperty('ADMIN_KEY'); P_().deleteProperty('VIEW_KEY'); setup(); }

function ensure_(ss, name, cols) {
  let sh = ss.getSheetByName(name); if (!sh) sh = ss.insertSheet(name);
  if (sh.getLastRow() === 0) { sh.appendRow(cols); sh.setFrozenRows(1); sh.getRange(1, 1, 1, cols.length).setFontWeight('bold').setBackground('#E3EEE7'); }
  return sh;
}
function rnd_(n) { const a = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; let s = ''; for (let i = 0; i < n; i++) s += a.charAt(Math.floor(Math.random() * a.length)); return s; }
function stamp_(d) { return Utilities.formatDate(d || new Date(), TZ, "yyyy-MM-dd'T'HH:mm:ss"); }
function str_(v) { return v instanceof Date ? stamp_(v) : String(v == null ? '' : v); }
function clean_(v, n) { let s = String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, n); if (/^[=+\-@]/.test(s)) s = "'" + s; return s; }
function text_(s) { return /^[+\d][\d\s.]*$/.test(s) ? "'" + s : s; }

function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.api) return out_(route_(p.api, p));
  if (p.csv) return csv_(p);
  if (p.cp || p.tb || p.m || p.g || p.sc) return page_('Field').setTitle('Hiện trường Saigon South Residences').addMetaTag('viewport', 'width=device-width, initial-scale=1');
  if (p.p === 'bql') {
    const id = P_().getProperty('BQL_FILE_ID');
    if (id) return HtmlService.createHtmlOutput(DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8')).setTitle('Quản lý Saigon South Residences').addMetaTag('viewport', 'width=device-width, initial-scale=1').setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }
  return page_('Portal').setTitle('Cổng cư dân Saigon South Residences').addMetaTag('viewport', 'width=device-width, initial-scale=1');
}
function doPost(e) { let b = {}; try { b = JSON.parse(e.postData.contents); } catch (x) { } return out_(route_(b.api, b)); }
/** Dùng cho google.script.run từ cổng cư dân và trang Ban Quản lý đặt trên Google. */
function api(b) { b = b || {}; return route_(b.api, b); }
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function route_(a, b) {
  try {
    switch (a) {
      case 'ping': return { ok: true, t: Date.now(), name: ss_().getName(), role: role_(b) };
      case 'send': return send_(b);
      case 'public': return { ok: true, items: listPublic_() };
      case 'mine': return { ok: true, items: mine_(b.tracks) };
      case 'notices': return { ok: true, items: notices_() };
      case 'inbox': need_(b, 'view'); return { ok: true, items: rows_().map(full_) };
      case 'read': need_(b, 'admin'); return mark_(b);
      case 'status': need_(b, 'admin'); return status_(b);
      case 'reply': need_(b, 'admin'); return reply_(b);
      case 'pushNotices': need_(b, 'admin'); return pushNotices_(b);
      case 'lock': need_(b, 'admin'); return lock_(b);
      case 'pull': need_(b, 'view'); return pull_(b);
      case 'push': need_(b, 'admin'); return push_(b);
      case 'sheets': need_(b, 'admin'); return sheets_(b);
      default: if (V3[a]) return V3[a](b); return { ok: false, error: 'Yêu cầu không hợp lệ' };
    }
  } catch (err) { return { ok: false, error: String((err && err.message) || err) }; }
}
function role_(b) { const p = P_(), k = b && b.key; if (k && k === p.getProperty('ADMIN_KEY')) return 'admin'; if (k && k === p.getProperty('VIEW_KEY')) return 'view'; return 'public'; }
function need_(b, lvl) { const r = role_(b); if (r === 'admin' || (lvl === 'view' && r === 'view')) return; throw new Error(lvl === 'admin' ? 'Cần khóa quản trị' : 'Cần khóa truy cập hợp lệ'); }
function log_(who, act, detail) { try { ss_().getSheetByName(SH_LOG).appendRow([stamp_(), clean_(who, 80), act, clean_(detail, 500)]); } catch (e) { } }

/* ----- tin nhắn cư dân ----- */
function sheet_() { return ss_().getSheetByName(SH_MSG); }
function rows_() { const sh = sheet_(); const n = sh.getLastRow(); if (n < 2) return []; return sh.getRange(2, 1, n - 1, MSG_COLS.length).getValues(); }
function full_(r) { return { id: str_(r[K.id]), t: str_(r[K.t]), name: str_(r[K.name]), unit: str_(r[K.unit]), phone: str_(r[K.phone]), type: str_(r[K.type]), content: str_(r[K.content]), pub: str_(r[K.pub]), track: str_(r[K.track]), status: str_(r[K.status]), readAt: str_(r[K.readAt]), readBy: str_(r[K.readBy]), reply: str_(r[K.reply]), replyAt: str_(r[K.replyAt]), replyBy: str_(r[K.replyBy]), ticket: str_(r[K.ticket]), upd: str_(r[K.upd]) }; }
function pub_(r) { const u = str_(r[K.unit]); return { id: str_(r[K.id]), t: str_(r[K.t]), block: u ? 'Block ' + u.charAt(0) : '', type: str_(r[K.type]), content: str_(r[K.content]).slice(0, 600), status: str_(r[K.status]), readAt: str_(r[K.readAt]), reply: str_(r[K.reply]), replyAt: str_(r[K.replyAt]) }; }
function send_(b) {
  const content = clean_(b.content, 2000); if (content.replace(/'/g, '').length < 5) throw new Error('Nội dung quá ngắn');
  const unit = clean_(b.unit, 12).toUpperCase(); if (unit && !/^[ABCDEG]-\d{2}\.\d{2}$/.test(unit)) throw new Error('Mã căn hộ chưa đúng dạng, ví dụ A-12.05');
  const phone = clean_(b.phone, 20), type = TYPES.indexOf(b.type) >= 0 ? b.type : 'Khác';
  const cache = CacheService.getScriptCache(), rk = 'rl_' + (unit || phone || 'khach'), n = +(cache.get(rk) || 0);
  if (n >= 6) throw new Error('Bạn đã gửi nhiều tin trong thời gian ngắn, vui lòng thử lại sau ít phút');
  cache.put(rk, String(n + 1), 600);
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try {
    const now = new Date(), id = 'TN-' + Utilities.formatDate(now, TZ, 'yyMMdd-HHmmss') + '-' + rnd_(2), track = rnd_(6);
    sheet_().appendRow([id, stamp_(now), clean_(b.name, 80), unit, text_(phone), type, content, (b.pub === false || b.pub === 'Không') ? 'Không' : 'Có', track, 'Đã gửi', '', '', '', '', '', '', stamp_(now)]);
    if (!b._test) notify_(id, unit, type, content);
    if (b.photo) { try { savePhoto_(id, 'Cư dân', clean_(b.name, 80) || unit || 'Cư dân', b.photo, b.thumb); } catch (x) { } }
    return { ok: true, id: id, track: track };
  } finally { lock.releaseLock(); }
}
function notify_(id, unit, type, content) {
  const to = P_().getProperty('NOTIFY_EMAIL'); if (!to) return;
  try { MailApp.sendEmail(to, '[SSR Điều Hành] ' + type + ' mới ' + id + (unit ? ', căn ' + unit : ''), content + '\n\nMở công cụ quản lý, mục Hộp thư cư dân để đọc và phản hồi.'); } catch (e) { }
}
function listPublic_() { const out = []; const rs = rows_(); for (let i = rs.length - 1; i >= 0 && out.length < 80; i--) if (str_(rs[i][K.pub]) === 'Có') out.push(pub_(rs[i])); return out; }
function mine_(tracks) {
  if (!Array.isArray(tracks)) return []; const set = {}; tracks.slice(0, 30).forEach(t => { t = String(t).toUpperCase(); if (/^[A-Z0-9]{6}$/.test(t)) set[t] = 1; });
  return rows_().filter(r => set[str_(r[K.track])]).map(r => { const o = full_(r); delete o.phone; return o; }).reverse();
}
function findRow_(id) { const rs = rows_(); for (let i = 0; i < rs.length; i++) if (str_(rs[i][K.id]) === id) return { i: i + 2, r: rs[i] }; return null; }
function setRow_(f) { sheet_().getRange(f.i, 1, 1, MSG_COLS.length).setValues([f.r]); }
function mark_(b) {
  const ids = (Array.isArray(b.ids) ? b.ids : []).slice(0, 100), who = clean_(b.who || 'Ban Quản lý', 80); let n = 0;
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try { ids.forEach(id => { const f = findRow_(String(id)); if (f && !str_(f.r[K.readAt])) { f.r[K.readAt] = stamp_(); f.r[K.readBy] = who; if (str_(f.r[K.status]) === 'Đã gửi') f.r[K.status] = 'Đã đọc'; f.r[K.upd] = stamp_(); setRow_(f); n++; } }); }
  finally { lock.releaseLock(); }
  return { ok: true, n: n };
}
function status_(b) {
  if (STATUSES.indexOf(b.status) < 0) throw new Error('Trạng thái không hợp lệ');
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try { const f = findRow_(String(b.id)); if (!f) throw new Error('Không tìm thấy tin ' + b.id); const who = clean_(b.who || 'Ban Quản lý', 80);
    if (!str_(f.r[K.readAt])) { f.r[K.readAt] = stamp_(); f.r[K.readBy] = who; }
    f.r[K.status] = b.status; if (b.ticket) f.r[K.ticket] = clean_(b.ticket, 20); f.r[K.upd] = stamp_(); setRow_(f); log_(who, 'Đổi trạng thái', b.id + ': ' + b.status); return { ok: true }; }
  finally { lock.releaseLock(); }
}
function reply_(b) {
  const text = clean_(b.text, 2000); if (text.length < 2) throw new Error('Nội dung phản hồi quá ngắn');
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try { const f = findRow_(String(b.id)); if (!f) throw new Error('Không tìm thấy tin ' + b.id); const who = clean_(b.who || 'Ban Quản lý', 80);
    if (!str_(f.r[K.readAt])) { f.r[K.readAt] = stamp_(); f.r[K.readBy] = who; }
    f.r[K.reply] = text; f.r[K.replyAt] = stamp_(); f.r[K.replyBy] = who; if (str_(f.r[K.status]) !== 'Đã xong') f.r[K.status] = 'Đã phản hồi'; f.r[K.upd] = stamp_(); setRow_(f); log_(who, 'Phản hồi', b.id); return { ok: true }; }
  finally { lock.releaseLock(); }
}
/* ----- bảng tin ----- */
function notices_() {
  const sh = ss_().getSheetByName(SH_NT), n = sh.getLastRow(); if (n < 2) return [];
  const td = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd');
  return sh.getRange(2, 1, n - 1, NT_COLS.length).getValues().map(r => ({ id: str_(r[0]), title: str_(r[1]), body: str_(r[2]), category: str_(r[3]), scope: str_(r[4]), start: str_(r[5]).slice(0, 10), end: str_(r[6]).slice(0, 10), pinned: str_(r[7]) }))
    .filter(x => x.start <= td && x.end >= td).sort((a, b) => (b.pinned === 'Có') - (a.pinned === 'Có') || (b.start > a.start ? 1 : -1));
}
function pushNotices_(b) {
  const items = (Array.isArray(b.items) ? b.items : []).slice(0, 60), sh = ss_().getSheetByName(SH_NT), n = sh.getLastRow();
  if (n > 1) sh.getRange(2, 1, n - 1, NT_COLS.length).clearContent();
  if (items.length) sh.getRange(2, 1, items.length, NT_COLS.length).setValues(items.map(x => ["'" + clean_(x.id, 20), clean_(x.title, 200), clean_(x.body, 2000), clean_(x.category, 60), clean_(x.scope, 60), "'" + clean_(x.start, 10), "'" + clean_(x.end, 10), x.pinned === 'Có' ? 'Có' : 'Không']));
  return { ok: true, n: items.length };
}
/* ----- đồng bộ toàn bộ dữ liệu Ban Quản lý ----- */
function lock_(b) {
  const p = P_(), now = Date.now(), dev = clean_(b.dev, 20), lk = LockService.getScriptLock(); lk.waitLock(10000);
  try {
    const by = p.getProperty('LOCK_BY'), d = p.getProperty('LOCK_DEV'), until = +(p.getProperty('LOCK_UNTIL') || 0);
    if (b.release) { if (d === dev) { p.deleteProperty('LOCK_BY'); p.deleteProperty('LOCK_DEV'); p.deleteProperty('LOCK_UNTIL'); } return { ok: true, released: true }; }
    if (until > now && d && d !== dev && !b.force) return { ok: false, holder: by, until: until };
    const u = now + LOCK_MIN * 60000; p.setProperty('LOCK_BY', clean_(b.who || 'Ban Quản lý', 80)); p.setProperty('LOCK_DEV', dev); p.setProperty('LOCK_UNTIL', String(u));
    return { ok: true, until: u };
  } finally { lk.releaseLock(); }
}
function pull_(b) {
  const p = P_(), id = p.getProperty('DATA_FILE_ID'), ver = +(p.getProperty('DATA_VERSION') || 0);
  if (!id || !ver) return { ok: true, version: 0 };
  if (b.since && +b.since >= ver) return { ok: true, version: ver, same: true };
  return { ok: true, version: ver, by: p.getProperty('DATA_BY') || '', at: p.getProperty('DATA_AT') || '', data: DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8') };
}
function push_(b) {
  if (typeof b.data !== 'string' || b.data.length < 20) throw new Error('Thiếu dữ liệu');
  let o; try { o = JSON.parse(b.data); } catch (e) { throw new Error('Dữ liệu không phải JSON hợp lệ'); }
  if (!o || o.app !== 'SSR-DH') throw new Error('Dữ liệu không phải của công cụ SSR Điều Hành');
  const p = P_(), lk = LockService.getScriptLock(); lk.waitLock(20000);
  try {
    const ver = +(p.getProperty('DATA_VERSION') || 0), now = Date.now(), dev = clean_(b.dev, 20);
    if (+b.base !== ver && !b.force) return { ok: false, conflict: true, version: ver, by: p.getProperty('DATA_BY') || '' };
    const lockDev = p.getProperty('LOCK_DEV'), until = +(p.getProperty('LOCK_UNTIL') || 0);
    if (until > now && lockDev && lockDev !== dev && !b.force) return { ok: false, locked: true, holder: p.getProperty('LOCK_BY') };
    let id = p.getProperty('DATA_FILE_ID');
    if (id) DriveApp.getFileById(id).setContent(b.data);
    else {
      const f = DriveApp.createFile('SSRDH-du-lieu-chung.json', b.data, MimeType.PLAIN_TEXT); id = f.getId(); p.setProperty('DATA_FILE_ID', id);
      const parents = DriveApp.getFileById(ss_().getId()).getParents(); if (parents.hasNext()) f.moveTo(parents.next());
    }
    const nv = ver + 1, who = clean_(b.who || 'Ban Quản lý', 80);
    p.setProperty('DATA_VERSION', String(nv)); p.setProperty('DATA_BY', who); p.setProperty('DATA_AT', stamp_());
    try { CacheService.getScriptCache().removeAll(['idxM', 'idxU']); } catch (x) { }
    log_(who, 'Đồng bộ dữ liệu', 'Phiên bản ' + nv + ', ' + Math.round(b.data.length / 1024) + ' KB' + (b.force ? ', ghi đè' : ''));
    try { CacheService.getScriptCache().removeAll(['stat', 'tkst', 'svc']); } catch (x) { } snapshot_(b.data, nv, who);
    return { ok: true, version: nv };
  } finally { lk.releaseLock(); }
}

/* =====================================================================
 * Phần mở rộng: bảng tính đọc được, cảnh báo qua email, bản tin sáng,
 * sao lưu hằng ngày, menu SSR và tự kiểm tra.
 * ===================================================================== */
const MIRROR_NOTE = 'Bảng chỉ để xem, tự cập nhật từ công cụ quản lý. Sửa dữ liệu trong công cụ để mọi thay đổi được ghi nhật ký.';
const BONUS_ = { 'Khẩn cấp': .8, 'Cao': .4, 'Trung bình': .15, 'Thấp': 0 };
const TOL_ = { 'Một lần': 3, 'Hằng ngày': .5, 'Hằng tuần': 2, 'Hằng tháng': 5, 'Hằng quý': 10, 'Nửa năm': 15, 'Hằng năm': 20 };
const LVN_ = { 3: 'Khẩn cấp', 2: 'Cảnh báo', 1: 'Nhắc việc' };

/** Chạy một lần: tạo sheet, sinh khóa, cài lịch tự động (cảnh báo mỗi giờ, bản tin 7 giờ sáng, sao lưu 1 giờ sáng). */
function caiDat() {
  setup();
  ScriptApp.getProjectTriggers().forEach(t => { if (['guiCanhBao', 'banTinSang', 'saoLuu', 'baoCaoTuan'].indexOf(t.getHandlerFunction()) >= 0) ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('guiCanhBao').timeBased().everyHours(1).create();
  ScriptApp.newTrigger('banTinSang').timeBased().atHour(7).everyDays(1).inTimezone(TZ).create();
  ScriptApp.newTrigger('saoLuu').timeBased().atHour(1).everyDays(1).inTimezone(TZ).create();
  ScriptApp.newTrigger('baoCaoTuan').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(7).inTimezone(TZ).create();
  ensure_(ss_(), SH_RT, RT_COLS); ensure_(ss_(), SH_KS, KS_COLS); ensure_(ss_(), SH_SC, SC_COLS);
  Logger.log('Đã cài lịch tự động: cảnh báo mỗi giờ, bản tin sáng 7 giờ, sao lưu 1 giờ sáng.');
  Logger.log('Bước tiếp theo: Triển khai thành ứng dụng web (nếu chưa), rồi chạy hàm chuoiKetNoi để lấy chuỗi dán vào SSR Điều Hành.');
  try { chuoiKetNoi(); } catch (e) { }
}

function onOpen() {
  SpreadsheetApp.getUi().createMenu('SSR Điều Hành')
    .addItem('Cập nhật bảng từ dữ liệu mới nhất', 'capNhatBang')
    .addItem('Gửi cảnh báo ngay', 'guiCanhBao')
    .addItem('Gửi bản tin sáng ngay', 'banTinSang')
    .addItem('Sao lưu dữ liệu ngay', 'saoLuu')
    .addSeparator()
    .addItem('Kiểm tra hệ thống', 'kiemTra')
    .addItem('Xem khóa truy cập', 'xemKhoa')
    .addToUi();
}
function ui_() { try { return SpreadsheetApp.getUi(); } catch (e) { return null; } }
function xemKhoa() { const p = P_(), u = ui_(), m = 'Khóa quản trị: ' + p.getProperty('ADMIN_KEY') + '\nKhóa xem: ' + p.getProperty('VIEW_KEY') + '\nMã hiện trường cho bảo vệ, kỹ thuật: ' + p.getProperty('GUARD_PIN') + '\n\nChỉ đưa khóa quản trị cho người được sửa dữ liệu.'; if (u) u.alert('Khóa truy cập', m, u.ButtonSet.OK); else Logger.log(m); }
function emails_(names) { const p = P_(); return names.map(n => p.getProperty(n) || '').join(',').split(/[,;\s]+/).filter(x => /@/.test(x)).filter((x, i, a) => a.indexOf(x) === i).join(','); }
function loadData_() { const id = P_().getProperty('DATA_FILE_ID'); if (!id) return null; try { return JSON.parse(DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8')); } catch (e) { return null; } }
function T_(s) { if (!s) return NaN; s = String(s); return new Date(s.length === 10 ? s + 'T00:00:00+07:00' : s.length === 16 ? s + ':00+07:00' : s).getTime(); }
function dur_(ms) { const m = Math.abs(ms) / 6e4; if (m < 60) return Math.max(1, Math.round(m)) + ' phút'; const h = m / 60; if (h < 24) return (Math.round(h * 10) / 10).toString().replace('.', ',') + ' giờ'; const d = Math.floor(h / 24), r = Math.round(h - d * 24); return d + ' ngày' + (r ? ' ' + r + ' giờ' : ''); }
function money_(n) { return Math.round(+n || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' đ'; }
function esc_(v) { return String(v == null ? '' : v).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

/** Tính cảnh báo trên máy chủ theo đúng công thức của công cụ, để vẫn leo thang khi không ai mở công cụ. */
function alarms_(S) {
  const now = Date.now(), H = 36e5, D = 864e5, out = [], lv = s => s >= 1 ? 3 : s >= .5 ? 2 : 1, sla = (S && S.settings && S.settings.sla) || {};
  if (S) {
    (S.tickets || []).forEach(r => { if (r.status === 'Hoàn thành' || r.status === 'Đã hủy') return; const dl = T_(r.deadline); if (isNaN(dl) || now <= dl) return;
      out.push({ lv: lv((now - dl) / ((sla[r.priority] || 72) * H) + (BONUS_[r.priority] || 0)), mod: 'Phản ánh', code: r.code, title: r.title, what: 'Quá hạn xử lý', late: now - dl, who: r.owner, loc: r.location }); });
    (S.tasks || []).forEach(r => { if (r.status === 'Hoàn thành' || r.status === 'Tạm hoãn') return; const dl = T_(r.deadline); if (isNaN(dl) || now <= dl) return;
      out.push({ lv: lv((now - dl) / ((TOL_[r.frequency] || 3) * D) + (BONUS_[r.priority] || 0)), mod: 'Bảo trì', code: r.code, title: r.title, what: 'Bảo trì quá hạn', late: now - dl, who: r.owner, loc: r.location }); });
    (S.assets || []).forEach(r => { const nc = T_(r.nextCheck), crit = r.type === 'Thang máy' || r.type === 'PCCC';
      if (!isNaN(nc) && now > nc + D) { const d = (now - nc) / D; out.push({ lv: d > 30 ? 3 : d > 7 ? (crit ? 3 : 2) : (crit ? 2 : 1), mod: 'Thiết bị', code: r.code, title: r.name, what: 'Quá hạn kiểm tra', late: now - nc, who: r.owner, loc: r.location }); }
      if (r.status === 'Ngưng hoạt động') out.push({ lv: crit ? 3 : 2, mod: 'Thiết bị', code: r.code + '-NG', title: r.name, what: 'Thiết bị ngưng hoạt động', who: r.owner, loc: r.location }); });
    (S.contracts || []).forEach(r => { if (r.status === 'Đã kết thúc') return; const e = T_(r.end); if (isNaN(e)) return; const d = (e - now) / D;
      if (d <= 30) out.push({ lv: d < 0 ? 3 : d <= 7 ? 2 : 1, mod: 'Hợp đồng', code: r.code, title: r.vendor, what: d < 0 ? 'Hợp đồng đã hết hạn' : 'Còn ' + Math.ceil(d) + ' ngày hết hạn', late: d < 0 ? now - e : 0, who: r.owner, loc: r.service }); });
    (S.visits || []).forEach(v => { if (!v.outAt && now - T_(v.inAt) > 12 * H) out.push({ lv: now - T_(v.inAt) > 24 * H ? 2 : 1, mod: 'Ra vào', code: v.code, title: v.kind + ': ' + v.name, what: 'Khách chưa ghi nhận ra', late: now - T_(v.inAt), who: 'Bảo vệ ca trực', loc: v.gate }); });
  }
  rows_().forEach(r => { if (str_(r[K.status]) !== 'Đã gửi') return; const age = now - T_(str_(r[K.t]));
    if (age > 2 * H) out.push({ lv: age > 12 * H ? 2 : 1, mod: 'Tin cư dân', code: str_(r[K.id]), title: str_(r[K.content]).slice(0, 90), what: 'Tin cư dân chưa được đọc', late: age, who: 'Lễ tân và chăm sóc cư dân', loc: str_(r[K.unit]) }); });
  return out.sort((a, b) => b.lv - a.lv || (b.late || 0) - (a.late || 0));
}
const MAIL_CSS_ = 'body{font-family:"Times New Roman",Times,serif;color:#111;font-size:14px}h2{color:#063B28;font-size:18px;margin:0 0 6px}h3{background:#E3EEE7;color:#063B28;font-size:15px;padding:5px 8px;margin:16px 0 6px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #C9D3CC;padding:4px 7px;text-align:left;vertical-align:top}th{background:#F2F6F3}.nd{background:#EEF5F0;border-left:3pt solid #0B6E47;padding:7px 10px;margin:8px 0}.nd div{margin:2px 0}.bad{color:#A93434;font-weight:bold}.ok{color:#1E7A46}.ft{color:#666;font-size:12px;margin-top:14px}';
function alarmTable_(list) { return '<table><tr><th>Mức</th><th>Phân hệ</th><th>Mã</th><th>Nội dung</th><th>Tình trạng</th><th>Phụ trách</th></tr>' + list.map(a => '<tr><td' + (a.lv === 3 ? ' class="bad"' : '') + '>' + LVN_[a.lv] + '</td><td>' + esc_(a.mod) + '</td><td>' + esc_(a.code) + '</td><td>' + esc_(a.title) + (a.loc ? '<br><small>' + esc_(a.loc) + '</small>' : '') + '</td><td>' + esc_(a.what) + (a.late ? ', quá ' + dur_(a.late) : '') + '</td><td>' + esc_(a.who || '') + '</td></tr>').join('') + '</table>'; }

/** Chạy mỗi giờ: gửi email khi có việc mới lên mức Cảnh báo hoặc Khẩn cấp, hoặc tăng mức. Mỗi việc chỉ báo một lần ở mỗi mức. */
function guiCanhBao() {
  const to = emails_(['NOTIFY_EMAIL']); const al = alarms_(loadData_());
  const prev = JSON.parse(P_().getProperty('NOTIFIED') || '{}'), cur = {}, news = [];
  al.forEach(a => { if (a.lv < 2) return; cur[a.code] = a.lv; if (!prev[a.code] || prev[a.code] < a.lv) news.push(a); });
  let js = JSON.stringify(cur); if (js.length > 8500) js = JSON.stringify(Object.fromEntries(Object.entries(cur).filter(e => e[1] === 3).slice(0, 300)));
  P_().setProperty('NOTIFIED', js);
  if (!news.length || !to) return { ok: true, sent: 0 };
  const n3 = news.filter(a => a.lv === 3).length;
  const html = '<style>' + MAIL_CSS_ + '</style><h2>Cảnh báo mới tại Saigon South Residences</h2><div class="nd">' + (n3 ? '<div><b>' + n3 + ' việc ở mức khẩn cấp</b> cần xử lý ngay.</div>' : '') + '<div>Tổng ' + news.length + ' việc vừa lên mức cảnh báo hoặc tăng mức so với lần báo trước.</div><div>Cảnh báo chỉ hết khi việc được hoàn thành trong công cụ quản lý.</div></div>' + alarmTable_(news) + '<p class="ft">Email tự động từ hệ thống quản lý Saigon South Residences, kiểm tra mỗi giờ.</p>';
  MailApp.sendEmail({ to: to, subject: '[SSR Điều Hành] ' + (n3 ? n3 + ' việc khẩn cấp, ' : '') + news.length + ' cảnh báo mới', htmlBody: html });
  log_('Hệ thống', 'Gửi cảnh báo', news.length + ' cảnh báo tới ' + to);
  return { ok: true, sent: news.length };
}

/** Chạy 7 giờ sáng: bản tin tình hình gửi Ban Quản lý và Ban Quản trị, kèm file PDF. */
function banTinSang() {
  const to = emails_(['NOTIFY_EMAIL', 'BQT_EMAILS']); if (!to) return { ok: false, error: 'Chưa khai báo NOTIFY_EMAIL' };
  const S = loadData_(), al = alarms_(S), now = Date.now(), td = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd');
  const c = l => al.filter(a => a.lv === l).length;
  const openTk = S ? (S.tickets || []).filter(t => t.status !== 'Hoàn thành' && t.status !== 'Đã hủy') : [];
  const lateTk = openTk.filter(t => T_(t.deadline) < now).length;
  const unread = rows_().filter(r => str_(r[K.status]) === 'Đã gửi').length;
  const bk = S ? (S.bookings || []).filter(b => b.date === td && b.status !== 'Đã hủy') : [];
  const debt6 = S ? (S.units || []).filter(u => (+u.debtMonths || 0) >= 6).length : 0;
  const tasksToday = S ? (S.tasks || []).filter(t => t.status !== 'Hoàn thành' && t.status !== 'Tạm hoãn' && String(t.plannedAt).slice(0, 10) <= td) : [];
  const nd = [c(3) ? '<b>' + c(3) + ' việc khẩn cấp</b> cần xử lý đầu giờ sáng nay.' : 'Không có việc ở mức khẩn cấp.',
    openTk.length + ' phản ánh đang mở, trong đó ' + lateTk + ' việc đã quá hạn.',
    unread ? unread + ' tin nhắn cư dân chưa được đọc.' : 'Mọi tin nhắn cư dân đã được đọc.',
    tasksToday.length + ' việc bảo trì đến hạn hoặc đang dở dang; ' + bk.length + ' lượt đặt tiện ích trong ngày.',
    (function () { if (!S) return ''; const L = outagesLive_(S), a = L.filter(o => o.status === 'Đang diễn ra').length, u = L.filter(o => o.status === 'Sắp diễn ra' && T_(o.planStart) - now < 48 * 36e5).length; return a || u ? [a ? a + ' gián đoạn dịch vụ đang diễn ra' : '', u ? u + ' lần ngưng dịch vụ sắp diễn ra trong 48 giờ' : ''].filter(Boolean).join('; ') + '.' : ''; })(),
    debt6 ? debt6 + ' căn nợ phí từ 6 tháng, cần thống nhất biện pháp theo quy chế.' : ''].filter(Boolean);
  const hk = hookSrv_(S);
  const body = '<h2>Bản tin sáng ' + Utilities.formatDate(new Date(), TZ, 'dd/MM/yyyy') + '</h2>' + hookHtml_(hk, 'Số liệu và việc cần xử lý trong ngày ở các mục dưới đây.') + '<p>Ban Quản lý chung cư Saigon South Residences, Phú Mỹ Hưng</p>' +
    '<h3>Tóm tắt</h3><table><tr><th>Chỉ tiêu</th><th>Số lượng</th></tr><tr><td>Cảnh báo khẩn cấp</td><td class="' + (c(3) ? 'bad' : 'ok') + '">' + c(3) + '</td></tr><tr><td>Cảnh báo</td><td>' + c(2) + '</td></tr><tr><td>Nhắc việc</td><td>' + c(1) + '</td></tr><tr><td>Phản ánh đang mở</td><td>' + openTk.length + '</td></tr><tr><td>Phản ánh quá hạn</td><td>' + lateTk + '</td></tr><tr><td>Tin cư dân chưa đọc</td><td>' + unread + '</td></tr><tr><td>Đặt chỗ tiện ích hôm nay</td><td>' + bk.length + '</td></tr></table>' +
    '<div class="nd"><b>Nhận định</b>' + nd.map(x => '<div>' + x + '</div>').join('') + '</div>' +
    (al.filter(a => a.lv >= 2).length ? '<h3>Việc cần xử lý</h3>' + alarmTable_(al.filter(a => a.lv >= 2).slice(0, 40)) : '') +
    (tasksToday.length ? '<h3>Bảo trì trong ngày</h3><table><tr><th>Mã</th><th>Công việc</th><th>Đơn vị thực hiện</th><th>Hạn</th></tr>' + tasksToday.slice(0, 30).map(t => '<tr><td>' + esc_(t.code) + '</td><td>' + esc_(t.title) + '</td><td>' + esc_(t.executor) + '</td><td>' + esc_(String(t.deadline).replace('T', ' ')) + '</td></tr>').join('') + '</table>' : '') +
    (bk.length ? '<h3>Đặt chỗ tiện ích hôm nay</h3><table><tr><th>Giờ</th><th>Tiện ích</th><th>Căn hộ</th><th>Trạng thái</th></tr>' + bk.map(b => '<tr><td>' + esc_(b.start + ' đến ' + b.end) + '</td><td>' + esc_(b.facility) + '</td><td>' + esc_(b.unit) + '</td><td>' + esc_(b.status) + '</td></tr>').join('') + '</table>' : '') +
    '<p class="ft">Số liệu theo lần đồng bộ gần nhất từ công cụ quản lý' + (P_().getProperty('DATA_AT') ? ', lúc ' + String(P_().getProperty('DATA_AT')).replace('T', ' ').slice(0, 16) : '') + '.</p>';
  const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><style>' + MAIL_CSS_ + '</style></head><body>' + body + '</body></html>';
  const pdf = Utilities.newBlob(html, 'text/html', 'bantin.html').getAs('application/pdf').setName('SSR-BanTinSang-' + td + '.pdf');
  MailApp.sendEmail({ to: to, subject: '[SSR] Bản tin sáng ' + Utilities.formatDate(new Date(), TZ, 'dd/MM') + (hk ? ': ' + hk.k : '') + (c(3) ? ', ' + c(3) + ' việc khẩn cấp' : ''), htmlBody: html, attachments: [pdf] });
  log_('Hệ thống', 'Gửi bản tin sáng', to);
  return { ok: true };
}

/** Chạy 1 giờ sáng: chép file dữ liệu vào thư mục "SSR sao luu", giữ 30 ngày gần nhất. */
function saoLuu() {
  const id = P_().getProperty('DATA_FILE_ID'); if (!id) return { ok: false, error: 'Chưa có dữ liệu để sao lưu' };
  const parents = DriveApp.getFileById(ss_().getId()).getParents(), root = parents.hasNext() ? parents.next() : DriveApp.getRootFolder();
  const it = root.getFoldersByName('SSRDH sao luu'), folder = it.hasNext() ? it.next() : root.createFolder('SSRDH sao luu');
  DriveApp.getFileById(id).makeCopy('SSRDH-du-lieu-' + Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd'), folder);
  const cut = Date.now() - 30 * 864e5, files = folder.getFiles(); let del = 0;
  while (files.hasNext()) { const f = files.next(); if (f.getDateCreated().getTime() < cut) { f.setTrashed(true); del++; } }
  log_('Hệ thống', 'Sao lưu', 'Đã sao lưu, xóa ' + del + ' bản cũ hơn 30 ngày');
  return { ok: true };
}

/* ----- bảng tính đọc được: công cụ gửi bảng đã định dạng, máy chủ ghi vào các sheet ----- */
function sheets_(b) {
  const tables = Array.isArray(b.tables) ? b.tables.slice(0, 40) : []; if (!tables.length) throw new Error('Thiếu dữ liệu bảng');
  const p = P_(), js = JSON.stringify(tables); let id = p.getProperty('MIRROR_FILE_ID');
  if (id) DriveApp.getFileById(id).setContent(js);
  else { const f = DriveApp.createFile('SSRDH-bang-tinh.json', js, MimeType.PLAIN_TEXT); id = f.getId(); p.setProperty('MIRROR_FILE_ID', id); const par = DriveApp.getFileById(ss_().getId()).getParents(); if (par.hasNext()) f.moveTo(par.next()); }
  const n = writeMirror_(tables); p.setProperty('MIRROR_AT', stamp_()); p.setProperty('MIRROR_BY', clean_(b.who || '', 80));
  return { ok: true, n: n, at: p.getProperty('MIRROR_AT') };
}
function capNhatBang() {
  const id = P_().getProperty('MIRROR_FILE_ID'), u = ui_();
  if (!id) { if (u) u.alert('Chưa có dữ liệu bảng. Mở công cụ quản lý ở chế độ quản trị và bấm "Cập nhật Google Sheets ngay".'); return; }
  const n = writeMirror_(JSON.parse(DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8')));
  if (u) u.alert('Đã cập nhật ' + n + ' bảng.');
}
function writeMirror_(tables) {
  const ss = ss_(); let n = 0;
  tables.forEach(t => {
    const name = clean_(t.name, 60).replace(/^'/, ''); if (!name || [SH_MSG, SH_NT, SH_LOG].indexOf(name) >= 0) return;
    const rows = Array.isArray(t.rows) ? t.rows : []; const w = rows.reduce((m, r) => Math.max(m, (r || []).length), 1);
    const vals = rows.map(r => { const a = (r || []).map(v => typeof v === 'number' ? v : clean_(v, 3000)); while (a.length < w) a.push(''); return a; });
    let sh = ss.getSheetByName(name); if (!sh) sh = ss.insertSheet(name);
    sh.clearContents();
    if (vals.length) {
      sh.getRange(1, 1, vals.length, w).setValues(vals);
      sh.getRange(1, 1, 1, w).setFontWeight('bold').setBackground('#E3EEE7');
      sh.setFrozenRows(1);
    }
    if (!sh.getProtections(SpreadsheetApp.ProtectionType.SHEET).length) {
      const pr = sh.protect().setDescription(MIRROR_NOTE); pr.removeEditors(pr.getEditors()); if (pr.canDomainEdit()) pr.setDomainEdit(false);
    }
    if (name === 'Tổng quan') chartOverview_(sh, vals);
    n++;
  });
  return n;
}
function chartOverview_(sh, vals) {
  sh.getCharts().forEach(c => sh.removeChart(c));
  const r = vals.findIndex(x => x[0] === 'Tháng'); if (r < 0) return;
  let end = r + 1; while (end < vals.length && vals[end][0]) end++;
  sh.insertChart(sh.newChart().setChartType(Charts.ChartType.COLUMN).addRange(sh.getRange(r + 1, 1, end - r, 3)).setNumHeaders(1)
    .setPosition(2, 5, 0, 0).setOption('title', 'Thu chi quỹ vận hành 12 tháng').setOption('colors', ['#128157', '#C9A24A']).setOption('legend', { position: 'bottom' }).build());
}

/** Tự kiểm tra sau khi cài: ghi, đọc, đánh dấu đã đọc, phản hồi một tin thử rồi xóa; kiểm tra Drive, lịch tự động, email. */
function kiemTra() {
  const res = [], ok = (c, m) => res.push((c ? 'ĐẠT   ' : 'LỖI   ') + m);
  const p = P_(); ok(!!p.getProperty('ADMIN_KEY') && !!p.getProperty('VIEW_KEY'), 'Đã có khóa quản trị và khóa xem');
  ok(!!ss_().getSheetByName(SH_MSG) && !!ss_().getSheetByName(SH_NT), 'Đã có sheet TinNhan và BangTin');
  try {
    const s = route_('send', { type: 'Khác', content: 'Tin kiểm tra hệ thống, sẽ tự xóa', unit: 'A-02.01', pub: false, _test: true });
    ok(s.ok, 'Gửi tin thử từ cổng cư dân' + (s.ok ? '' : ': ' + s.error));
    if (s.ok) {
      const ak = p.getProperty('ADMIN_KEY');
      ok(route_('read', { key: ak, ids: [s.id], who: 'Kiểm tra' }).n === 1, 'Đánh dấu đã đọc');
      ok(route_('reply', { key: ak, id: s.id, text: 'Phản hồi thử', who: 'Kiểm tra' }).ok, 'Phản hồi tin');
      const m = route_('mine', { tracks: [s.track] }).items[0]; ok(m && m.status === 'Đã phản hồi' && m.readAt, 'Cư dân thấy dấu đã đọc và phản hồi');
      const f = findRow_(s.id); if (f) sheet_().deleteRow(f.i); ok(!findRow_(s.id), 'Xóa tin thử');
      CacheService.getScriptCache().remove('rl_A-02.01');
    }
  } catch (e) { ok(false, 'Luồng tin nhắn: ' + e.message); }
  try { const f = DriveApp.createFile('ssr-kiem-tra.txt', 'ok'); f.setTrashed(true); ok(true, 'Ghi được file vào Google Drive'); } catch (e) { ok(false, 'Ghi file Drive: ' + e.message); }
  ok(!!p.getProperty('GUARD_PIN'), 'Đã có mã hiện trường cho bảo vệ, kỹ thuật');
  ok([SH_BK, SH_GU, SH_FD, SH_PH].every(n => !!ss_().getSheetByName(n)), 'Đã có sheet DatCho, KhachDangKy, HienTruong, Anh (chạy caiDat nếu thiếu)');
  ['Portal', 'Field'].forEach(fn => { try { page_(fn); ok(true, 'Có trang ' + fn); } catch (e) { ok(false, 'Không dựng được trang ' + fn + ': ' + e.message); } });
  const I = idx_(); ok(!!(I && I.m.salt), 'Dữ liệu đã đồng bộ có mã tra cứu căn hộ' + (I ? '' : ', chưa đồng bộ lần nào'));
  const tr = ScriptApp.getProjectTriggers().map(t => t.getHandlerFunction());
  ok(['guiCanhBao', 'banTinSang', 'saoLuu'].every(h => tr.indexOf(h) >= 0), 'Lịch tự động (chạy hàm caiDat nếu thiếu)');
  ok(!!emails_(['NOTIFY_EMAIL']), 'Email nhận cảnh báo NOTIFY_EMAIL' + (emails_(['NOTIFY_EMAIL']) ? ': ' + emails_(['NOTIFY_EMAIL']) : ' chưa khai báo'));
  let url = ''; try { url = ScriptApp.getService().getUrl() || ''; } catch (e) { }
  ok(!!url, 'Đã triển khai ứng dụng web' + (url ? ': ' + url : ', vào Triển khai để tạo'));
  try { res.push('THÔNG TIN hạn mức email còn lại hôm nay: ' + MailApp.getRemainingDailyQuota()); } catch (e) { }
  res.push('THÔNG TIN dữ liệu đồng bộ: phiên bản ' + (p.getProperty('DATA_VERSION') || 0) + (p.getProperty('DATA_AT') ? ', lúc ' + p.getProperty('DATA_AT') : ', chưa có'));
  const txt = res.join('\n'); Logger.log(txt); const u = ui_(); if (u) u.alert('Kết quả kiểm tra hệ thống', txt, u.ButtonSet.OK);
  return res;
}

/* =====================================================================
 * Phiên bản 3: đặt tiện ích, tra cứu phí, đăng ký khách trước (cư dân);
 * tuần tra, kiểm tra thiết bị, chỉ số công tơ, ảnh hiện trường (bảo vệ, kỹ thuật).
 * ===================================================================== */
const SH_BK = 'DatCho', SH_GU = 'KhachDangKy', SH_FD = 'HienTruong', SH_PH = 'Anh';
const BK_COLS = ['Mã yêu cầu', 'Thời điểm', 'Căn hộ', 'Họ tên', 'Điện thoại', 'Tiện ích', 'Ngày', 'Từ', 'Đến', 'Số người', 'Ghi chú', 'Trạng thái', 'Mã đặt chỗ', 'Lý do', 'Cập nhật'];
const GU_COLS = ['Mã khách', 'Thời điểm tạo', 'Căn hộ', 'Loại', 'Tên khách', 'Biển số', 'Ngày', 'Từ giờ', 'Đến giờ', 'Giờ vào', 'Cổng vào', 'Bảo vệ', 'Giờ ra', 'Ghi chú'];
const FD_COLS = ['Số', 'Thời điểm', 'Loại', 'Mã', 'Người ghi', 'Kết quả', 'Giá trị', 'Ghi chú', 'Ảnh'];
const PH_COLS = ['Thời điểm', 'Mã liên quan', 'Loại ảnh', 'Người gửi', 'Mã tệp', 'Ảnh thu nhỏ'];
const GUEST_KINDS = ['Khách thăm', 'Giao hàng lớn', 'Thợ sửa chữa', 'Chuyển đồ'];
const FIELD_TYPES = ['Kiểm tra thiết bị', 'Tuần tra', 'Chỉ số công tơ'];
const BANKS_ = { '970436': 'Vietcombank', '970415': 'VietinBank', '970418': 'BIDV', '970405': 'Agribank', '970407': 'Techcombank', '970422': 'MB', '970416': 'ACB', '970432': 'VPBank', '970403': 'Sacombank', '970437': 'HDBank', '970423': 'TPBank', '970441': 'VIB', '970443': 'SHB', '970431': 'Eximbank', '970448': 'OCB', '970426': 'MSB', '970440': 'SeABank', '970449': 'LPBank', '970428': 'Nam A Bank', '970409': 'Bac A Bank' };
const ALPH_ = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

function setupV3_() {
  const ss = ss_(); ensure_(ss, SH_BK, BK_COLS); ensure_(ss, SH_GU, GU_COLS); ensure_(ss, SH_FD, FD_COLS); ensure_(ss, SH_PH, PH_COLS);
  const p = P_(); if (!p.getProperty('GUARD_PIN')) p.setProperty('GUARD_PIN', String(Math.floor(100000 + Math.random() * 900000)));
  Logger.log('Mã hiện trường (bảo vệ, kỹ thuật nhập một lần trên điện thoại): ' + p.getProperty('GUARD_PIN'));
}
function today_() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd'); }
function addDays_(d, n) { return Utilities.formatDate(new Date(T_(d) + n * 864e5), TZ, 'yyyy-MM-dd'); }
function nowHM_() { return Utilities.formatDate(new Date(), TZ, 'HH:mm'); }
function cyrb_(str) { let h1 = 0xdeadbeef, h2 = 0x41c6ce57; for (let i = 0; i < str.length; i++) { const c = str.charCodeAt(i); h1 = Math.imul(h1 ^ c, 2654435761); h2 = Math.imul(h2 ^ c, 1597334677); } h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909); h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909); return (h2 >>> 0).toString(16).padStart(8, '0') + (h1 >>> 0).toString(16).padStart(8, '0'); }
function unitSecret_(salt, code) { const h = cyrb_('SSRU|' + salt + '|' + code); let s = ''; for (let i = 0; i < 6; i++) s += ALPH_.charAt(parseInt(h.substr(i * 2, 2), 16) % 32); return s; }
function tlv_(id, v) { return id + String(v.length).padStart(2, '0') + v; }
function crc16_(s) { let c = 0xFFFF; for (let i = 0; i < s.length; i++) { c ^= s.charCodeAt(i) << 8; for (let j = 0; j < 8; j++) c = (c & 0x8000) ? ((c << 1) ^ 0x1021) & 0xFFFF : (c << 1) & 0xFFFF; } return c.toString(16).toUpperCase().padStart(4, '0'); }
function vietqr_(bin, acc, amount, info) { const mai = tlv_('00', 'A000000727') + tlv_('01', tlv_('00', bin) + tlv_('01', acc)) + tlv_('02', 'QRIBFTTA'); let s = tlv_('00', '01') + tlv_('01', amount ? '12' : '11') + tlv_('38', mai) + tlv_('53', '704') + (amount ? tlv_('54', String(Math.round(amount))) : '') + tlv_('58', 'VN') + (info ? tlv_('62', tlv_('08', info)) : ''); s += '6304'; return s + crc16_(s); }

/** Chỉ mục gọn đọc từ file dữ liệu chung, lưu tạm 6 giờ, xóa mỗi lần đồng bộ. */
function idx_() {
  const c = CacheService.getScriptCache(), m = c.get('idxM'), u = c.get('idxU'); if (m && u) return { m: JSON.parse(m), u: JSON.parse(u) };
  const S = loadData_(); if (!S) return null; const st = S.settings || {}, park = {};
  (S.vehicles || []).forEach(v => { if (v.status === 'Đang sử dụng') park[v.unit] = (park[v.unit] || 0) + (+v.fee || 0); });
  const U = {}; (S.units || []).forEach(x => { U[x.code] = [+x.area || 0, +x.debt || 0, +x.debtMonths || 0, park[x.code] || 0]; });
  const td = today_(), lim = addDays_(td, 45);
  const M = { feeRate: +st.feeRate || 0, bank: st.bank || {}, dueDay: st.dueDay || 15, salt: st.unitSalt || '', hotline: st.hotline || '',
    fac: (S.facilities || []).filter(f => f.bookable === 'Có').map(f => ({ id: f.id, name: f.name, zone: f.zone, hours: f.hours, fee: +f.fee || 0, status: f.status })),
    busy: (S.bookings || []).filter(b => b.status !== 'Đã hủy' && b.date >= td && b.date <= lim).map(b => [b.facility, b.date, b.start, b.end]), assets: {}, cps: {}, meters: {} };
  (S.assets || []).forEach(a => M.assets[a.code] = [a.name, a.location, a.status]);
  (S.checkpoints || []).forEach(a => M.cps[a.code] = [a.name, a.location]);
  (S.meters || []).forEach(a => M.meters[a.code] = [a.name, a.uom, a.location]);
  try { c.put('idxM', JSON.stringify(M), 21600); c.put('idxU', JSON.stringify(U), 21600); } catch (e) { }
  return { m: M, u: U };
}
function verifyUnit_(b) {
  const unit = String(b.unit || '').trim().toUpperCase(), code = String(b.code || '').trim().toUpperCase();
  if (!/^[ABCDEG]-\d{2}\.\d{2}$/.test(unit)) throw new Error('Căn hộ ghi theo dạng A-12.05');
  const cache = CacheService.getScriptCache(), fk = 'vu_' + unit, fails = +(cache.get(fk) || 0);
  if (fails >= 10) throw new Error('Nhập sai mã nhiều lần, vui lòng thử lại sau một giờ');
  const I = idx_(); if (!I || !I.m.salt) throw new Error('Hệ thống chưa sẵn sàng, Ban Quản lý chưa đồng bộ dữ liệu');
  if (!I.u[unit] || unitSecret_(I.m.salt, unit) !== code) { cache.put(fk, String(fails + 1), 3600); throw new Error('Căn hộ hoặc mã tra cứu chưa đúng. Mã tra cứu in trên giấy báo phí hằng tháng'); }
  return { unit: unit, I: I };
}
function needPin_(b) {
  if (role_(b) === 'admin') return; const p = P_().getProperty('GUARD_PIN'), cache = CacheService.getScriptCache(), n = +(cache.get('pinfail') || 0);
  if (n >= 30) throw new Error('Nhập sai mã quá nhiều lần, thử lại sau');
  if (!p || String(b.pin || '') !== p) { cache.put('pinfail', String(n + 1), 3600); throw new Error('Mã hiện trường không đúng'); }
}
function sheetRows_(name, cols) { const sh = ss_().getSheetByName(name); if (!sh) return []; const n = sh.getLastRow(); return n < 2 ? [] : sh.getRange(2, 1, n - 1, cols.length).getValues(); }
function obj_(cols, r, i) { const o = { _row: i + 2 }; cols.forEach((c, j) => o[c] = str_(r[j])); return o; }
function hmIn_(t, hours) { const m = String(hours || '').match(/(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})/); return !m || (t >= m[1] && t <= m[2]); }
function savePhoto_(ref, kind, who, data, thumb) {
  if (!data) return ''; data = String(data).replace(/^data:image\/\w+;base64,/, ''); if (data.length > 3000000) throw new Error('Ảnh quá lớn');
  const par = DriveApp.getFileById(ss_().getId()).getParents(), root = par.hasNext() ? par.next() : DriveApp.getRootFolder();
  const it = root.getFoldersByName('SSRDH anh hien truong'), folder = it.hasNext() ? it.next() : root.createFolder('SSRDH anh hien truong');
  const f = folder.createFile(Utilities.newBlob(Utilities.base64Decode(data), 'image/jpeg', clean_(ref, 30).replace(/'/g, '') + '-' + kind + '-' + stamp_().replace(/[:T]/g, '') + '.jpg'));
  ss_().getSheetByName(SH_PH).appendRow([stamp_(), clean_(ref, 30), kind, clean_(who, 80), f.getId(), String(thumb || '').slice(0, 45000)]);
  return f.getId();
}
const V3 = {
  portalInfo: b => { const I = idx_(); return { ok: true, fac: I ? I.m.fac.filter(f => f.status === 'Mở cửa') : [], hotline: I ? I.m.hotline : '' }; },
  slots: b => {
    const I = idx_(); if (!I) return { ok: true, busy: [] }; const f = I.m.fac.find(x => x.id === b.fac); if (!f) throw new Error('Không có tiện ích này');
    const busy = I.m.busy.filter(x => x[0] === f.name && x[1] === b.date).map(x => [x[2], x[3]]);
    sheetRows_(SH_BK, BK_COLS).forEach(r => { if (str_(r[5]) === f.name && str_(r[6]).slice(0, 10) === b.date && ['Chờ duyệt', 'Đã xác nhận'].indexOf(str_(r[11])) >= 0) busy.push([str_(r[7]), str_(r[8])]); });
    return { ok: true, busy: busy, hours: f.hours, fee: f.fee };
  },
  bookReq: b => {
    const v = verifyUnit_(b), f = v.I.m.fac.find(x => x.id === b.fac); if (!f || f.status !== 'Mở cửa') throw new Error('Tiện ích hiện không nhận đặt chỗ');
    const td = today_(), d = String(b.date || ''), s = String(b.start || ''), e = String(b.end || '');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d) || d < td || d > addDays_(td, 30)) throw new Error('Chỉ đặt trong vòng 30 ngày tới');
    if (!/^\d{2}:\d{2}$/.test(s) || !/^\d{2}:\d{2}$/.test(e) || e <= s) throw new Error('Giờ kết thúc phải sau giờ bắt đầu');
    if (!hmIn_(s, f.hours) || !hmIn_(e, f.hours)) throw new Error('Ngoài giờ mở cửa ' + f.hours);
    const busy = V3.slots({ fac: b.fac, date: d }).busy; if (busy.some(x => !(e <= x[0] || s >= x[1]))) throw new Error('Khung giờ này đã có người đặt');
    const mine = sheetRows_(SH_BK, BK_COLS).filter(r => str_(r[2]) === v.unit && str_(r[11]) === 'Chờ duyệt').length; if (mine >= 3) throw new Error('Căn hộ đang có 3 yêu cầu chờ duyệt');
    const id = 'YC-' + rnd_(6), lock = LockService.getScriptLock(); lock.waitLock(10000);
    try { ss_().getSheetByName(SH_BK).appendRow([id, stamp_(), v.unit, clean_(b.name, 80), text_(clean_(b.phone, 20)), f.name, "'" + d, "'" + s, "'" + e, +b.people || '', clean_(b.note, 300), 'Chờ duyệt', '', '', stamp_()]); } finally { lock.releaseLock(); }
    return { ok: true, id: id };
  },
  myBook: b => { const v = verifyUnit_(b); return { ok: true, items: sheetRows_(SH_BK, BK_COLS).map((r, i) => obj_(BK_COLS, r, i)).filter(o => o['Căn hộ'] === v.unit).reverse().slice(0, 20) }; },
  fee: b => {
    const v = verifyUnit_(b), x = v.I.u[v.unit], M = v.I.m, now = new Date(), mm = Utilities.formatDate(now, TZ, 'MM'), yy = Utilities.formatDate(now, TZ, 'yyyy');
    const fee = x[0] * M.feeRate, total = fee + x[3] + x[1], info = ('SSR ' + v.unit.replace(/[-.]/g, '') + ' T' + mm + yy);
    return { ok: true, unit: v.unit, area: x[0], rate: M.feeRate, fee: fee, park: x[3], debt: x[1], debtMonths: x[2], total: total, month: +mm + '/' + yy, due: String(Math.min(28, M.dueDay)).padStart(2, '0') + '/' + mm + '/' + yy,
      bank: M.bank.acc ? { name: BANKS_[M.bank.bin] || M.bank.bin, acc: M.bank.acc, holder: M.bank.name || '' } : null, info: info, qr: M.bank.acc && M.bank.bin && total > 0 ? vietqr_(M.bank.bin, M.bank.acc, total, info) : '' };
  },
  guestNew: b => {
    const v = verifyUnit_(b), td = today_(), d = String(b.date || ''), s = String(b.from || ''), e = String(b.to || '');
    if (GUEST_KINDS.indexOf(b.kind) < 0) throw new Error('Chọn loại khách'); if (clean_(b.name, 80).length < 2) throw new Error('Nhập tên khách');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d) || d < td || d > addDays_(td, 14)) throw new Error('Chỉ đăng ký trong vòng 14 ngày tới');
    if (!/^\d{2}:\d{2}$/.test(s) || !/^\d{2}:\d{2}$/.test(e) || e <= s) throw new Error('Giờ kết thúc phải sau giờ bắt đầu');
    if (sheetRows_(SH_GU, GU_COLS).filter(r => str_(r[2]) === v.unit && str_(r[6]).slice(0, 10) === d).length >= 10) throw new Error('Mỗi căn đăng ký tối đa 10 lượt khách một ngày');
    const id = 'KH-' + rnd_(6); ss_().getSheetByName(SH_GU).appendRow([id, stamp_(), v.unit, b.kind, clean_(b.name, 80), clean_(b.plate, 20), "'" + d, "'" + s, "'" + e, '', '', '', '', clean_(b.note, 200)]);
    let url = ''; try { url = ScriptApp.getService().getUrl() || ''; } catch (x) { }
    return { ok: true, code: id, link: url ? url + '?g=' + id : '' };
  },
  myGuests: b => { const v = verifyUnit_(b); return { ok: true, items: sheetRows_(SH_GU, GU_COLS).map((r, i) => obj_(GU_COLS, r, i)).filter(o => o['Căn hộ'] === v.unit).reverse().slice(0, 20) }; },
  fieldInfo: b => {
    needPin_(b); const I = idx_(), ref = String(b.ref || '').toUpperCase();
    if (b.type === 'g') { const r = sheetRows_(SH_GU, GU_COLS).map((x, i) => obj_(GU_COLS, x, i)).find(o => o['Mã khách'] === ref); if (!r) throw new Error('Không tìm thấy mã khách'); delete r._row; return { ok: true, guest: r, today: today_(), now: nowHM_() }; }
    const map = I ? (b.type === 'cp' ? I.m.cps : b.type === 'm' ? I.m.meters : I.m.assets) : {}; if (!map[ref]) throw new Error('Không tìm thấy mã ' + ref + ' trong dữ liệu đã đồng bộ');
    const last = sheetRows_(SH_FD, FD_COLS).filter(r => str_(r[3]) === ref).slice(-1)[0];
    return { ok: true, ref: ref, info: map[ref], last: last ? { t: str_(last[1]), who: str_(last[4]), result: str_(last[5]), value: str_(last[6]) } : null };
  },
  fieldlog: b => {
    needPin_(b); if (FIELD_TYPES.indexOf(b.type) < 0) throw new Error('Loại ghi nhận không hợp lệ');
    const ref = String(b.ref || '').toUpperCase(), who = clean_(b.who, 60); if (who.length < 2) throw new Error('Nhập tên người ghi nhận');
    if (b.type === 'Chỉ số công tơ' && !(+b.value >= 0)) throw new Error('Nhập chỉ số công tơ');
    const photo = b.photo ? savePhoto_(ref, 'Hiện trường', who, b.photo, b.thumb) : '';
    const sh = ss_().getSheetByName(SH_FD), lock = LockService.getScriptLock(); lock.waitLock(10000);
    try { const n = Math.max(0, sh.getLastRow() - 1) + 1; sh.appendRow([n, stamp_(), b.type, ref, who, clean_(b.result, 40), b.value === '' || b.value == null ? '' : +b.value, clean_(b.note, 500), photo]); } finally { lock.releaseLock(); }
    return { ok: true };
  },
  guestIn: b => { needPin_(b); return guestMark_(b, true); },
  guestOut: b => { needPin_(b); return guestMark_(b, false); },
  upload: b => { if (role_(b) !== 'admin') needPin_(b); return { ok: true, id: savePhoto_(b.ref, clean_(b.kind || 'Hiện trường', 30), b.who || 'Ban Quản lý', b.photo, b.thumb) }; },
  photos: b => { need_(b, 'view'); return { ok: true, items: sheetRows_(SH_PH, PH_COLS).filter(r => str_(r[1]) === String(b.ref)).map(r => ({ t: str_(r[0]), kind: str_(r[2]), who: str_(r[3]), id: str_(r[4]), thumb: str_(r[5]) })) }; },
  fieldlogs: b => { need_(b, 'view'); const since = +b.since || 0; return { ok: true, items: sheetRows_(SH_FD, FD_COLS).filter(r => +r[0] > since).map(r => ({ n: +r[0], t: str_(r[1]), type: str_(r[2]), ref: str_(r[3]), who: str_(r[4]), result: str_(r[5]), value: str_(r[6]), note: str_(r[7]), photo: str_(r[8]) })) }; },
  bookreqs: b => { need_(b, 'view'); return { ok: true, items: sheetRows_(SH_BK, BK_COLS).map((r, i) => obj_(BK_COLS, r, i)).slice(-300) }; },
  bookSet: b => {
    need_(b, 'admin'); if (['Đã xác nhận', 'Từ chối'].indexOf(b.status) < 0) throw new Error('Trạng thái không hợp lệ');
    const sh = ss_().getSheetByName(SH_BK), rows = sheetRows_(SH_BK, BK_COLS), i = rows.findIndex(r => str_(r[0]) === b.id); if (i < 0) throw new Error('Không tìm thấy yêu cầu');
    sh.getRange(i + 2, 12, 1, 4).setValues([[b.status, clean_(b.booking || '', 20), clean_(b.reason || '', 300), stamp_()]]); return { ok: true };
  },
  guests: b => { need_(b, 'view'); return { ok: true, items: sheetRows_(SH_GU, GU_COLS).map((r, i) => obj_(GU_COLS, r, i)).filter(o => o['Giờ vào']).slice(-500) }; }
};
function guestMark_(b, isIn) {
  const sh = ss_().getSheetByName(SH_GU), rows = sheetRows_(SH_GU, GU_COLS), ref = String(b.g || '').toUpperCase(), i = rows.findIndex(r => str_(r[0]) === ref);
  if (i < 0) throw new Error('Không tìm thấy mã khách'); const r = rows[i];
  if (isIn) {
    if (str_(r[9])) throw new Error('Mã này đã được dùng lúc ' + str_(r[9]).replace('T', ' ').slice(0, 16));
    if (str_(r[6]).slice(0, 10) !== today_()) throw new Error('Mã khách không phải cho hôm nay (' + str_(r[6]).slice(0, 10) + ')');
    const t = nowHM_(), from = str_(r[7]), to = str_(r[8]); if (t < addMin_(from, -60) || t > addMin_(to, 60)) throw new Error('Ngoài khung giờ đăng ký ' + from + ' đến ' + to);
    sh.getRange(i + 2, 10, 1, 3).setValues([[stamp_(), clean_(b.gate || 'Cổng 1', 30), clean_(b.who || '', 60)]]);
  } else { if (!str_(r[9])) throw new Error('Khách chưa được ghi nhận vào'); sh.getRange(i + 2, 13).setValue(stamp_()); }
  return { ok: true };
}
function addMin_(hm, n) { const p = String(hm).split(':'); let m = (+p[0]) * 60 + (+p[1]) + n; m = Math.max(0, Math.min(1439, m)); return String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'); }

/* =====================================================================
 * Phiên bản 4: giữ 60 phiên bản và khôi phục, báo cáo tuần qua email,
 * tình hình vận hành công khai, chấm điểm hài lòng, liên kết cho file Excel dữ liệu chung.
 * ===================================================================== */
const SH_RT = 'DanhGia', RT_COLS = ['Thời điểm', 'Mã tin', 'Mã theo dõi', 'Mã phản ánh', 'Số sao', 'Nhận xét'];
function vFolder_() { const par = DriveApp.getFileById(ss_().getId()).getParents(), root = par.hasNext() ? par.next() : DriveApp.getRootFolder(), it = root.getFoldersByName('SSRDH phien ban'); return it.hasNext() ? it.next() : root.createFolder('SSRDH phien ban'); }
function snapshot_(data, nv, who) {
  try { const f = vFolder_(); f.createFile('v' + String(nv).padStart(5, '0') + '_' + stamp_().replace(/[-:T]/g, '').slice(0, 12) + '_' + String(who).replace(/[^\w\u00C0-\u1EF9 ]/g, '').slice(0, 30) + '.json', data, MimeType.PLAIN_TEXT);
    const L = [], it = f.getFiles(); while (it.hasNext()) L.push(it.next()); L.sort((a, b) => a.getName() < b.getName() ? 1 : -1); L.slice(60).forEach(x => x.setTrashed(true)); } catch (e) { }
}
function csvCell_(v) { v = v == null ? '' : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
function csv_(p) {
  const pr = P_(), key = String(p.key || ''); if (!key || (key !== pr.getProperty('VIEW_KEY') && key !== pr.getProperty('ADMIN_KEY'))) return ContentService.createTextOutput('Khóa không đúng').setMimeType(ContentService.MimeType.TEXT);
  const id = pr.getProperty('XLSX_FILE_ID'); let T = {}; try { T = JSON.parse(DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8')); } catch (e) { }
  const rows = T[String(p.csv).toLowerCase()] || [[]];
  return ContentService.createTextOutput('\uFEFF' + rows.map(r => r.map(csvCell_).join(',')).join('\r\n')).setMimeType(ContentService.MimeType.CSV);
}
function ratingsMap_() { const m = {}; sheetRows_(SH_RT, RT_COLS).forEach(r => { m[str_(r[1])] = { stars: +r[4], note: str_(r[5]), t: str_(r[0]) }; }); return m; }
function tkStatus_() { const c = CacheService.getScriptCache(), v = c.get('tkst'); if (v) return JSON.parse(v); const S = loadData_(), m = {}; ((S && S.tickets) || []).forEach(t => { m[t.code] = [t.status, t.doneAt || '']; }); try { c.put('tkst', JSON.stringify(m), 600); } catch (e) { } return m; }
const mineBase_ = mine_;
mine_ = function (tracks) { const L = mineBase_(tracks), R = ratingsMap_(), TS = tkStatus_(); L.forEach(o => { const s = o.ticket && TS[o.ticket]; o.tkStatus = s ? s[0] : ''; o.tkDoneAt = s ? s[1] : ''; if (R[o.id]) o.rating = R[o.id]; }); return L; };
function stat_() {
  const c = CacheService.getScriptCache(), v = c.get('stat'); if (v) return JSON.parse(v);
  const S = loadData_(); if (!S) return { ok: true, empty: true }; const now = Date.now(), T = s => new Date(String(s || '').length === 16 ? s + ':00+07:00' : s).getTime();
  const openTk = (S.tickets || []).filter(t => t.status !== 'Hoàn thành' && t.status !== 'Đã hủy'), openTs = (S.tasks || []).filter(t => ['Kế hoạch', 'Đang thực hiện'].indexOf(t.status) >= 0 && T(t.plannedAt) <= now + 7 * 864e5 && t.frequency !== 'Hằng ngày');
  const loc = {}; openTk.forEach(t => { const o = loc[t.location] = loc[t.location] || { tk: 0, ts: 0, late: 0 }; o.tk++; if (T(t.deadline) < now) o.late++; }); openTs.forEach(t => { const o = loc[t.location] = loc[t.location] || { tk: 0, ts: 0, late: 0 }; o.ts++; if (T(t.deadline) < now) o.late++; });
  const done7 = (S.tickets || []).concat(S.tasks || []).filter(t => t.status === 'Hoàn thành' && now - T(t.doneAt) < 7 * 864e5).length, tk30 = (S.tickets || []).filter(t => t.status === 'Hoàn thành' && now - T(t.doneAt) < 30 * 864e5).length;
  const late = openTk.filter(t => T(t.deadline) < now).length + openTs.filter(t => T(t.deadline) < now).length;
  const o = { ok: true, at: P_().getProperty('DATA_AT') || '', open: openTk.length, late: late, done7: done7, tk30: tk30, loc: Object.keys(loc).map(k => [k, loc[k].tk, loc[k].ts, loc[k].late]).sort((a, b) => b[3] - a[3] || (b[1] + b[2]) - (a[1] + a[2])) };
  try { let lv = []; try { lv = outagesLive_(S).filter(x => x.status === 'Đang diễn ra'); } catch (e) { } const lo = o.loc[0], lc = s => { s = String(s || ''); return s ? s[0].toLowerCase() + s.slice(1) : s; };
    if (lv.length) { const x = lv[0], pe = x.planEnd ? T(x.planEnd) : NaN; o.hook = 'Đang ngưng ' + lc(x.service) + ' tại Block ' + x.blocks + (x.floors ? ', tầng ' + x.floors : '') + (isNaN(pe) ? '' : now > pe ? ', đã trễ so với giờ hẹn có lại ' + Utilities.formatDate(new Date(pe), TZ, 'HH:mm dd/MM') : ', giờ hẹn có lại ' + Utilities.formatDate(new Date(pe), TZ, 'HH:mm dd/MM')) + '.'; }
    else if (late && lo && lo[3]) o.hook = 'Ban Quản lý đã xử lý xong ' + tk30 + ' phản ánh trong 30 ngày qua, nhưng còn ' + late + ' việc đang quá hạn; nhiều nhất ở ' + lo[0] + ' với ' + lo[3] + ' việc.';
    else if (tk30) o.hook = tk30 + ' phản ánh được xử lý xong trong 30 ngày qua, hiện không có việc nào quá hạn.'; } catch (e) { }
  try { c.put('stat', JSON.stringify(o), 300); } catch (e) { } return o;
}
Object.assign(V3, {
  opstat: b => stat_(),
  rate: b => {
    const track = String(b.track || '').toUpperCase(), stars = Math.round(+b.stars); if (!/^[A-Z0-9]{6}$/.test(track) || !(stars >= 1 && stars <= 5)) throw new Error('Chọn từ 1 đến 5 sao');
    const r = rows_().find(x => str_(x[K.track]) === track); if (!r) throw new Error('Không tìm thấy lời nhắn');
    const tk = str_(r[K.ticket]), st = tkStatus_()[tk]; if (!tk || !st || st[0] !== 'Hoàn thành') throw new Error('Chỉ chấm điểm khi việc đã xử lý xong');
    const sh = ss_().getSheetByName(SH_RT) || ensure_(ss_(), SH_RT, RT_COLS), rows = sheetRows_(SH_RT, RT_COLS), i = rows.findIndex(x => str_(x[1]) === str_(r[K.id])), row = [stamp_(), str_(r[K.id]), track, tk, stars, clean_(b.comment, 300)];
    if (i >= 0) sh.getRange(i + 2, 1, 1, RT_COLS.length).setValues([row]); else sh.appendRow(row); return { ok: true };
  },
  ratings: b => { need_(b, 'view'); return { ok: true, items: sheetRows_(SH_RT, RT_COLS).map(r => ({ t: str_(r[0]), id: str_(r[1]), ticket: str_(r[3]), stars: +r[4], note: str_(r[5]) })) }; },
  xlsxPush: b => { need_(b, 'admin'); const s = String(b.tables || ''); if (s.length < 10 || s.length > 8e6) throw new Error('Dữ liệu Excel không hợp lệ'); const p = P_(); let id = p.getProperty('XLSX_FILE_ID'); try { if (id) DriveApp.getFileById(id).setContent(s); else id = null; } catch (e) { id = null; } if (!id) { const f = vFolder_().getParents().hasNext() ? vFolder_().getParents().next().createFile('SSRDH-excel.json', s, MimeType.PLAIN_TEXT) : DriveApp.createFile('SSRDH-excel.json', s, MimeType.PLAIN_TEXT); p.setProperty('XLSX_FILE_ID', f.getId()); } return { ok: true }; },
  viewKey: b => { need_(b, 'admin'); return { ok: true, key: P_().getProperty('VIEW_KEY') }; },
  versions: b => { need_(b, 'admin'); const L = [], it = vFolder_().getFiles(); while (it.hasNext()) { const f = it.next(), m = f.getName().match(/^v(\d+)_(\d{12})_(.*)\.json$/); if (m) L.push({ id: f.getId(), n: +m[1], at: m[2].replace(/(\d{4})(\d\d)(\d\d)(\d\d)(\d\d)/, '$1-$2-$3T$4:$5'), by: m[3] }); } return { ok: true, current: +(P_().getProperty('DATA_VERSION') || 0), items: L.sort((a, b) => b.n - a.n) }; },
  restore: b => {
    need_(b, 'admin'); const why = clean_(b.reason, 300); if (why.length < 3) throw new Error('Cần ghi lý do khôi phục');
    const data = DriveApp.getFileById(String(b.id)).getBlob().getDataAsString('UTF-8'); const o = JSON.parse(data); if (!o || o.app !== 'SSR-DH') throw new Error('Phiên bản không hợp lệ');
    const p = P_(), lk = LockService.getScriptLock(); lk.waitLock(20000);
    try { DriveApp.getFileById(p.getProperty('DATA_FILE_ID')).setContent(data); const nv = +(p.getProperty('DATA_VERSION') || 0) + 1, who = clean_(b.who || 'Ban Quản lý', 80);
      p.setProperty('DATA_VERSION', String(nv)); p.setProperty('DATA_BY', who + ' (khôi phục)'); p.setProperty('DATA_AT', stamp_()); CacheService.getScriptCache().removeAll(['idxM', 'idxU', 'stat', 'tkst']);
      log_(who, 'Khôi phục phiên bản', 'Về nội dung phiên bản ' + b.n + ', thành phiên bản ' + nv + '. Lý do: ' + why); snapshot_(data, nv, who + ' khoi phuc'); return { ok: true, version: nv }; } finally { lk.releaseLock(); }
  }
});
/** Sáng thứ Hai 7 giờ: gửi báo cáo tuần kèm PDF cho Ban Quản lý và Ban Quản trị. */
function baoCaoTuan() {
  const S = loadData_(); if (!S) return; const pr = P_(), to = [pr.getProperty('NOTIFY_EMAIL'), pr.getProperty('BQT_EMAILS')].filter(Boolean).join(','); if (!to) return;
  const now = Date.now(), T = s => new Date(String(s || '').length === 16 ? s + ':00+07:00' : s).getTime(), W = { 'Khẩn cấp': 2, 'Cao': 1, 'Trung bình': 0, 'Thấp': -1 }, LV = ['', 'Nhắc nhở', 'Cảnh báo', 'Báo động', 'Báo động đỏ'];
  const od = []; (S.tickets || []).concat(S.tasks || []).forEach(r => { if (['Hoàn thành', 'Đã hủy', 'Tạm hoãn'].indexOf(r.status) >= 0 || !(T(r.deadline) < now)) return; const h = (now - T(r.deadline)) / 36e5, base = h < 24 ? 1 : h < 72 ? 2 : h < 168 ? 3 : 4, isT = !!r.category; od.push({ lv: Math.max(1, Math.min(4, base + (isT || r.frequency === 'Một lần' ? (W[r.priority] || 0) : 0))), r: r, h: h }); });
  od.sort((a, b) => b.lv - a.lv || b.h - a.h); const done = (S.tickets || []).concat(S.tasks || []).filter(r => r.status === 'Hoàn thành' && now - T(r.doneAt) < 7 * 864e5);
  const td = (c, x) => '<td style="border:1px solid #CCD6CF;padding:5px 7px;font-size:12px' + (x || '') + '">' + String(c == null ? '' : c).replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</td>', th = a => '<tr>' + a.map(x => '<th style="background:#DCEBE2;color:#063B28;border:1px solid #CCD6CF;padding:5px 7px;font-size:12px;text-align:left">' + x + '</th>').join('') + '</tr>';
  const hkw = hookSrv_(S, true);
  const du = h => h >= 24 ? Math.floor(h / 24) + ' ngày ' + Math.round(h % 24) + ' giờ' : Math.round(h) + ' giờ';
  const html = '<div style="font-family:Times New Roman,serif;color:#111"><div style="background:#063B28;color:#F3E3A6;padding:12px 16px;font-size:18px"><b>Báo cáo vận hành tuần</b><br><span style="font-size:12px;color:#CFE3D6">Saigon South Residences, tuần kết thúc ' + Utilities.formatDate(new Date(), TZ, 'dd/MM/yyyy') + '</span></div>' + hookHtml_(hkw, 'Chi tiết theo từng mục bên dưới.') +
    '<p>' + od.length + ' việc quá hạn; ' + (S.tickets || []).filter(t => t.status !== 'Hoàn thành' && t.status !== 'Đã hủy').length + ' phản ánh đang mở; ' + done.length + ' việc hoàn thành trong 7 ngày.</p><h3 style="color:#063B28">1. Việc quá hạn</h3><table style="border-collapse:collapse;width:100%">' + th(['Mức', 'Việc', 'Vị trí', 'Phụ trách', 'Quá hạn']) + od.slice(0, 40).map(a => '<tr>' + td(LV[a.lv], a.lv >= 3 ? ';color:#A93434;font-weight:bold' : '') + td(a.r.title) + td(a.r.location) + td(a.r.owner) + td(du(a.h)) + '</tr>').join('') + '</table>' +
    '<h3 style="color:#063B28">2. Đã hoàn thành trong 7 ngày</h3><table style="border-collapse:collapse;width:100%">' + th(['Việc', 'Người thực hiện', 'Hoàn thành', 'Đánh giá']) + done.slice(0, 40).map(r => '<tr>' + td(r.title) + td(r.executor) + td(String(r.doneAt).replace('T', ' ')) + td(!r.deadline || T(r.doneAt) <= T(r.deadline) ? 'Đúng hạn' : 'Trễ hạn') + '</tr>').join('') + '</table>' + (function () { const L = outagesLive_(S).filter(o => o.status !== 'Đã hủy' && now - T(o.actualStart || o.planStart) < 7 * 864e5 && T(o.actualStart || o.planStart) <= now); return '<h3 style="color:#063B28">3. Gián đoạn dịch vụ trong tuần</h3><table style="border-collapse:collapse;width:100%">' + th(['Mã', 'Dịch vụ', 'Phạm vi', 'Thời gian', 'Đánh giá']) + (L.map(o => '<tr>' + td(o.code) + td(o.service + ', ' + String(o.kind).toLowerCase()) + td('Block ' + o.blocks + ', tầng ' + o.floors) + td(String(o.actualStart || o.planStart).replace('T', ' ') + (o.actualEnd ? ' đến ' + String(o.actualEnd).replace('T', ' ') : '')) + td(gdFlags_(o).join('; ') || 'Đúng cam kết', gdFlags_(o).some(x => /sớm|trễ|dưới/.test(x)) ? ';color:#A93434' : '') + '</tr>').join('') || '<tr>' + td('Không có gián đoạn') + td('') + td('') + td('') + td('') + '</tr>') + '</table>'; })() + '<p style="font-size:11px;color:#555">Thư gửi tự động từ máy chủ dữ liệu chung SSR Điều Hành. Không ghi tên hay căn hộ người phản ánh.</p></div>';
  const pdf = Utilities.newBlob(html, 'text/html', 'bao-cao-tuan.html').getAs('application/pdf').setName('SSR-BaoCaoTuan-' + Utilities.formatDate(new Date(), TZ, 'yyyyMMdd') + '.pdf');
  MailApp.sendEmail({ to: to, subject: '[SSR Điều Hành] Báo cáo vận hành tuần' + (hkw ? ': ' + hkw.k : ''), htmlBody: html, attachments: [pdf] });
}

/* ===== Phiên bản 6: tình trạng dịch vụ theo căn, khảo sát hài lòng hằng tháng ===== */
const SH_KS = 'KhaoSat', KS_COLS = ['Thời điểm', 'Căn hộ', 'Cấp nước', 'Vệ sinh', 'An ninh', 'Phản hồi của Ban Quản lý', 'Góp ý'];
Object.assign(V3, {
  svc: b => { const c = CacheService.getScriptCache(), v = c.get('svc'); if (v) return JSON.parse(v);
    const S = loadData_(), now = Date.now(), T = s => new Date(String(s || '').length === 16 ? s + ':00+07:00' : s).getTime();
    const items = ((S && S.outages) || []).filter(o => o.status === 'Đang diễn ra' || (o.status === 'Sắp diễn ra' && T(o.planStart) - now < 7 * 864e5) || (o.status === 'Đã khôi phục' && now - T(o.actualEnd) < 24 * 36e5))
      .map(o => ({ code: o.code, service: o.service, kind: o.kind, blocks: o.blocks, floors: o.floors, planStart: o.planStart || '', planEnd: o.planEnd || '', actualStart: o.actualStart || '', actualEnd: o.actualEnd || '', status: o.status, cause: String(o.cause || '').slice(0, 200) }));
    const r = { ok: true, at: P_().getProperty('DATA_AT') || '', items: items }; try { c.put('svc', JSON.stringify(r), 120); } catch (e) { } return r; },
  survey: b => { const s = (b.s || []).map(x => Math.round(+x)); if (s.length !== 4 || s.some(x => !(x >= 1 && x <= 5))) throw new Error('Chấm đủ 4 tiêu chí, từ 1 đến 5 sao');
    const unit = String(b.unit || '').toUpperCase().trim(); if (unit && !/^[ABCDEG]-\d{2}\.\d{2}$/.test(unit)) throw new Error('Mã căn hộ dạng A-12.05, hoặc để trống');
    const sh = ss_().getSheetByName(SH_KS) || ensure_(ss_(), SH_KS, KS_COLS), mk = stamp_().slice(0, 7);
    if (unit && sheetRows_(SH_KS, KS_COLS).some(r => str_(r[1]) === unit && str_(r[0]).slice(0, 7) === mk)) throw new Error('Căn hộ này đã góp ý trong tháng');
    sh.appendRow([stamp_(), unit].concat(s, [clean_(b.note, 300)])); return { ok: true }; },
  surveys: b => { need_(b, 'view'); return { ok: true, items: sheetRows_(SH_KS, KS_COLS).map(r => ({ t: str_(r[0]), s: [+r[2], +r[3], +r[4], +r[5]] })) }; }
});

/* ===== Phiên bản 7: sự cố từ hiện trường, cảnh báo và báo cáo máy chủ cho các sổ mới ===== */
const SH_SC = 'SuCoHienTruong', SC_COLS = ['Thời điểm', 'Mã sự cố', 'Hành động', 'Dịch vụ', 'Block', 'Tầng', 'Nguyên nhân', 'Người báo', 'Đã nhận', 'Mã tạm'];
function scEvents_() { return sheetRows_(SH_SC, SC_COLS).map((r, i) => ({ row: i + 2, t: str_(r[0]), code: str_(r[1]), act: str_(r[2]), service: str_(r[3]), blocks: str_(r[4]), floors: str_(r[5]), cause: str_(r[6]), who: str_(r[7]), ack: str_(r[8]), tmp: str_(r[9]) })); }
function outagesLive_(S) { const L = ((S && S.outages) || []).map(o => Object.assign({}, o));
  scEvents_().filter(e => e.ack !== 'Có').forEach(e => { if (e.act === 'new') L.push({ code: e.tmp, service: e.service, kind: 'Đột xuất', blocks: e.blocks, floors: e.floors, actualStart: e.t, status: 'Đang diễn ra', cause: e.cause, origin: 'Nội bộ tòa nhà' });
    else { const o = L.find(x => x.code === e.code); if (!o) return; if (e.act === 'start') { o.actualStart = e.t; o.status = 'Đang diễn ra'; } if (e.act === 'end') { o.actualEnd = e.t; o.status = 'Đã khôi phục'; } } });
  return L; }
function gdFlags_(o) { const f = [], ps = T_(o.planStart), pe = T_(o.planEnd), as = T_(o.actualStart), ae = T_(o.actualEnd), an = T_(o.announcedAt);
  if (o.kind === 'Đột xuất') f.push('Đột xuất'); else { if (!isNaN(an) && !isNaN(ps) && ps - an < 864e5) f.push('Báo trước dưới 24 giờ'); if (!isNaN(as) && !isNaN(ps) && as < ps - 3e5) f.push('Ngưng sớm ' + Math.round((ps - as) / 6e4) + ' phút'); }
  const end = !isNaN(ae) ? ae : (o.status === 'Đang diễn ra' ? Date.now() : NaN); if (!isNaN(pe) && !isNaN(end) && end > pe + 6e5) f.push('Có lại trễ ' + Math.round((end - pe) / 6e4) + ' phút'); return f; }
V3.svc = b => { const c = CacheService.getScriptCache(), v = c.get('svc'); if (v) return JSON.parse(v);
  const S = loadData_(), now = Date.now(), items = outagesLive_(S).filter(o => o.status === 'Đang diễn ra' || (o.status === 'Sắp diễn ra' && T_(o.planStart) - now < 7 * 864e5) || (o.status === 'Đã khôi phục' && now - T_(o.actualEnd) < 24 * 36e5))
    .map(o => ({ code: o.code, service: o.service, kind: o.kind, blocks: o.blocks, floors: o.floors, planStart: o.planStart || '', planEnd: o.planEnd || '', actualStart: o.actualStart || '', actualEnd: o.actualEnd || '', status: o.status, cause: String(o.cause || '').slice(0, 200) }));
  const r = { ok: true, at: P_().getProperty('DATA_AT') || '', items: items }; try { c.put('svc', JSON.stringify(r), 60); } catch (e) { } return r; };
Object.assign(V3, {
  fieldOutages: b => { needPin_(b); const now = Date.now(); return { ok: true, items: outagesLive_(loadData_()).filter(o => o.status === 'Đang diễn ra' || (o.status === 'Sắp diễn ra' && T_(o.planStart) - now < 2 * 864e5)).map(o => ({ code: o.code, service: o.service, kind: o.kind, blocks: o.blocks, floors: o.floors, planStart: o.planStart || '', planEnd: o.planEnd || '', actualStart: o.actualStart || '', status: o.status, cause: String(o.cause || '').slice(0, 160) })) }; },
  outageEvent: b => { needPin_(b); const act = String(b.act || ''); if (['start', 'end', 'new'].indexOf(act) < 0) throw new Error('Thao tác không hợp lệ');
    const who = clean_(b.who || 'Hiện trường', 60), sh = ss_().getSheetByName(SH_SC) || ensure_(ss_(), SH_SC, SC_COLS); let tmp = '';
    if (act === 'new') { if (['Nước', 'Điện', 'Thang máy', 'Cửa và thẻ', 'Khác'].indexOf(String(b.service)) < 0) throw new Error('Chọn dịch vụ'); if (!clean_(b.blocks, 40)) throw new Error('Ghi block bị ảnh hưởng'); tmp = 'HT-' + rnd_(5);
      sh.appendRow([stamp_(), '', 'new', b.service, clean_(b.blocks, 40), clean_(b.floors || 'Tất cả', 40), clean_(b.cause, 200), who, '', tmp]); }
    else { const code = clean_(b.code, 20); if (!code) throw new Error('Thiếu mã sự cố'); sh.appendRow([stamp_(), code, act, '', '', '', '', who, '', '']); }
    try { CacheService.getScriptCache().remove('svc'); } catch (e) { } log_(who, 'Hiện trường: ' + (act === 'new' ? 'báo sự cố mới' : act === 'start' ? 'bắt đầu ngưng' : 'đã có lại'), b.code || tmp); return { ok: true, tmp: tmp }; },
  outageEvents: b => { need_(b, 'admin'); return { ok: true, items: scEvents_().filter(e => e.ack !== 'Có') }; },
  outageAck: b => { need_(b, 'admin'); const sh = ss_().getSheetByName(SH_SC); if (!sh) return { ok: true }; (b.rows || []).forEach(r => { r = +r; if (r >= 2 && r <= sh.getLastRow()) sh.getRange(r, 9).setValue('Có'); }); try { CacheService.getScriptCache().remove('svc'); } catch (e) { } return { ok: true }; }
});
const alarmsBase_ = alarms_;
alarms_ = function (S) { const out = alarmsBase_(S); if (!S) return out; const now = Date.now(), H = 36e5, D = 864e5, dd = s => T_(String(s || '').length === 10 ? s + 'T00:00' : s);
  outagesLive_(S).forEach(o => { const sc = o.service + ' block ' + o.blocks + ', tầng ' + o.floors;
    if (o.status === 'Đang diễn ra') { const pe = T_(o.planEnd); if (!isNaN(pe) && now > pe + 6e5) out.push({ lv: now - pe > 3 * H ? 3 : 2, mod: 'Gián đoạn dịch vụ', code: o.code + '-TRE', title: sc, what: 'Chưa có lại, trễ ' + Math.round((now - pe) / 6e4) + ' phút so với giờ hẹn', late: now - pe, who: 'Trưởng bộ phận kỹ thuật', loc: 'Block ' + o.blocks });
      else if (o.kind === 'Đột xuất' && now - T_(o.actualStart) > 2 * H) out.push({ lv: 2, mod: 'Gián đoạn dịch vụ', code: o.code + '-DX', title: sc, what: 'Mất ' + String(o.service).toLowerCase() + ' đột xuất đã ' + Math.round((now - T_(o.actualStart)) / 6e4) + ' phút, chưa có giờ hẹn', late: now - T_(o.actualStart), who: 'Trưởng Ban Quản lý', loc: 'Block ' + o.blocks }); }
    if (o.status === 'Sắp diễn ra' && !o.announcedAt && T_(o.planStart) - now < 48 * H) out.push({ lv: 1, mod: 'Gián đoạn dịch vụ', code: o.code + '-TB', title: sc, what: 'Sắp ngưng nhưng chưa thông báo cư dân', who: 'Ban Quản lý', loc: 'Block ' + o.blocks }); });
  (S.letters || []).forEach(l => { if (l.status !== 'Chờ trả lời' || !l.dueAt) return; const d = (now - dd(l.dueAt)) / D; if (d > 1) out.push({ lv: d > 14 ? 2 : 1, mod: 'Công văn', code: l.code, title: l.party + ': ' + l.subject, what: 'Quá hạn trả lời ' + Math.floor(d) + ' ngày', late: d * D, who: 'Thư ký Ban Quản trị', loc: '' }); });
  (S.lifts || []).forEach(l => { const d = (dd(l.certEnd) - now) / D; if (d < 60) out.push({ lv: d < 0 ? 3 : 1, mod: 'Thang máy', code: l.code, title: l.name + ' block ' + l.block, what: d < 0 ? 'Đã hết hạn kiểm định' : 'Hết hạn kiểm định sau ' + Math.ceil(d) + ' ngày', who: 'Trưởng bộ phận kỹ thuật', loc: 'Block ' + l.block }); });
  (S.fires || []).forEach(f => { const d = (dd(f.nextDue) - now) / D; if (d < 30) out.push({ lv: d < 0 ? 2 : 1, mod: 'PCCC', code: f.code, title: f.kind, what: d < 0 ? 'Đã quá hạn' : 'Đến hạn sau ' + Math.ceil(d) + ' ngày', who: 'Đội PCCC cơ sở', loc: '' }); });
  (S.wtests || []).forEach(w => { if (w.result === 'Không đạt' && now - dd(w.date) < 60 * D) out.push({ lv: 3, mod: 'Chất lượng nước', code: w.code, title: w.place, what: 'Mẫu nước không đạt', who: 'Trưởng Ban Quản lý', loc: w.place }); });
  (S.permits || []).forEach(p => { if (p.status !== 'Chờ duyệt') return; const due = dd(p.submittedAt) + (p.change === 'Có' ? 14 : 7) * D; if (now > due + D) out.push({ lv: 1, mod: 'Thi công', code: p.code, title: 'Hồ sơ thi công căn ' + p.unit, what: 'Quá hạn duyệt', who: 'Ban Quản lý', loc: p.unit }); });
  const cnt = {}; outagesLive_(S).forEach(o => { if (o.asset && now - T_(o.actualStart || o.planStart) < 60 * D) cnt[o.asset] = (cnt[o.asset] || 0) + 1; }); (S.tickets || []).forEach(t => { if (t.asset && now - T_(t.createdAt) < 60 * D) cnt[t.asset] = (cnt[t.asset] || 0) + 1; });
  Object.keys(cnt).forEach(k => { if (cnt[k] >= 3) { const a = (S.assets || []).find(x => x.code === k) || {}; out.push({ lv: cnt[k] >= 5 ? 3 : 2, mod: 'Hỏng lặp lại', code: k + '-LL', title: a.name || k, what: 'Hỏng ' + cnt[k] + ' lần trong 60 ngày', who: 'Trưởng bộ phận kỹ thuật', loc: a.location || '' }); } });
  return out.sort((a, b) => b.lv - a.lv || (b.late || 0) - (a.late || 0)); };


/* ===== Phiên bản 9: câu móc mở đầu cho email báo cáo và cổng cư dân ===== */
function hookSrv_(S, noLive) {
  if (!S) return null; const now = Date.now(), C = [], T = s => new Date(String(s || '').length === 16 ? s + ':00+07:00' : s).getTime();
  const du = ms => { const h = ms / 36e5; return h >= 24 ? Math.floor(h / 24) + ' ngày' + (Math.round(h % 24) ? ' ' + Math.round(h % 24) + ' giờ' : '') : h >= 1 ? Math.round(h) + ' giờ' : Math.max(1, Math.round(h * 60)) + ' phút'; };
  const lc = s => { s = String(s || ''); return s ? s[0].toLowerCase() + s.slice(1) : s; };
  try { const L = outagesLive_(S).filter(o => o.status === 'Đang diễn ra' && o.planEnd && now > T(o.planEnd)); if (L.length) { const o = L[0]; C.push({ s: 88, live: 1, t: 'Đang ngưng ' + lc(o.service) + ' tại Block ' + o.blocks + (o.floors ? ', tầng ' + o.floors : '') + ', trễ ' + du(now - T(o.planEnd)) + ' so với giờ hẹn có lại.', k: 'ngưng ' + lc(o.service) + ' Block ' + o.blocks + ' trễ hẹn ' + du(now - T(o.planEnd)) }); } } catch (e) { }
  const openR = (S.tickets || []).concat(S.tasks || []).filter(r => ['Hoàn thành', 'Đã hủy', 'Tạm hoãn'].indexOf(r.status) < 0), late = openR.filter(r => r.deadline && T(r.deadline) < now);
  if (late.length >= 5) { const o = {}; late.forEach(r => { if (r.owner) o[r.owner] = (o[r.owner] || 0) + 1; }); const E = Object.keys(o).map(k => [k, o[k]]).sort((a, b) => b[1] - a[1]);
    if (E.length) { const sh = Math.round(E[0][1] / late.length * 100); if (sh >= 35) C.push({ s: 45 + sh / 2, t: 'Một người phụ trách đang giữ ' + E[0][1] + ' trên ' + late.length + ' việc quá hạn của cả Ban Quản lý, tức ' + sh + '%' + (sh > 50 ? '; gỡ được chỗ nghẽn này là gỡ hơn một nửa số việc trễ' : '') + '.', k: sh + '% việc trễ dồn vào một người' }); } }
  const tk = (S.tickets || []).filter(t => t.status !== 'Hoàn thành' && t.status !== 'Đã hủy'), tl = tk.filter(t => T(t.deadline) < now);
  if (tl.length) { const dn = (S.tickets || []).filter(t => t.status === 'Hoàn thành' && now - T(t.doneAt) < 30 * 864e5), on = dn.filter(t => T(t.doneAt) <= T(t.deadline)).length, old = Math.max.apply(null, tl.map(t => now - T(t.deadline)));
    C.push({ s: 35 + Math.min(40, tl.length * 2), t: (dn.length ? 'Trong 30 ngày qua, ' + Math.round(on / dn.length * 100) + '% phản ánh được xử lý đúng hạn, nhưng ' : '') + tl.length + ' trên ' + tk.length + ' phản ánh đang mở đã quá hạn, lâu nhất ' + du(old) + '.', k: tl.length + ' phản ánh quá hạn' }); }
  const U = (S.units || []).filter(u => +u.debt > 0); if (U.length >= 3) { const D = U.reduce((s, u) => s + +u.debt, 0), L3 = U.filter(u => +u.debtMonths >= 3), sh = Math.round(L3.reduce((s, u) => s + +u.debt, 0) / D * 100);
    if (L3.length && sh >= 40 && L3.length / U.length <= .5) C.push({ s: 50 + sh / 4, t: U.length + ' căn đang nợ phí, nhưng chỉ ' + L3.length + ' căn nợ từ 3 tháng trở lên đã chiếm ' + sh + '% tổng nợ.', k: L3.length + ' căn chiếm ' + sh + '% nợ phí' }); }
  const R = C.filter(x => !(noLive && x.live)).sort((a, b) => b.s - a.s); return R[0] || null;
}
function hookHtml_(h, sub) { return h ? '<div style="margin:10px 0 6px;padding:9px 13px;border-left:4px solid #B8892B;background:#F6F2E7;color:#063B28;font-weight:bold;font-size:15px;line-height:1.45">' + String(h.t).replace(/&/g, '&amp;').replace(/</g, '&lt;') + (sub ? '<div style="font-weight:normal;font-size:12px;color:#3A4A40;margin-top:3px">' + sub + '</div>' : '') + '</div>' : ''; }

/* ===== Cài đặt một tệp: trang cổng cư dân và trang hiện trường nằm sẵn trong mã, không cần tạo tệp HTML riêng ===== */
function page_(name) {
  let html = name === 'Field' ? PAGE_FIELD : PAGE_PORTAL;
  try { html = HtmlService.createHtmlOutputFromFile(name + '_rieng').getContent(); } catch (e) { }
  return HtmlService.createHtmlOutput(html);
}
/** Chạy sau khi đã Triển khai thành ứng dụng web: in và gửi email chuỗi kết nối, các đường dẫn cho cư dân và hiện trường. */
function chuoiKetNoi() {
  const pr = P_(), url = ScriptApp.getService().getUrl(), me = Session.getEffectiveUser().getEmail();
  if (!pr.getProperty('NOTIFY_EMAIL') && me) pr.setProperty('NOTIFY_EMAIL', me);
  if (!url) { Logger.log('Chưa triển khai ứng dụng web. Bấm Triển khai, Tùy chọn triển khai mới, Ứng dụng web, Người có quyền truy cập: Bất kỳ ai; rồi chạy lại hàm chuoiKetNoi.'); return; }
  const cs = 'SSRDH|' + url + '|' + pr.getProperty('ADMIN_KEY');
  Logger.log('CHUỖI KẾT NỐI (dán vào SSR Điều Hành, mục Dữ liệu chung): ' + cs);
  Logger.log('Cổng cư dân: ' + url); Logger.log('Trang hiện trường sự cố (bảo vệ, kỹ thuật): ' + url + '?sc=1'); Logger.log('Khóa xem: ' + pr.getProperty('VIEW_KEY') + '. Mã hiện trường: ' + pr.getProperty('GUARD_PIN'));
  if (me) MailApp.sendEmail({ to: me, subject: '[SSR Điều Hành] Thông tin kết nối dữ liệu chung',
    htmlBody: '<div style="font-family:Times New Roman,serif;font-size:14px"><p><b>Chuỗi kết nối</b> (dán nguyên dòng vào SSR Điều Hành, Cài đặt và dữ liệu, mục Dữ liệu chung qua Google Sheets, ô Địa chỉ web app, rồi bấm Lưu và kiểm tra):</p><p style="background:#EEF3EF;padding:10px;word-break:break-all"><code>' + cs + '</code></p>' +
      '<p><b>Cổng cư dân:</b> ' + url + '<br><b>Trang hiện trường sự cố:</b> ' + url + '?sc=1<br><b>Khóa xem</b> (Ban Quản trị, nhân viên chỉ xem): ' + pr.getProperty('VIEW_KEY') + '<br><b>Mã hiện trường</b> (bảo vệ, kỹ thuật): ' + pr.getProperty('GUARD_PIN') + '</p><p>Giữ thư này riêng tư: chuỗi kết nối chứa khóa quản trị.</p></div>' });
}
const PAGE_PORTAL = "<!DOCTYPE html>\n<html lang=\"vi\">\n<head>\n<base target=\"_top\">\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<link href=\"https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Cormorant+Garamond:wght@600;700&display=swap\" rel=\"stylesheet\">\n<style>\n:root{--bg:#F1F5F1;--sf:#fff;--ln:#DAE3DB;--ink:#14231B;--ink2:#3F5347;--ink3:#6A7C71;--em:#0B6E47;--em9:#063B28;--gold:#C9A24A;--g1:#F7EED0;--ok:#1E7A46;--okb:#E2F2E7;--warn:#A86F10;--warnb:#FBF0D8;--info:#2E6690;--infob:#E1ECF5}\n*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.55 \"Be Vietnam Pro\",\"Segoe UI\",Roboto,Arial,sans-serif}\nheader{background:radial-gradient(120% 90% at 0 0,#0E6242,#063B28 60%,#042C1E);color:#EAF3EE;padding:18px 16px 16px;border-bottom:1px solid rgba(201,162,74,.5)}\n.hb{display:flex;gap:12px;align-items:center;max-width:720px;margin:0 auto}.hb img{width:56px;height:56px}\n.hb b{display:block;font:700 22px/1.05 \"Cormorant Garamond\",Georgia,serif;color:#F3E3A6}.hb span{font-size:12.5px;color:#A9C6B3}\nnav{display:flex;gap:4px;max-width:720px;margin:14px auto 0;overflow-x:auto}\nnav button{border:0;background:rgba(255,255,255,.08);color:#D6E6DC;padding:8px 13px;border-radius:999px;font:inherit;font-size:13.5px;font-weight:500;white-space:nowrap;cursor:pointer}\nnav button.on{background:linear-gradient(135deg,#F4E6AE,#C9A24A);color:#33250A}\nmain{max-width:720px;margin:0 auto;padding:16px 14px 60px}\n.card{background:var(--sf);border:1px solid var(--ln);border-radius:16px;padding:16px;margin-bottom:12px}\nh2{font:700 24px/1.15 \"Cormorant Garamond\",Georgia,serif;color:var(--em9);margin:4px 0 10px}\nlabel{display:block;font-size:13px;font-weight:500;color:var(--ink2);margin:12px 0 5px}\ninput,select,textarea{width:100%;font:inherit;font-size:16px;border:1px solid var(--ln);border-radius:10px;padding:10px 12px;background:#fff;color:var(--ink)}\ntextarea{min-height:120px;resize:vertical}\n.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}\n.chk{display:flex;gap:10px;align-items:flex-start;margin-top:14px;font-size:13.5px;color:var(--ink2)}.chk input{width:20px;height:20px;flex:none;margin-top:1px}\n.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:12px;padding:12px 18px;font:inherit;font-weight:600;cursor:pointer;background:var(--em);color:#fff;width:100%;margin-top:16px}\n.btn.sec{background:#fff;color:var(--em);border:1px solid var(--ln);width:auto;margin-top:0;padding:9px 14px}\n.btn[disabled]{opacity:.6}\n.muted{color:var(--ink3);font-size:13px}.err{color:#B23A34;font-size:13.5px;margin-top:8px}\n.ok{background:var(--okb);border:1px solid #BFE2CB;border-radius:14px;padding:14px;margin-top:12px}\n.code{font:700 26px/1.1 \"Be Vietnam Pro\",sans-serif;letter-spacing:4px;color:var(--em9)}\n.msg{border:1px solid var(--ln);border-radius:14px;padding:13px 14px;margin-bottom:10px;background:#fff}\n.mh{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;color:var(--ink3);flex-wrap:wrap}\n.mc{margin:6px 0 8px;white-space:pre-line}\n.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600}\n.s-gui{background:var(--infob);color:var(--info)}.s-doc{background:var(--g1);color:#8A661B}.s-xl{background:var(--warnb);color:var(--warn)}.s-ph,.s-xong{background:var(--okb);color:var(--ok)}\n.steps{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}\n.st{display:flex;align-items:center;gap:5px;font-size:12px;color:var(--ink3)}.st i{width:10px;height:10px;border-radius:50%;border:2px solid var(--ln);display:inline-block}\n.st.on{color:var(--ink)}.st.on i{background:var(--em);border-color:var(--em)}\n.rp{background:var(--okb);border-radius:10px;padding:9px 12px;font-size:14px;margin-top:8px}\n.nt{border-left:3px solid var(--gold);background:linear-gradient(90deg,var(--g1),#fff 70%);border-radius:10px;padding:12px 14px;margin-bottom:10px}\n.nt b{display:block;margin:4px 0}.nt p{margin:0;white-space:pre-line;font-size:14px;color:var(--ink2)}\n.empty{text-align:center;color:var(--ink3);padding:26px 8px;font-size:14px}\n.add{display:flex;gap:8px;margin-top:10px}.add input{text-transform:uppercase}\nfooter{text-align:center;font-size:12px;color:var(--ink3);padding:10px}\n@media (max-width:480px){.row{grid-template-columns:1fr}}\n.tb{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px}.tb td,.tb th{border-bottom:1px solid var(--ln);padding:7px 4px;text-align:left}.tb td.n,.tb th.n{text-align:right}.tot td{font-weight:700}\n.qr{display:block;margin:12px auto;width:220px;height:220px;border:1px solid var(--ln);border-radius:12px;padding:8px;background:#fff}\n.slot{display:inline-block;background:var(--warnb);color:var(--warn);border-radius:8px;padding:3px 9px;margin:3px 4px 0 0;font-size:13px;font-weight:600}\n\n.stars{display:flex;gap:4px;margin:6px 0}.stars button{background:none;border:0;font-size:28px;color:#D9D2BD;cursor:pointer;padding:0 2px}.stars button.on{color:#C9A24A}\n.rcm{width:100%;border:1px solid var(--ln);border-radius:10px;padding:9px;font:inherit}\n.sgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.sb{border:1px solid var(--ln);border-radius:12px;padding:12px}.sb b{display:block;font-size:26px;font-family:Georgia,serif;color:#063B28}.sb.bad b{color:#B23A34}.sb span{font-size:13px;color:#6A7C71}\n.lrow{display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--ln);font-size:14px}.late{color:#B23A34}\n.hook{margin:4px 0 10px;padding:7px 0 7px 11px;border-left:3px solid #B8892B;color:#063B28;font-weight:600;font-size:16px;line-height:1.45}\n</style>\n<script src=\"https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js\"></script>\n</head>\n<body>\n<header><div class=\"hb\"><img src=\"data:image/webp;base64,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\" alt=\"Saigon South Residences\"><div><b>Saigon South Residences</b><span>Cổng cư dân, gửi tin cho Ban Quản lý</span></div></div>\n<nav><button data-t=\"send\" class=\"on\">Gửi tin</button><button data-t=\"mine\">Tin của tôi</button><button data-t=\"pub\">Bảng phản ánh chung</button><button data-t=\"book\">Đặt tiện ích</button><button data-t=\"fee\">Phí của tôi</button><button data-t=\"guest\">Khách đến thăm</button><button data-t=\"svc\">Tình trạng dịch vụ</button><button data-t=\"st\">Tình hình vận hành</button><button data-t=\"nt\">Thông báo</button></nav></header>\n<main id=\"m\"></main>\n<footer>Ban Quản lý chung cư Saigon South Residences, Phú Mỹ Hưng</footer>\n<script>\nvar TAB='send', LAST=null;\nfunction $(s){return document.querySelector(s)}\nfunction esc(v){return String(v==null?'':v).replace(/[&<>\"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]})}\nfunction fdt(s){if(!s)return'';var d=new Date(String(s).length===10?s+'T00:00':s);if(isNaN(d))return s;function p(n){return String(n).padStart(2,'0')}return p(d.getHours())+':'+p(d.getMinutes())+', '+p(d.getDate())+'/'+p(d.getMonth()+1)+'/'+d.getFullYear()}\nfunction tracks(){try{return JSON.parse(localStorage.getItem('ssr-tracks'))||[]}catch(e){return[]}}\nfunction saveTracks(a){try{localStorage.setItem('ssr-tracks',JSON.stringify(a.slice(0,30)))}catch(e){}}\nfunction call(p){return new Promise(function(res,rej){if(window.google&&google.script&&google.script.run){google.script.run.withSuccessHandler(res).withFailureHandler(function(e){rej(e)}).api(p)}else if(window.SSR_API){fetch(window.SSR_API,{method:'POST',body:JSON.stringify(p)}).then(function(r){return r.json()}).then(res,rej)}else rej(new Error('Chưa kết nối máy chủ'))})}\nvar SC={'Đã gửi':'s-gui','Đã đọc':'s-doc','Đang xử lý':'s-xl','Đã phản hồi':'s-ph','Đã xong':'s-xong'};\nfunction steps(m){var s=m.status,o=['Đã gửi','Đã đọc','Đang xử lý','Đã phản hồi','Đã xong'],i=o.indexOf(s);function on(k){return k<=i||(k===1&&m.readAt)||(k===3&&m.reply)}\nreturn '<div class=\"steps\">'+['Đã gửi',m.readAt?'Đã đọc '+fdt(m.readAt):'Chưa đọc','Đang xử lý','Đã phản hồi','Đã xong'].map(function(t,k){return '<span class=\"st'+(on(k)?' on':'')+'\"><i></i>'+esc(t)+'</span>'}).join('')+'</div>'}\nfunction card(m,mine){return '<div class=\"msg\"><div class=\"mh\"><span>'+esc(mine?(m.unit||'')+' '+m.id:(m.block||'Không ghi căn'))+'</span><span>'+esc(m.type)+', '+fdt(m.t)+'</span></div><div class=\"mc\">'+esc(m.content)+'</div><span class=\"pill '+(SC[m.status]||'')+'\">'+esc(m.status)+'</span>'+steps(m)+(m.reply?'<div class=\"rp\"><b>Ban Quản lý phản hồi</b> '+(m.replyAt?'<span class=\"muted\">('+fdt(m.replyAt)+')</span>':'')+'<br>'+esc(m.reply)+'</div>':'')+(mine&&m.ticket?rateBox(m):'')+'</div>'}\nfunction vSend(){return '<div class=\"card\"><h2>Gửi tin cho Ban Quản lý</h2><p class=\"muted\" style=\"margin-top:0\">Phản ánh sự cố, góp ý hoặc câu hỏi. Sau khi gửi, bạn theo dõi được tin đã được đọc, đang xử lý hay đã phản hồi.</p>'+\n'<label for=\"ty\">Loại tin</label><select id=\"ty\"><option>Phản ánh sự cố</option><option>Góp ý</option><option>Hỏi đáp</option><option>Khác</option></select>'+\n'<label for=\"ct\">Nội dung</label><textarea id=\"ct\" maxlength=\"2000\" placeholder=\"Mô tả sự việc, vị trí, thời gian nếu có\"></textarea>'+\n'<div class=\"row\"><div><label for=\"un\">Căn hộ</label><input id=\"un\" placeholder=\"Ví dụ A-12.05\" maxlength=\"8\" autocomplete=\"off\"></div><div><label for=\"ph\">Số điện thoại</label><input id=\"ph\" inputmode=\"tel\" maxlength=\"20\"></div></div>'+\n'<label for=\"nm\">Họ tên</label><input id=\"nm\" maxlength=\"80\" autocomplete=\"name\">'+\n'<label class=\"chk\"><input type=\"checkbox\" id=\"pb\" checked><span>Hiển thị trên bảng phản ánh chung để cư dân khác cùng theo dõi. Tên, số điện thoại và số căn được ẩn, chỉ hiện block.</span></label>'+\n'<label for=\"ph2\">Ảnh kèm theo (không bắt buộc)</label><input type=\"file\" id=\"ph2\" accept=\"image/*\"><p class=\"muted\" style=\"margin:10px 0 0\">Họ tên, căn hộ và số điện thoại chỉ dùng để Ban Quản lý liên hệ, xử lý và phản hồi tin của bạn.</p><button class=\"btn\" id=\"go\">Gửi tin</button><div class=\"err\" id=\"er\" hidden></div>'+(LAST?'<div class=\"ok\"><b>Đã gửi thành công.</b><br>Mã theo dõi của bạn<div class=\"code\">'+esc(LAST.track)+'</div><span class=\"muted\">Mã được lưu trên điện thoại này. Nếu đổi máy, nhập lại mã ở mục Tin của tôi.</span></div>':'')+'</div>'}\nfunction load(fn){$('#m').innerHTML='<div class=\"empty\">Đang tải</div>';fn().then(function(h){$('#m').innerHTML=h;bind()},function(e){$('#m').innerHTML='<div class=\"card\"><div class=\"err\">'+esc(e&&e.message||e)+'</div></div>'})}\nfunction show(){document.querySelectorAll('nav button').forEach(function(b){b.classList.toggle('on',b.dataset.t===TAB)});\nif(TAB==='book'||TAB==='fee'||TAB==='guest')return showUnit();\nif(TAB==='st')return showStatus();\nif(TAB==='svc')return showSvc();\nif(TAB==='send'){$('#m').innerHTML=vSend();bind();return}\nif(TAB==='mine')return load(function(){var t=tracks();if(!t.length)return Promise.resolve('<div class=\"card\"><h2>Tin của tôi</h2><div class=\"empty\">Chưa có tin nào trên điện thoại này.</div>'+addBox()+'</div>');return call({api:'mine',tracks:t}).then(function(r){if(!r.ok)throw new Error(r.error);return '<div class=\"card\"><h2>Tin của tôi</h2>'+(r.items.length?r.items.map(function(m){return card(m,true)}).join(''):'<div class=\"empty\">Không tìm thấy tin theo mã đã lưu.</div>')+addBox()+'</div>'})});\nif(TAB==='pub')return load(function(){return call({api:'public'}).then(function(r){if(!r.ok)throw new Error(r.error);return '<div class=\"card\"><h2>Bảng phản ánh chung</h2><p class=\"muted\" style=\"margin-top:0\">Các tin cư dân chọn công khai, kèm thời điểm Ban Quản lý đã đọc và phản hồi.</p>'+(r.items.length?r.items.map(function(m){return card(m,false)}).join(''):'<div class=\"empty\">Chưa có tin công khai.</div>')+'</div>'})});\nif(TAB==='nt')return load(function(){return call({api:'notices'}).then(function(r){if(!r.ok)throw new Error(r.error);return '<div class=\"card\"><h2>Thông báo của Ban Quản lý</h2>'+(r.items.length?r.items.map(function(n){return '<div class=\"nt\"><span class=\"muted\">'+esc(n.category)+', '+esc(n.scope)+'</span><b>'+esc(n.title)+'</b><p>'+esc(n.body)+'</p></div>'}).join(''):'<div class=\"empty\">Hiện không có thông báo.</div>')+'</div>'})})}\nfunction addBox(){return '<p class=\"muted\" style=\"margin:14px 0 0\">Nhập mã theo dõi nhận được khi gửi tin từ máy khác</p><div class=\"add\"><input id=\"tk\" maxlength=\"6\" placeholder=\"Mã 6 ký tự\"><button class=\"btn sec\" id=\"tka\">Thêm</button></div>'}\nfunction bind(){var g=$('#go');if(g)g.onclick=function(){var ct=$('#ct').value.trim(),er=$('#er');er.hidden=true;if(ct.length<5){er.textContent='Nội dung quá ngắn.';er.hidden=false;return}var un=$('#un').value.trim().toUpperCase();if(un&&!/^[ABCDEG]-\\d{2}\\.\\d{2}$/.test(un)){er.textContent='Căn hộ ghi theo dạng A-12.05.';er.hidden=false;return}\ng.disabled=true;g.textContent='Đang gửi';photoData($('#ph2')).then(function(ph){return call({api:'send',type:$('#ty').value,content:ct,unit:un,phone:$('#ph').value.trim(),name:$('#nm').value.trim(),pub:$('#pb').checked,photo:ph.photo,thumb:ph.thumb})}).then(function(r){if(!r.ok)throw new Error(r.error);var t=tracks();t.unshift(r.track);saveTracks(t);LAST=r;show()},function(e){g.disabled=false;g.textContent='Gửi tin';er.textContent=(e&&e.message)||'Không gửi được, thử lại sau';er.hidden=false})};\nvar a=$('#tka');if(a)a.onclick=function(){var v=$('#tk').value.trim().toUpperCase();if(!/^[A-Z0-9]{6}$/.test(v))return;var t=tracks();if(t.indexOf(v)<0)t.unshift(v);saveTracks(t);show()}}\n\nfunction resize(file,max,q){return new Promise(function(res){var img=new Image(),r=new FileReader();r.onload=function(){img.onload=function(){var s=Math.min(1,max/Math.max(img.width,img.height)),c=document.createElement('canvas');c.width=Math.round(img.width*s);c.height=Math.round(img.height*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);res(c.toDataURL('image/jpeg',q))};img.src=r.result};r.readAsDataURL(file)})}\nfunction photoData(inp){if(!inp||!inp.files||!inp.files[0])return Promise.resolve({});var f=inp.files[0],o={};return resize(f,1280,.8).then(function(d){o.photo=d;return resize(f,240,.6)}).then(function(t){o.thumb=t;return o})}\nfunction unitCfg(){try{return JSON.parse(localStorage.getItem('ssr-unit'))||null}catch(e){return null}}\nfunction money(n){return Math.round(+n||0).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.')+' đ'}\nfunction qrImg(v){try{return new QRious({value:v,size:440,level:'M'}).toDataURL()}catch(e){return''}}\nfunction vdate(s){s=String(s||'');return s.slice(8,10)+'/'+s.slice(5,7)+'/'+s.slice(0,4)}\nfunction todayStr(k){var d=new Date(Date.now()+(k||0)*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}\nfunction authBox(msg){return '<div class=\"card\"><h2>Xác nhận căn hộ</h2><p class=\"muted\" style=\"margin-top:0\">Nhập số căn và mã tra cứu in trên giấy báo phí hằng tháng. Mã chỉ cần nhập một lần trên điện thoại này.</p><div class=\"row\"><div><label for=\"au\">Căn hộ</label><input id=\"au\" placeholder=\"Ví dụ A-12.05\" maxlength=\"8\"></div><div><label for=\"ac\">Mã tra cứu</label><input id=\"ac\" maxlength=\"6\" style=\"text-transform:uppercase\"></div></div><button class=\"btn\" id=\"ao\">Xác nhận</button><div class=\"err\" id=\"er\"'+(msg?'':' hidden')+'>'+esc(msg||'')+'</div></div>'}\nfunction authView(msg){$('#m').innerHTML=authBox(msg);$('#ao').onclick=function(){var b=this,x={unit:$('#au').value.trim().toUpperCase(),code:$('#ac').value.trim().toUpperCase()};b.disabled=true;call(Object.assign({api:'fee'},x)).then(function(r){if(!r.ok)throw new Error(r.error);localStorage.setItem('ssr-unit',JSON.stringify(x));showUnit()}).catch(function(e){authView((e&&e.message)||e)})}}\nfunction showUnit(){var u=unitCfg();if(!u)return authView();\nvar head='<p class=\"muted\" style=\"margin:0 0 8px\">Căn hộ '+esc(u.unit)+'. <a href=\"#\" id=\"lo\">Đổi căn</a></p>';\nfunction fin(h){$('#m').innerHTML='<div class=\"card\">'+head+h+'</div>';var lo=$('#lo');if(lo)lo.onclick=function(){localStorage.removeItem('ssr-unit');showUnit();return false}}\nfunction err(e){var m=(e&&e.message)||e;if(/mã tra cứu|Căn hộ ghi/.test(m)){localStorage.removeItem('ssr-unit');authView(m);return}fin('<div class=\"err\">'+esc(m)+'</div>')}\n$('#m').innerHTML='<div class=\"empty\">Đang tải</div>';\nif(TAB==='fee')return call(Object.assign({api:'fee'},u)).then(function(r){if(!r.ok)throw new Error(r.error);var q=r.qr?qrImg(r.qr):'';\nfin('<h2>Phí tháng '+esc(r.month)+'</h2><table class=\"tb\"><tr><th>Khoản</th><th class=\"n\">Số tiền</th></tr><tr><td>Phí quản lý ('+r.area+' m² x '+money(r.rate).replace(' đ','')+')</td><td class=\"n\">'+money(r.fee)+'</td></tr>'+(r.park?'<tr><td>Phí gửi xe</td><td class=\"n\">'+money(r.park)+'</td></tr>':'')+(r.debt?'<tr><td>Nợ kỳ trước ('+r.debtMonths+' tháng)</td><td class=\"n\">'+money(r.debt)+'</td></tr>':'')+'<tr class=\"tot\"><td>Tổng phải thanh toán</td><td class=\"n\">'+money(r.total)+'</td></tr></table><p class=\"muted\">Hạn thanh toán '+esc(r.due)+'. Số liệu theo lần cập nhật gần nhất của Ban Quản lý; khoản vừa chuyển có thể chưa được ghi nhận.</p>'+\n(r.bank?(q?'<img class=\"qr\" src=\"'+q+'\" alt=\"Mã VietQR\"><p class=\"muted\" style=\"text-align:center\">Mở ứng dụng ngân hàng, quét mã. Số tiền và nội dung được điền sẵn.</p>':'')+'<table class=\"tb\"><tr><td>Ngân hàng</td><td class=\"n\">'+esc(r.bank.name)+'</td></tr><tr><td>Số tài khoản</td><td class=\"n\">'+esc(r.bank.acc)+'</td></tr>'+(r.bank.holder?'<tr><td>Chủ tài khoản</td><td class=\"n\">'+esc(r.bank.holder)+'</td></tr>':'')+'<tr><td>Nội dung</td><td class=\"n\"><b>'+esc(r.info)+'</b></td></tr></table>':'<p class=\"muted\">Ban Quản lý chưa công bố tài khoản nhận tiền trên cổng.</p>'))}).catch(err);\nif(TAB==='book')return Promise.all([call({api:'portalInfo'}),call(Object.assign({api:'myBook'},u))]).then(function(a){if(!a[0].ok)throw new Error(a[0].error);if(!a[1].ok)throw new Error(a[1].error);var fac=a[0].fac;\nfin('<h2>Đặt tiện ích</h2>'+(fac.length?'<label for=\"bf\">Tiện ích</label><select id=\"bf\">'+fac.map(function(f){return '<option value=\"'+f.id+'\">'+esc(f.name)+', '+esc(f.hours)+(f.fee?', '+money(f.fee)+' mỗi giờ':', miễn phí')+'</option>'}).join('')+'</select><label for=\"bd\">Ngày</label><input id=\"bd\" type=\"date\" min=\"'+todayStr()+'\" max=\"'+todayStr(30)+'\" value=\"'+todayStr()+'\"><div id=\"bs\" class=\"muted\" style=\"margin-top:8px\"></div><div class=\"row\"><div><label for=\"b1\">Từ giờ</label><input id=\"b1\" type=\"time\" value=\"18:00\"></div><div><label for=\"b2\">Đến giờ</label><input id=\"b2\" type=\"time\" value=\"19:00\"></div></div><div class=\"row\"><div><label for=\"bn\">Người đặt</label><input id=\"bn\" maxlength=\"80\"></div><div><label for=\"bp\">Số người</label><input id=\"bp\" type=\"number\" min=\"1\" value=\"2\"></div></div><label for=\"bt\">Ghi chú</label><input id=\"bt\" maxlength=\"300\"><button class=\"btn\" id=\"bo\">Gửi yêu cầu đặt chỗ</button><div class=\"err\" id=\"er\" hidden></div>':'<div class=\"empty\">Hiện chưa có tiện ích nhận đặt qua cổng.</div>')+\n'<h2 style=\"margin-top:22px\">Yêu cầu của căn hộ</h2>'+(a[1].items.length?a[1].items.map(function(o){return '<div class=\"msg\"><div class=\"mh\"><span>'+esc(o['Mã yêu cầu'])+'</span><span>'+esc(vdate(o['Ngày']))+', '+esc(o['Từ'])+' đến '+esc(o['Đến'])+'</span></div><div class=\"mc\">'+esc(o['Tiện ích'])+'</div><span class=\"pill '+(o['Trạng thái']==='Đã xác nhận'?'s-ph':o['Trạng thái']==='Từ chối'?'s-gui':'s-xl')+'\">'+esc(o['Trạng thái'])+'</span>'+(o['Lý do']?'<div class=\"rp\">'+esc(o['Lý do'])+'</div>':'')+'</div>'}).join(''):'<div class=\"empty\">Chưa có yêu cầu.</div>'));\nif(!fac.length)return;function slots(){call({api:'slots',fac:$('#bf').value,date:$('#bd').value}).then(function(r){$('#bs').innerHTML=r.ok?(r.busy.length?'Đã có người đặt: '+r.busy.map(function(x){return '<span class=\"slot\">'+esc(x[0])+' đến '+esc(x[1])+'</span>'}).join(''):'Chưa có ai đặt trong ngày này.'):esc(r.error)})}\n$('#bf').onchange=slots;$('#bd').onchange=slots;slots();\n$('#bo').onclick=function(){var b=this,er=$('#er');er.hidden=true;b.disabled=true;call(Object.assign({api:'bookReq',fac:$('#bf').value,date:$('#bd').value,start:$('#b1').value,end:$('#b2').value,name:$('#bn').value.trim(),people:$('#bp').value,note:$('#bt').value.trim()},u)).then(function(r){if(!r.ok)throw new Error(r.error);showUnit()}).catch(function(e){b.disabled=false;er.textContent=e.message||e;er.hidden=false})}}).catch(err);\nif(TAB==='guest')return call(Object.assign({api:'myGuests'},u)).then(function(r){if(!r.ok)throw new Error(r.error);\nfin('<h2>Đăng ký khách đến thăm</h2><p class=\"muted\" style=\"margin-top:0\">Gửi mã cho khách. Bảo vệ quét mã ở cổng là biết khách của căn nào, không phải gọi xác nhận.</p><label for=\"gk\">Loại khách</label><select id=\"gk\"><option>Khách thăm</option><option>Giao hàng lớn</option><option>Thợ sửa chữa</option><option>Chuyển đồ</option></select><div class=\"row\"><div><label for=\"gn\">Tên khách</label><input id=\"gn\" maxlength=\"80\"></div><div><label for=\"gp\">Biển số xe</label><input id=\"gp\" maxlength=\"20\"></div></div><label for=\"gd\">Ngày đến</label><input id=\"gd\" type=\"date\" min=\"'+todayStr()+'\" max=\"'+todayStr(14)+'\" value=\"'+todayStr()+'\"><div class=\"row\"><div><label for=\"g1\">Từ giờ</label><input id=\"g1\" type=\"time\" value=\"09:00\"></div><div><label for=\"g2\">Đến giờ</label><input id=\"g2\" type=\"time\" value=\"11:00\"></div></div><label for=\"gt\">Ghi chú cho bảo vệ</label><input id=\"gt\" maxlength=\"200\"><button class=\"btn\" id=\"go2\">Tạo mã khách</button><div class=\"err\" id=\"er\" hidden></div><div id=\"gr\"></div>'+\n'<h2 style=\"margin-top:22px\">Khách đã đăng ký</h2>'+(r.items.length?r.items.map(function(o){return '<div class=\"msg\"><div class=\"mh\"><span>'+esc(o['Mã khách'])+', '+esc(o['Loại'])+'</span><span>'+esc(vdate(o['Ngày']))+', '+esc(o['Từ giờ'])+' đến '+esc(o['Đến giờ'])+'</span></div><div class=\"mc\">'+esc(o['Tên khách'])+(o['Biển số']?', '+esc(o['Biển số']):'')+'</div><span class=\"pill '+(o['Giờ ra']?'s-xong':o['Giờ vào']?'s-ph':'s-gui')+'\">'+(o['Giờ ra']?'Đã ra':o['Giờ vào']?'Đã vào '+esc(fdt(o['Giờ vào'])):'Chưa đến')+'</span></div>'}).join(''):'<div class=\"empty\">Chưa có khách đăng ký.</div>'));\n$('#go2').onclick=function(){var b=this,er=$('#er');er.hidden=true;b.disabled=true;call(Object.assign({api:'guestNew',kind:$('#gk').value,name:$('#gn').value.trim(),plate:$('#gp').value.trim(),date:$('#gd').value,from:$('#g1').value,to:$('#g2').value,note:$('#gt').value.trim()},u)).then(function(x){if(!x.ok)throw new Error(x.error);b.disabled=false;var q=qrImg(x.link||x.code);$('#gr').innerHTML='<div class=\"ok\"><b>Mã khách</b><div class=\"code\">'+esc(x.code)+'</div>'+(q?'<img class=\"qr\" src=\"'+q+'\" alt=\"Mã QR khách\">':'')+'<span class=\"muted\">Chụp màn hình gửi khách. Bảo vệ quét mã để cho vào đúng khung giờ đã đăng ký.</span></div>'}).catch(function(e){b.disabled=false;er.textContent=e.message||e;er.hidden=false})}}).catch(err);}\n\nfunction rateBox(m){if(m.tkStatus!=='Hoàn thành')return m.tkStatus?'<div class=\"muted\" style=\"margin-top:6px\">Phản ánh '+esc(m.ticket)+': '+esc(m.tkStatus)+'</div>':'';\nif(m.rating)return '<div class=\"rp\" style=\"background:#EAF4EE;border-color:#1E7A46\"><b>Bạn đã đánh giá</b> <span style=\"color:#C9A24A;font-size:18px\">'+'★'.repeat(m.rating.stars)+'</span><span class=\"muted\">'+'★'.repeat(5-m.rating.stars)+'</span>'+(m.rating.note?'<br>'+esc(m.rating.note):'')+'</div>';\nreturn '<div class=\"rp\" data-rt=\"'+esc(m.track)+'\"><b>Ban Quản lý đã xử lý xong</b>'+(m.tkDoneAt?' <span class=\"muted\">('+fdt(m.tkDoneAt)+')</span>':'')+'<br>Bạn hài lòng với cách xử lý không?<div class=\"stars\">'+[1,2,3,4,5].map(function(i){return '<button type=\"button\" data-rs=\"'+i+'\">★</button>'}).join('')+'</div><input class=\"rcm\" maxlength=\"300\" placeholder=\"Nhận xét (không bắt buộc)\"><button class=\"btn\" data-rsend=\"1\" style=\"margin-top:8px\">Gửi đánh giá</button></div>'}\ndocument.addEventListener('click',function(e){var s=e.target.closest('[data-rs]');if(s){var box=s.closest('[data-rt]');box.dataset.v=s.dataset.rs;box.querySelectorAll('[data-rs]').forEach(function(b){b.classList.toggle('on',+b.dataset.rs<=+s.dataset.rs)});return}\nvar g=e.target.closest('[data-rsend]');if(g){var bx=g.closest('[data-rt]');if(!bx.dataset.v){alert('Chọn số sao trước');return}g.disabled=true;call({api:'rate',track:bx.dataset.rt,stars:+bx.dataset.v,comment:bx.querySelector('.rcm').value.trim()}).then(function(r){if(!r.ok)throw new Error(r.error);show()}).catch(function(x){g.disabled=false;alert(x.message||x)})}});\nfunction within(o,u){var m=/^([ABCDEG])-(\\d{2})\\.\\d{2}$/.exec(u);if(!m)return false;var b=m[1],f=+m[2],bs=String(o.blocks||'');if(!/toàn/i.test(bs)&&bs.toUpperCase().split(/[^A-Z]+/).indexOf(b)<0)return false;var fs=String(o.floors||'');if(/tất cả|toàn/i.test(fs)||!fs.trim())return true;return fs.split(/[,;]/).some(function(p){var r=/(\\d+)\\s*[-đến]+\\s*(\\d+)/.exec(p);if(r)return f>=+r[1]&&f<=+r[2];return parseInt(p,10)===f})}\nfunction svcCard(o){var cls=o.status==='Đang diễn ra'?'late':'',when=o.status==='Đã khôi phục'?'Đã có lại lúc '+fdt(o.actualEnd):o.status==='Đang diễn ra'?('Bắt đầu '+fdt(o.actualStart||o.planStart)+(o.planEnd?', dự kiến có lại '+fdt(o.planEnd):', đang xác định giờ có lại')):('Từ '+fdt(o.planStart)+' đến '+fdt(o.planEnd));\nreturn '<div class=\"card\"><div style=\"display:flex;justify-content:space-between;gap:8px\"><b>'+esc(o.service)+(o.kind==='Đột xuất'?' (sự cố)':'')+'</b><span class=\"'+cls+'\" style=\"font-weight:700\">'+esc(o.status)+'</span></div><div class=\"muted\" style=\"margin-top:4px\">Block '+esc(o.blocks)+', tầng '+esc(o.floors)+'</div><div style=\"margin-top:6px\">'+when+'</div>'+(o.cause?'<div class=\"muted\" style=\"margin-top:4px\">'+esc(o.cause)+'</div>':'')+'</div>'}\nfunction showSvc(){$('#m').innerHTML='<div class=\"empty\">Đang tải</div>';call({api:'svc'}).then(function(r){if(!r.ok)throw new Error(r.error);var u='';try{u=localStorage.getItem('ssr-unit')||''}catch(e){}\nfunction draw(){var mine=u?r.items.filter(function(o){return within(o,u)}):[];\n$('#m').innerHTML='<div class=\"card\"><h2>Tình trạng dịch vụ</h2><p class=\"muted\" style=\"margin-top:0\">Cắt nước, cắt điện, thang máy đang diễn ra, sắp diễn ra trong 7 ngày và vừa khôi phục trong 24 giờ. Cập nhật '+(r.at?fdt(r.at):'')+'.</p><label class=\"muted\">Mã căn hộ của bạn</label><div style=\"display:flex;gap:8px;margin-top:4px\"><input id=\"svu\" class=\"rcm\" placeholder=\"Ví dụ A-12.05\" value=\"'+esc(u)+'\"><button class=\"btn\" id=\"svb\" style=\"white-space:nowrap\">Kiểm tra</button></div>'+(u?'<div style=\"margin-top:12px;font-weight:700\">'+(mine.length?'Căn '+esc(u)+' đang hoặc sắp bị ảnh hưởng:':'Căn '+esc(u)+' hiện không bị ảnh hưởng.')+'</div>':'')+'</div>'+(u&&mine.length?mine.map(svcCard).join(''):'')+'<h2 style=\"font-size:18px;margin:16px 4px 8px\">Toàn khu</h2>'+(r.items.length?r.items.map(svcCard).join(''):'<div class=\"card empty\">Không có gián đoạn nào.</div>');\n$('#svb').onclick=function(){u=$('#svu').value.trim().toUpperCase();try{localStorage.setItem('ssr-unit',u)}catch(e){}draw()}}\ndraw()}).catch(function(e){$('#m').innerHTML='<div class=\"card\"><div class=\"err\">'+esc(e.message||e)+'</div></div>'})}\nfunction surveyBox(){var mk=new Date().toISOString().slice(0,7),done='';try{done=localStorage.getItem('ssr-survey-'+mk)}catch(e){}\nif(done)return '<div class=\"card\"><h2 style=\"font-size:18px\">Góp ý chất lượng dịch vụ</h2><p class=\"muted\">Cảm ơn bạn đã góp ý trong tháng này.</p></div>';\nvar C=['Cấp nước','Vệ sinh','An ninh','Phản hồi của Ban Quản lý'];return '<div class=\"card\" id=\"svy\"><h2 style=\"font-size:18px\">Góp ý chất lượng dịch vụ tháng này</h2><p class=\"muted\" style=\"margin-top:0\">Chấm từ 1 đến 5 sao cho từng mục. Ý kiến tổng hợp gửi Ban Quản trị, không công khai tên.</p>'+C.map(function(c,i){return '<div style=\"margin-top:8px\">'+c+'<div class=\"stars\" data-rt=\"q'+i+'\">'+[1,2,3,4,5].map(function(k){return '<button type=\"button\" data-rs=\"'+k+'\">★</button>'}).join('')+'</div></div>'}).join('')+'<input class=\"rcm\" id=\"svyu\" placeholder=\"Mã căn hộ (không bắt buộc)\" style=\"margin-top:8px\"><input class=\"rcm\" id=\"svyn\" maxlength=\"300\" placeholder=\"Góp ý thêm (không bắt buộc)\" style=\"margin-top:8px\"><button class=\"btn\" id=\"svys\" style=\"margin-top:10px\">Gửi góp ý</button></div>'}\ndocument.addEventListener('click',function(e){if(e.target.id!=='svys')return;var bx=document.getElementById('svy'),s=[0,1,2,3].map(function(i){var q=bx.querySelector('[data-rt=q'+i+']');return +(q.dataset.v||0)});if(s.some(function(x){return !x})){alert('Chấm đủ 4 mục');return}e.target.disabled=true;\ncall({api:'survey',s:s,unit:document.getElementById('svyu').value.trim(),note:document.getElementById('svyn').value.trim()}).then(function(r){if(!r.ok)throw new Error(r.error);try{localStorage.setItem('ssr-survey-'+new Date().toISOString().slice(0,7),'1')}catch(x){}show()}).catch(function(x){e.target.disabled=false;alert(x.message||x)})});\n\nfunction showStatus(){$('#m').innerHTML='<div class=\"empty\">Đang tải</div>';call({api:'opstat'}).then(function(r){if(!r.ok)throw new Error(r.error);if(r.empty){$('#m').innerHTML='<div class=\"card empty\">Ban Quản lý chưa đồng bộ dữ liệu.</div>';return}\n$('#m').innerHTML='<div class=\"card\"><h2>Tình hình vận hành</h2>'+(r.hook?'<p class=\"hook\">'+esc(r.hook)+'</p>':'')+'<p class=\"muted\" style=\"margin-top:0\">Cập nhật '+(r.at?fdt(r.at):'')+'. Không ghi tên hay căn hộ người phản ánh.</p><div class=\"sgrid\"><div class=\"sb\"><b>'+r.open+'</b><span>Phản ánh đang xử lý</span></div><div class=\"sb bad\"><b>'+r.late+'</b><span>Việc đang quá hạn</span></div><div class=\"sb\"><b>'+r.done7+'</b><span>Việc xong trong 7 ngày</span></div><div class=\"sb\"><b>'+r.tk30+'</b><span>Phản ánh xử lý xong trong 30 ngày</span></div></div><h2 style=\"margin-top:18px;font-size:18px\">Theo khu vực</h2>'+r.loc.map(function(x){var p=[];if(x[1])p.push(x[1]+' phản ánh');if(x[2])p.push(x[2]+' công việc');return '<div class=\"lrow\"><span>'+esc(x[0])+'</span><span>'+p.join(', ')+(x[3]?', <b class=\"late\">'+x[3]+' quá hạn</b>':'')+'</span></div>'}).join('')+'</div>'+surveyBox()}).catch(function(e){$('#m').innerHTML='<div class=\"card\"><div class=\"err\">'+esc(e.message||e)+'</div></div>'})}\n\ndocument.querySelectorAll('nav button').forEach(function(b){b.onclick=function(){TAB=b.dataset.t;if(TAB!=='send')LAST=null;show()}});\nsetInterval(function(){if(TAB==='mine'||TAB==='pub')show()},60000);\nshow();\n</script>\n</body>\n</html>\n";
const PAGE_FIELD = "<!DOCTYPE html>\n<html lang=\"vi\">\n<head>\n<base target=\"_top\">\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<style>\n:root{--bg:#F1F5F1;--ln:#DAE3DB;--ink:#14231B;--ink3:#6A7C71;--em:#0B6E47;--em9:#063B28;--gold:#C9A24A;--ok:#1E7A46;--okb:#E2F2E7;--bad:#B23A34;--badb:#F8E0DE;--warnb:#FBF0D8}\n*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.5 \"Segoe UI\",Roboto,Arial,sans-serif}\nheader{background:linear-gradient(160deg,#0E6242,#063B28);color:#F3E3A6;padding:14px 16px;font:700 19px Georgia,serif;border-bottom:2px solid var(--gold)}\nheader small{display:block;font:400 12.5px Arial,sans-serif;color:#A9C6B3;margin-top:2px}\nmain{max-width:560px;margin:0 auto;padding:14px}\n.card{background:#fff;border:1px solid var(--ln);border-radius:16px;padding:16px;margin-bottom:12px}\nh2{margin:0 0 4px;font:700 21px Georgia,serif;color:var(--em9)}.muted{color:var(--ink3);font-size:14px}\nlabel{display:block;font-size:14px;font-weight:600;margin:14px 0 6px}\ninput,select,textarea{width:100%;font:inherit;border:1px solid var(--ln);border-radius:12px;padding:12px;background:#fff}\ntextarea{min-height:80px}\n.btn{display:block;width:100%;border:0;border-radius:14px;padding:15px;font:inherit;font-weight:700;margin-top:16px;background:var(--em);color:#fff;cursor:pointer}\n.btn.sec{background:#fff;color:var(--em);border:1px solid var(--ln)}.btn.red{background:var(--bad)}.btn[disabled]{opacity:.55}\n.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:6px}.seg button{border:1px solid var(--ln);background:#fff;border-radius:12px;padding:12px 6px;font:inherit;font-size:14px;font-weight:600}\n.seg button.on{background:var(--em);color:#fff;border-color:var(--em)}.seg button.bad.on{background:var(--bad);border-color:var(--bad)}\n.ok{background:var(--okb);border-radius:14px;padding:16px;font-weight:600;color:var(--ok);text-align:center}\n.err{background:var(--badb);color:var(--bad);border-radius:12px;padding:12px;margin-top:12px;font-size:14.5px}\n.kv{display:grid;grid-template-columns:auto 1fr;gap:6px 12px;font-size:15px;margin-top:8px}.kv b{font-weight:600}\n.big{font-size:30px;font-weight:700;letter-spacing:2px;color:var(--em9)}\n.st{display:inline-block;padding:3px 12px;border-radius:999px;font-size:13px;font-weight:700;background:var(--warnb)}\n.st.in{background:var(--okb);color:var(--ok)}.st.out{background:#eee}\nimg.pv{max-width:100%;border-radius:12px;margin-top:10px}\n</style>\n</head>\n<body>\n<header>Saigon South Residences<small id=\"sub\">Ghi nhận hiện trường</small></header>\n<main id=\"m\"><div class=\"card muted\">Đang tải</div></main>\n<script>\nvar P={}, CFG=JSON.parse(localStorage.getItem('ssr-field')||'{}'), PHOTO=null, THUMB=null, RES='Bình thường';\nfunction $(s){return document.querySelector(s)}\nfunction esc(v){return String(v==null?'':v).replace(/[&<>\"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]})}\nfunction fdt(s){if(!s)return'';s=String(s);return s.slice(11,16)+', '+s.slice(8,10)+'/'+s.slice(5,7)}\nfunction call(p){p.pin=CFG.pin;return new Promise(function(res,rej){if(window.google&&google.script&&google.script.run)google.script.run.withSuccessHandler(res).withFailureHandler(rej).api(p);else if(window.SSR_API)fetch(window.SSR_API,{method:'POST',body:JSON.stringify(p)}).then(function(r){return r.json()}).then(res,rej);else rej(new Error('Chưa kết nối máy chủ'))})}\nfunction fail(e){var el=$('#er');var t=(e&&e.message)||e||'Có lỗi xảy ra';if(el){el.textContent=t;el.hidden=false}else $('#m').innerHTML='<div class=\"card\"><div class=\"err\">'+esc(t)+'</div><button class=\"btn sec\" onclick=\"resetCfg()\">Nhập lại mã hiện trường</button></div>'}\nfunction resetCfg(){CFG={};localStorage.removeItem('ssr-field');start()}\nfunction setup(){$('#m').innerHTML='<div class=\"card\"><h2>Mã hiện trường</h2><p class=\"muted\">Nhập một lần trên điện thoại này. Ban Quản lý cấp mã cho bảo vệ và kỹ thuật.</p><label>Mã hiện trường</label><input id=\"pin\" inputmode=\"numeric\" maxlength=\"8\"><label>Tên của bạn</label><input id=\"who\" maxlength=\"60\" value=\"'+esc(CFG.who||'')+'\"><button class=\"btn\" id=\"sv\">Lưu</button><div class=\"err\" id=\"er\" hidden></div></div>';\n$('#sv').onclick=function(){var pin=$('#pin').value.trim(),who=$('#who').value.trim();if(!pin||who.length<2){fail('Nhập đủ mã và tên');return}CFG={pin:pin,who:who};localStorage.setItem('ssr-field',JSON.stringify(CFG));start()}}\nfunction resize(file,max,q){return new Promise(function(res){var img=new Image(),r=new FileReader();r.onload=function(){img.onload=function(){var s=Math.min(1,max/Math.max(img.width,img.height)),c=document.createElement('canvas');c.width=Math.round(img.width*s);c.height=Math.round(img.height*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);res(c.toDataURL('image/jpeg',q))};img.src=r.result};r.readAsDataURL(file)})}\nfunction photoBox(){return '<label>Ảnh (không bắt buộc)</label><input type=\"file\" id=\"ph\" accept=\"image/*\" capture=\"environment\"><img id=\"pv\" class=\"pv\" hidden>'}\nfunction bindPhoto(){var f=$('#ph');if(!f)return;f.onchange=function(){if(!f.files[0])return;resize(f.files[0],1280,.8).then(function(d){PHOTO=d;$('#pv').src=d;$('#pv').hidden=false;return resize(f.files[0],240,.6)}).then(function(t){THUMB=t})}}\nfunction seg(opts){return '<div class=\"seg\">'+opts.map(function(o,i){return '<button type=\"button\" class=\"'+(o==='Hỏng'||o==='Bất thường'?'bad ':'')+(i===0?'on':'')+'\" data-r=\"'+o+'\">'+o+'</button>'}).join('')+'</div>'}\nfunction bindSeg(){document.querySelectorAll('.seg button').forEach(function(b){b.onclick=function(){document.querySelectorAll('.seg button').forEach(function(x){x.classList.toggle('on',x===b)});RES=b.dataset.r}})}\nfunction done(msg){$('#m').innerHTML='<div class=\"card\"><div class=\"ok\">'+esc(msg)+'</div><p class=\"muted\" style=\"text-align:center\">Người ghi: '+esc(CFG.who)+'. Có thể đóng trang này.</p></div>'}\nfunction outages(){$('#sub').textContent='Sự cố dịch vụ';$('#m').innerHTML='<div class=\"card muted\">Đang tải</div>';call({api:'fieldOutages'}).then(function(r){if(!r.ok)throw new Error(r.error);\nvar h=r.items.map(function(o){return '<div class=\"card\"><div style=\"display:flex;justify-content:space-between;gap:8px\"><b>'+esc(o.code)+': '+esc(o.service)+'</b><span class=\"st'+(o.status==='Đang diễn ra'?' in':'')+'\">'+esc(o.status)+'</span></div><div class=\"muted\">Block '+esc(o.blocks)+', tầng '+esc(o.floors)+'</div><div class=\"muted\">'+(o.status==='Đang diễn ra'?'Ngưng từ '+fdt(o.actualStart||o.planStart)+(o.planEnd?', hẹn có lại '+fdt(o.planEnd):''):'Theo thông báo: '+fdt(o.planStart)+' đến '+fdt(o.planEnd))+'</div>'+(o.cause?'<div class=\"muted\">'+esc(o.cause)+'</div>':'')+'<button class=\"btn\" data-oc=\"'+esc(o.code)+'\" data-oa=\"'+(o.status==='Đang diễn ra'?'end':'start')+'\" style=\"margin-top:10px\">'+(o.status==='Đang diễn ra'?'Đã có lại lúc này':'Bắt đầu ngưng lúc này')+'</button></div>'}).join('');\n$('#m').innerHTML=(h||'<div class=\"card muted\">Không có gián đoạn đang diễn ra hoặc sắp diễn ra.</div>')+'<div class=\"card\"><h2>Báo sự cố đột xuất</h2><label>Dịch vụ</label><select id=\"os\"><option>Nước</option><option>Điện</option><option>Thang máy</option><option>Cửa và thẻ</option><option>Khác</option></select><label>Block bị ảnh hưởng</label><input id=\"ob\" placeholder=\"Ví dụ: D hoặc Toàn khu\"><label>Tầng</label><input id=\"of\" placeholder=\"Ví dụ: 10-20 hoặc Tất cả\"><label>Nguyên nhân, hiện trạng</label><input id=\"oc\" placeholder=\"Ví dụ: bể ống đứng\"><label>Người báo</label><input id=\"ow\" value=\"'+esc(CFG.who||'')+'\"><div class=\"err\" id=\"er\" hidden></div><button class=\"btn\" id=\"onew\" style=\"margin-top:10px\">Gửi báo sự cố</button></div>';\ndocument.querySelectorAll('[data-oc]').forEach(function(b){b.onclick=function(){b.disabled=true;call({api:'outageEvent',act:b.dataset.oa,code:b.dataset.oc,who:CFG.who||''}).then(function(x){if(!x.ok)throw new Error(x.error);outages()}).catch(function(e){b.disabled=false;alert(e.message||e)})}});\n$('#onew').onclick=function(){var w=$('#ow').value.trim();CFG.who=w;localStorage.setItem('ssr-field',JSON.stringify(CFG));this.disabled=true;var me=this;call({api:'outageEvent',act:'new',service:$('#os').value,blocks:$('#ob').value.trim(),floors:$('#of').value.trim(),cause:$('#oc').value.trim(),who:w}).then(function(x){if(!x.ok)throw new Error(x.error);outages()}).catch(function(e){me.disabled=false;fail(e)})}}).catch(fail)}\n\nfunction start(){if(!CFG.pin)return setup();var type=P.cp?'cp':P.tb?'tb':P.m?'m':P.g?'g':'';var ref=P.cp||P.tb||P.m||P.g;if(!type)return outages();\ncall({api:'fieldInfo',type:type,ref:ref}).then(function(r){if(!r.ok)throw new Error(r.error);RES='Bình thường';PHOTO=null;THUMB=null;\nif(type==='g'){var g=r.guest,st=g['Giờ ra']?'<span class=\"st out\">Đã ra '+fdt(g['Giờ ra'])+'</span>':g['Giờ vào']?'<span class=\"st in\">Đã vào '+fdt(g['Giờ vào'])+'</span>':'<span class=\"st\">Chưa vào</span>';$('#sub').textContent='Khách đăng ký trước';\n$('#m').innerHTML='<div class=\"card\"><div class=\"big\">'+esc(g['Mã khách'])+'</div>'+st+'<div class=\"kv\"><span>Căn hộ</span><b>'+esc(g['Căn hộ'])+'</b><span>Khách</span><b>'+esc(g['Tên khách'])+'</b><span>Loại</span><b>'+esc(g['Loại'])+'</b><span>Biển số</span><b>'+esc(g['Biển số']||'Không')+'</b><span>Ngày</span><b>'+esc(g['Ngày'].slice(8,10)+'/'+g['Ngày'].slice(5,7)+'/'+g['Ngày'].slice(0,4))+'</b><span>Khung giờ</span><b>'+esc(g['Từ giờ'])+' đến '+esc(g['Đến giờ'])+'</b></div>'+(g['Ghi chú']?'<p class=\"muted\">'+esc(g['Ghi chú'])+'</p>':'')+\n(!g['Giờ vào']?'<label>Cổng</label><select id=\"gt\"><option>Cổng 1</option><option>Cổng 2</option><option>Lối xuống hầm</option></select><button class=\"btn\" id=\"gi\">Cho vào</button>':!g['Giờ ra']?'<button class=\"btn sec\" id=\"go\">Ghi nhận ra</button>':'')+'<div class=\"err\" id=\"er\" hidden></div></div>';\nif($('#gi'))$('#gi').onclick=function(){this.disabled=true;call({api:'guestIn',g:ref,gate:$('#gt').value,who:CFG.who}).then(function(x){if(!x.ok)throw new Error(x.error);done('Đã ghi nhận khách vào lúc '+new Date().toTimeString().slice(0,5))}).catch(function(e){$('#gi').disabled=false;fail(e)})};\nif($('#go'))$('#go').onclick=function(){this.disabled=true;call({api:'guestOut',g:ref,who:CFG.who}).then(function(x){if(!x.ok)throw new Error(x.error);done('Đã ghi nhận khách ra')}).catch(fail)};return}\nvar i=r.info,lab={cp:'Điểm tuần tra',tb:'Thiết bị',m:'Công tơ'}[type];$('#sub').textContent=lab;\nvar h='<div class=\"card\"><span class=\"muted\">'+lab+' '+esc(r.ref)+'</span><h2>'+esc(i[0])+'</h2><div class=\"muted\">'+esc(type==='m'?i[2]:i[1])+(type==='tb'&&i[2]?', tình trạng hiện tại: '+esc(i[2]):'')+'</div>'+(r.last?'<p class=\"muted\">Lần ghi gần nhất: '+fdt(r.last.t)+', '+esc(r.last.who)+(r.last.value?', chỉ số '+esc(r.last.value):'')+(r.last.result?', '+esc(r.last.result):'')+'</p>':'')+'</div><div class=\"card\">';\nif(type==='cp')h+='<label>Tình trạng tại điểm</label>'+seg(['Bình thường','Bất thường']);\nif(type==='tb')h+='<label>Kết quả kiểm tra</label>'+seg(['Bình thường','Cần theo dõi','Hỏng']);\nif(type==='m')h+='<label>Chỉ số hiện tại ('+esc(i[1])+')</label><input id=\"val\" type=\"number\" inputmode=\"decimal\" step=\"any\">';\nh+='<label>Ghi chú</label><textarea id=\"nt\" maxlength=\"500\"></textarea>'+photoBox()+'<button class=\"btn\" id=\"sb\">'+(type==='cp'?'Xác nhận đã tuần tra':'Gửi ghi nhận')+'</button><div class=\"err\" id=\"er\" hidden></div><p class=\"muted\">Người ghi: '+esc(CFG.who)+' <a href=\"#\" onclick=\"resetCfg();return false\">Đổi</a></p></div>';\n$('#m').innerHTML=h;bindSeg();bindPhoto();\n$('#sb').onclick=function(){var b=this;b.disabled=true;var p={api:'fieldlog',type:{cp:'Tuần tra',tb:'Kiểm tra thiết bị',m:'Chỉ số công tơ'}[type],ref:r.ref,who:CFG.who,result:type==='m'?'':RES,value:type==='m'?$('#val').value:'',note:$('#nt').value.trim(),photo:PHOTO,thumb:THUMB};\ncall(p).then(function(x){if(!x.ok)throw new Error(x.error);done(type==='cp'?'Đã ghi nhận tuần tra lúc '+new Date().toTimeString().slice(0,5):'Đã gửi ghi nhận, cảm ơn anh chị')}).catch(function(e){b.disabled=false;fail(e)})}}).catch(fail)}\nif(window.google&&google.script&&google.script.url)google.script.url.getLocation(function(l){P=l.parameter||{};start()});\nelse{location.search.slice(1).split('&').forEach(function(kv){var a=kv.split('=');if(a[0])P[a[0]]=decodeURIComponent(a[1]||'')});start()}\n</script>\n</body>\n</html>\n";
