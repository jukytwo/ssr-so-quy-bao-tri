/**
 * Máy chủ Hỏi đáp SSR (Google Apps Script).
 * Nhận câu hỏi từ trang SSR, lấy các đoạn nội dung liên quan trong kho kb.json của trang,
 * rồi hỏi Gemini (gói miễn phí). Khóa Gemini chỉ nằm ở Thuộc tính tập lệnh, không nằm trong trang.
 *
 * Thuộc tính tập lệnh (Cài đặt dự án > Thuộc tính tập lệnh):
 *   GEMINI_API_KEY  bắt buộc, lấy ở https://aistudio.google.com/apikey
 *   DAILY_LIMIT     tùy chọn, số câu hỏi AI tối đa mỗi ngày, mặc định 300
 *   GEMINI_MODEL    tùy chọn, danh sách mô hình cách nhau dấu phẩy, thử lần lượt
 *   GEMINI_SEARCH   tùy chọn, "0" để tắt tra cứu Google khi trả lời
 *   KB_URL          tùy chọn, địa chỉ kb.json nếu trang chuyển đi nơi khác
 */
const HD_KB_URL = 'https://jukytwo.github.io/ssr-so-quy-bao-tri/web/hoi-dap/kb.json';
const HD_MODELS = 'gemini-flash-latest,gemini-2.5-flash,gemini-2.5-flash-lite';
// Chỉ dẫn hệ thống theo Bộ nguyên tắc xác minh thông tin và phân tích dựa trên bằng chứng (bản hợp nhất 17/10/2026), Phần I, IV, V.
const HD_SYS = [
  'Bạn là trợ lý hỏi đáp của trang SSR, phục vụ cư dân chung cư Saigon South Residences (Nam Sài Gòn Residences, Phú Mỹ Hưng, TP.HCM).',
  'Trang có hai mục: Quỹ bảo trì (phân tích độc lập sao kê quỹ bảo trì, đối chiếu Quy chế thu chi và pháp luật) và Điều hành (công cụ cho Ban Quản lý, Ban Quản trị).',
  '',
  'A. KIỂM SOÁT THÔNG TIN',
  '- Không bịa sự kiện, số liệu, trích dẫn hay nguồn; không dẫn một nguồn cho điều nguồn đó không nói.',
  '- Không trình bày tin đồn, tin chưa xác minh như sự thật. Không suy ra quan hệ nhân quả chỉ từ tương quan. Không suy đoán động cơ, ý định của cá nhân hay tổ chức.',
  '- Thông tin có tính thời điểm phải ghi rõ thời điểm (ví dụ số dư tại một ngày cụ thể); không dùng thông tin cũ như thông tin hiện tại.',
  '- Không đánh đổi tính chính xác để có câu trả lời đầy đủ. Thiếu căn cứ thì nói rõ chưa đủ dữ liệu hoặc chưa xác minh được.',
  '',
  'B. ĐÓNG SÁCH',
  '- Chỉ trả lời từ các đoạn TÀI LIỆU TRÊN TRANG được cấp, đánh số [1], [2]...',
  '- Tài liệu không có thông tin và câu hỏi không phải về quy định pháp luật nhà chung cư: trả lời đúng một câu "Tài liệu trên trang chưa đề cập nội dung này.", rồi gợi ý tên mục gần nhất trong các đoạn được cấp.',
  '- Số liệu chép nguyên văn từ tài liệu: không làm tròn lại, không tự tính số mới khi tài liệu không có phép tính đó. Mỗi số kèm thời điểm hoặc kỳ như tài liệu ghi.',
  '',
  'C. PHẦN NGOÀI TÀI LIỆU, CHỈ CHO QUY ĐỊNH PHÁP LUẬT VỀ NHÀ CHUNG CƯ',
  '- Chỉ dùng văn bản pháp luật chính thức còn hiệu lực; ghi đúng số hiệu, tên văn bản, ngày có hiệu lực và điều khoản; nêu tình trạng hiệu lực (còn hiệu lực, bị sửa đổi, bị thay thế); phân biệt dự thảo với văn bản đã ban hành; phân biệt luật, nghị định, thông tư, quyết định, công văn.',
  '- Mở đầu phần này bằng "Ngoài tài liệu của trang:" để người đọc biết đây không phải nội dung của trang.',
  '- Khi tra cứu web chỉ dựa vào nguồn chính thức (Công báo, Cơ sở dữ liệu quốc gia về văn bản pháp luật, cổng thông tin Chính phủ, bộ, ngành, Quốc hội) hoặc báo chí lớn có quy trình đính chính; không dựa vào diễn đàn, mạng xã hội, trang tư vấn.',
  '- Không chắc số hiệu, ngày hiệu lực hay nội dung điều khoản thì nói chưa xác minh được, không đoán.',
  '- Nêu điều kiện áp dụng, ngoại lệ, quy định chuyển tiếp khi có. Không tư vấn pháp lý cho trường hợp cụ thể.',
  '- Quy chế hoạt động, nội quy, điều lệ riêng của Ban Quản trị SSR mà tài liệu không có: nói rõ trang chưa có văn bản này, chỉ nêu quy định chung và gợi ý đề nghị Ban Quản trị cung cấp văn bản.',
  '',
  'D. KHÔNG KẾT LUẬN THAY CƠ QUAN CÓ THẨM QUYỀN',
  '- Không kết luận ai vi phạm, có lỗi hay chiếm đoạt. Diễn đạt là điểm cần làm rõ, đề nghị giải trình, đề nghị cung cấp hồ sơ, chứng từ.',
  '- Không nói tiền quỹ không bị mất, đã an toàn, hay chắc chắn bị thất thoát.',
  '- Không nêu tên cá nhân ngoài tài liệu. Không nhắc lại họ tên, số điện thoại, số căn hộ, số tài khoản mà người hỏi ghi vào câu hỏi.',
  '- Không đưa khuyến nghị nào ngoài nội dung có trong tài liệu.',
  '',
  'E. TRÌNH BÀY',
  '- Tiếng Việt, giọng trung tính, dễ hiểu với người không học luật; 3 đến 8 câu, mỗi ý một dòng, gạch đầu dòng khi liệt kê.',
  '- Dòng cuối bắt đầu bằng "Căn cứ:", nêu số đoạn [n] kèm tên mục, hoặc văn bản pháp luật kèm điều khoản.',
  '- Câu hỏi không liên quan tới chung cư, quỹ bảo trì, Ban Quản trị, Ban Quản lý hay pháp luật nhà ở thì từ chối nhẹ nhàng trong một câu.'
].join('\n');
// Nguồn tra cứu web được hiện cho cư dân: chỉ nguồn chính thức và báo chí lớn (Phần III, mục 1 đến 3).
const HD_WEB_OK = ['gov.vn', 'vbpl.vn', 'chinhphu.vn', 'quochoi.vn', 'baochinhphu.vn', 'vietnamplus.vn', 'nhandan.vn', 'vnexpress.net', 'tuoitre.vn', 'thanhnien.vn', 'nld.com.vn', 'sggp.org.vn', 'plo.vn', 'laodong.vn', 'reuters.com', 'apnews.com', 'afp.com'];
function hdWebOk_(w) {
  const h = String(w.title || '').toLowerCase().trim() || (String(w.uri || '').match(/^https?:\/\/([^/]+)/) || [])[1] || '';
  return HD_WEB_OK.some(d => h === d || h.endsWith('.' + d));
}

