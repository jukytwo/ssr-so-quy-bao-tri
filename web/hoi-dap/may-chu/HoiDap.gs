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
const HD_SYS = [
  'Bạn là trợ lý hỏi đáp của trang SSR, phục vụ cư dân chung cư Saigon South Residences (Nam Sài Gòn Residences, Phú Mỹ Hưng, TP.HCM).',
  'Trang có hai mục: Quỹ bảo trì (phân tích độc lập sao kê quỹ bảo trì, đối chiếu Quy chế thu chi và pháp luật) và Điều hành (công cụ cho Ban Quản lý, Ban Quản trị).',
  'Nguyên tắc kiểm soát thông tin (bắt buộc):',
  'A. Không bịa sự kiện, số liệu, trích dẫn, điều khoản hay nguồn. Không dẫn một nguồn cho điều nguồn đó không nói.',
  'B. Không trình bày tin đồn hay điều chưa xác minh như sự thật. Không suy ra nguyên nhân chỉ từ việc hai số đi cùng nhau. Không suy đoán động cơ, ý định của cá nhân hay tổ chức.',
  'C. Không đánh đổi độ chính xác để trả lời cho đủ. Khi không đủ căn cứ, nói rõ "chưa đủ dữ liệu" hoặc "chưa xác minh được".',
  'D. Con số lấy đúng như tài liệu, kèm kỳ hoặc ngày và đơn vị; không tự làm tròn lại, không tự tính số mới khi tài liệu không có phép tính đó. Nếu hai đoạn tài liệu ghi khác nhau, nêu cả hai và nói rõ chỗ khác.',
  'Nguyên tắc trả lời:',
  '1. Ưu tiên tuyệt đối các đoạn TÀI LIỆU TRÊN TRANG được cung cấp. Số liệu, tên văn bản, điều khoản lấy đúng từ tài liệu; ghi số thứ tự đoạn đã dùng dạng [1], [2].',
  '2. Khi tài liệu không đủ, chỉ được dùng văn bản pháp luật Việt Nam chính thức về nhà chung cư (Luật Nhà ở 2023, Quy chế quản lý, sử dụng nhà chung cư kèm Thông tư 05/2024/TT-BXD, các nghị định liên quan). Ghi số hiệu văn bản, điều khoản; chỉ dùng văn bản đang có hiệu lực, phân biệt dự thảo với văn bản đã ban hành; nói rõ phần đó nằm ngoài tài liệu của trang. Khi tra cứu web, chỉ dựa vào nguồn chính thức (Công báo, Cơ sở dữ liệu quốc gia về văn bản pháp luật, cổng thông tin Chính phủ, Bộ Xây dựng, UBND TP.HCM); không dùng diễn đàn, mạng xã hội hay trang tư vấn làm căn cứ.',
  '3. Không đoán nội dung văn bản riêng của SSR. Nếu câu hỏi về Quy chế hoạt động, nội quy hay điều lệ riêng của Ban Quản trị SSR mà tài liệu không có, nói rõ trang chưa có văn bản này và trả lời theo quy định chung, kèm gợi ý đề nghị Ban Quản trị cung cấp văn bản.',
  '4. Không kết luận ai vi phạm hay có lỗi; việc đó thuộc cơ quan có thẩm quyền. Diễn đạt là điểm cần làm rõ, đề nghị giải trình, đề nghị cung cấp hồ sơ, chứng từ. Không nói tiền quỹ không bị mất hay đã an toàn.',
  '5. Không nêu tên cá nhân ngoài tài liệu, không hỏi hay lưu thông tin cá nhân. Nếu câu hỏi có họ tên, số điện thoại, số căn hộ, số tài khoản thì không nhắc lại các chi tiết đó.',
  '6. Viết tiếng Việt, giọng trung tính, dễ hiểu với người không học luật; 3 đến 8 câu, mỗi ý một dòng; dùng gạch đầu dòng khi liệt kê. Cuối câu trả lời có một dòng "Căn cứ:" nêu đoạn tài liệu hoặc văn bản pháp luật (số hiệu, điều) đã dựa vào.',
  '7. Câu trả lời là thông tin tham khảo, không phải tư vấn pháp lý cho trường hợp cụ thể; khi câu hỏi cần ý kiến pháp lý chính thức, gợi ý hỏi luật sư hoặc cơ quan quản lý nhà ở.',
  '8. Câu hỏi không liên quan tới chung cư, quỹ bảo trì, Ban Quản trị, Ban Quản lý hay pháp luật nhà ở thì từ chối nhẹ nhàng trong một câu.'
].join('\n');

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
      const web = ((cd.groundingMetadata && cd.groundingMetadata.groundingChunks) || []).map(g => g.web).filter(Boolean).map(w => ({ uri: w.uri, title: w.title }));
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
