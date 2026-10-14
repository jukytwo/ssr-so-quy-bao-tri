# -*- coding: utf-8 -*-
"""Clip doc NGAN tom tat moi van de tu ban day du (04/10/2026). Khoang 90 giay, tong mau logo SSR (nap qua video_ssr_25)."""
import os, sys
os.environ.setdefault("CLIP_RES", "1080")
sys.path.insert(0, "/home/claude/ssr"); os.chdir("/home/claude/ssr")
import video_ssr_25 as V
O = V.O; _V = {v["id"]: v for v in O.V_ONE}
S0 = dict(sec="Tiền có mất không", icon="view")
vis = [dict(_V["ok"]), dict(_V["tong"]), dict(_V["pa"]), dict(_V["cuda"])]
vs = [("bia", "Quỹ bảo trì chung cư: năm vấn đề trong 90 giây."),
      ("bia", "Ngày 23/12/2025, 986,9 triệu tiền quỹ chuyển vào tài khoản do chính các thành viên Ban quản trị đồng đứng tên."),
      ("ok#2", "Tiền chưa mất: 198 giao dịch khớp tới từng đồng, tiền gốc còn 127,15 tỷ."),
      ("ok#-1", "Nhưng tiền đi sai đường ở năm chỗ."),
      ("tong#0", "Một: 986,9 triệu tiền quỹ vào tài khoản của Ban quản trị, trái Điều 7.2, 7.4 và 3.2.a."),
      ("tong#1", "Hai: 1,71 tỷ tiền khu vực chung không vào quỹ, trong đó 1,40 tỷ đã chi ngoài quy trình."),
      ("tong#2", "Ba: 13 khoản chi trên 50 triệu, tổng 5,04 tỷ, chưa thấy văn bản cho phép."),
      ("tong#3", "Bốn: 1,69 tỷ chưa truy được tới cùng, trong đó 705,8 triệu trả trọn cho Thép Quang."),
      ("tong#4", "Năm: 127,5 tỷ tiền gửi sau tái tục chưa có xác nhận của ngân hàng."),
      ("tong#-1", "Hai vấn đề đầu đã rõ trên sao kê; ba vấn đề sau đang chờ chứng từ."),
      ("pa#-1", "Hội nghị có ba phương án, xét riêng từng thành viên: giữ, xem xét thêm, hoặc bãi nhiệm."),
      ("cuda#-1", "Cư dân nên xem bộ clip đầy đủ, đọc ba file trong thư mục chia sẻ, và theo dõi câu trả lời cho mười câu hỏi."),
      ("lienhe", V.END)]
for s in vs: assert "(" not in s[1] and "→" not in s[1]
C = V.VS.C.copy()
C.update(hero_title="Quỹ bảo trì: **năm vấn đề** trong 90 giây", video_cover_stats=[["5", "vấn đề", "r"], ["127,15 tỷ", "tiền gốc còn", "g"]],
         video_script=vs, video_visuals=vis)
C["meta"] = dict(V.VS.C["meta"], date="Tóm tắt · 04/10/2026"); C.pop("video_script_short", None)
if __name__ == "__main__":
    if "prepare" in sys.argv:
        import audit_voice as AV; print(AV.prepare([x[1] for x in vs]))
    else:
        V.build(C, "SSR_Quy_bao_tri_clip_doc_tom_tat", "t", "Quỹ bảo trì SSR: tóm tắt năm vấn đề")