function hdP_() { return PropertiesService.getScriptProperties(); }
function hdOut_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function doGet(e) {
  return hdOut_({ ok: true, app: 'SSR Hoi dap', ai: !!hdP_().getProperty('GEMINI_API_KEY') });
}

function doPost(e) {
  let b = {};
  try { b = JSON.parse((e && e.postData && e.postData.contents) || '{}'); } catch (x) { }
  const q = String(b.q || '').replace(/\s+/g, ' ').trim().slice(0, 500);
  if (q.length < 4) return hdOut_({ ok: false, error: 'Câu hỏi quá ngắn.' });
  const pr = hdP_(), key = pr.getProperty('GEMINI_API_KEY');
  if (!key) return hdOut_({ ok: false, error: 'Phần hỏi AI chưa được cài khóa. Vui lòng báo người quản lý trang.' });
  const ids = (Array.isArray(b.ids) ? b.ids : []).slice(0, 8).map(String);
  const cache = CacheService.getScriptCache();
  const hk = 'a' + Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, q.toLowerCase() + '|' + ids.join(','), Utilities.Charset.UTF_8));
  const hit = cache.get(hk); if (hit) { const o = JSON.parse(hit); o.cached = true; return hdOut_(o); }
  // trần số câu hỏi AI mỗi ngày
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  const day = Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'yyyy-MM-dd'), lim = +(pr.getProperty('DAILY_LIMIT') || 300);
  let cnt = {}; try { cnt = JSON.parse(pr.getProperty('HD_COUNT') || '{}'); } catch (x) { }
  if (cnt.d !== day) cnt = { d: day, n: 0 };
  if (cnt.n >= lim) { lock.releaseLock(); return hdOut_({ ok: false, error: 'Hôm nay đã dùng hết lượt hỏi AI. Câu trả lời có sẵn trên trang vẫn dùng bình thường; phần AI mở lại vào ngày mai.' }); }
  cnt.n++; pr.setProperty('HD_COUNT', JSON.stringify(cnt)); lock.releaseLock();
  const kb = hdKb_(), used = [], parts = [];
  ids.forEach(id => { const c = kb[id]; if (!c) return; used.push(id); parts.push('[' + used.length + '] ' + c.st + ' | ' + c.t + '\n' + String(c.x).slice(0, 1600)); });
  const ctx = parts.join('\n\n').slice(0, 9000);
  const r = hdGemini_(key, q, ctx);
  if (r.ok) { r.used = used; try { cache.put(hk, JSON.stringify(r), 21600); } catch (x) { } }
  else { const c2 = JSON.parse(pr.getProperty('HD_COUNT') || '{}'); if (c2.d === day && c2.n > 0) { c2.n--; pr.setProperty('HD_COUNT', JSON.stringify(c2)); } }
  return hdOut_(r);
}

/** Kho nội dung của trang, lưu đệm 6 giờ, chia nhỏ vì mỗi ô đệm tối đa 100 KB. */
function hdKb_() {
  const cache = CacheService.getScriptCache(), url = hdP_().getProperty('KB_URL') || HD_KB_URL;
  let txt = null; const n = +(cache.get('kbn') || 0);
  if (n) { const m = cache.getAll(Array.from({ length: n }, (_, i) => 'kb' + i)); const a = []; for (let i = 0; i < n; i++) { if (!m['kb' + i]) { a.length = 0; break; } a.push(m['kb' + i]); } if (a.length === n) txt = a.join(''); }
  if (!txt) {
    txt = UrlFetchApp.fetch(url, { muteHttpExceptions: true }).getContentText('UTF-8');
    const size = 90000, pieces = {}; let k = 0; for (let i = 0; i < txt.length; i += size) pieces['kb' + (k++)] = txt.slice(i, i + size);
    try { cache.putAll(pieces, 21600); cache.put('kbn', String(k), 21600); } catch (x) { }
  }
  const map = {}; try { JSON.parse(txt).items.forEach(c => map[c.id] = c); } catch (x) { }
  return map;
}

function hdGemini_(key, q, ctx) {
  const pr = hdP_(), models = (pr.getProperty('GEMINI_MODEL') || HD_MODELS).split(',').map(s => s.trim()).filter(Boolean);
  const modes = pr.getProperty('GEMINI_SEARCH') === '0' ? [false] : [true, false];
  const user = 'TÀI LIỆU TRÊN TRANG SSR:\n' + (ctx || '(không tìm thấy đoạn nào liên quan trên trang)') + '\n\nCÂU HỎI CỦA CƯ DÂN: ' + q;
  let last = '';
  for (const m of models) for (const s of modes) {
    const body = { systemInstruction: { parts: [{ text: HD_SYS }] }, contents: [{ role: 'user', parts: [{ text: user }] }], generationConfig: { temperature: 0.2, maxOutputTokens: 1024 } };
    if (s) body.tools = [{ google_search: {} }];
    let res; try {
      res = UrlFetchApp.fetch('https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(m) + ':generateContent', { method: 'post', contentType: 'application/json', headers: { 'x-goog-api-key': key }, payload: JSON.stringify(body), muteHttpExceptions: true });
    } catch (x) { last = String(x); continue; }
    const code = res.getResponseCode(); let j = {}; try { j = JSON.parse(res.getContentText()); } catch (x) { }
    if (code === 200 && j.candidates && j.candidates[0] && j.candidates[0].content) {
      const cd = j.candidates[0], text = (cd.content.parts || []).map(p => p.text || '').join('').trim();
      if (!text) { last = 'trống'; continue; }
      const web = ((cd.groundingMetadata && cd.groundingMetadata.groundingChunks) || []).map(g => g.web).filter(Boolean).filter(hdWebOk_).map(w => ({ uri: w.uri, title: w.title }));
      return { ok: true, answer: text, model: m, web: web };
    }
    last = code + ' ' + ((j.error && j.error.message) || '').slice(0, 160);
  }
  console.log('Gemini lỗi: ' + last);
  return { ok: false, error: 'AI đang bận hoặc tạm hết lượt miễn phí. Vui lòng thử lại sau ít phút.' };
}

/** Chạy thử trong trình soạn mã: chọn hàm kiemTraHoiDap, bấm Chạy, xem Nhật ký thực thi. */
function kiemTraHoiDap() {
  const key = hdP_().getProperty('GEMINI_API_KEY');
  console.log(key ? 'ĐẠT: đã có GEMINI_API_KEY' : 'LỖI: chưa có GEMINI_API_KEY trong Thuộc tính tập lệnh');
  const kb = hdKb_(); console.log('Kho nội dung: ' + Object.keys(kb).length + ' mục');
  if (!key) return;
  const r = hdGemini_(key, 'Ban quản trị có phải công khai thông tin tài khoản quỹ bảo trì không?', '');
  console.log(r.ok ? 'ĐẠT: Gemini trả lời bằng mô hình ' + r.model + '\n' + r.answer.slice(0, 400) : 'LỖI: ' + r.error);
}
