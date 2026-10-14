# -*- coding: utf-8 -*-
"""Bo dung bao cao PDF theo tieu chi thiet ke ban tin (khong nhan dien thuong hieu)."""
import html, re, json

NAVY, NAVY2, GOLD, CREAM, ICE, BAND, GREEN, RED = "#1F3864", "#16294A", "#C8992F", "#FBF3DF", "#EEF3FA", "#DCE6F1", "#1E7A46", "#A93434"
ORANGE = "#C0662A"
E = lambda s: html.escape(str(s), quote=False)

def vnd(n): return f"{round(n):,}".replace(",", ".")
def ty(n, d=2): return f"{n/1e9:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def tr(n, d=1): return f"{n/1e6:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def pct(x, d=1): return f"{x*100:.{d}f}".replace(".", ",") + "%"

CSS = """
@page { size: A4; margin: 17mm 18mm 20mm 18mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin:0; font-family:'Liberation Serif','Times New Roman',serif; font-size:9.8pt; line-height:1.5; color:#111; }
.sans, h1, h2, h3, h4, table, .kpi, .pill, .lab, .kick, .src, .chip, .band, .card, .nd .lbl, .toc, .cap, .tl, .demo .lb { font-family:'Be Vietnam Pro','Liberation Sans',Arial,sans-serif; }
h1,h2,h3,h4 { margin:0; color:""" + NAVY + """; }
p { margin:0 0 5pt 0; text-align:justify; }
b, strong { font-weight:700; }
.cover { break-after: page; min-height: 254mm; display:flex; flex-direction:column; gap:8pt; }
.c-top { display:flex; justify-content:space-between; align-items:center; border-bottom:2pt solid """ + NAVY + """; padding-bottom:6pt; }
.c-top .lab { font-size:8.5pt; font-weight:700; letter-spacing:.12em; color:""" + NAVY + """; }
.c-top .lab2 { font-size:8.5pt; font-weight:600; letter-spacing:.06em; color:#5a6475; font-family:'Be Vietnam Pro',sans-serif; }
.c-title { font-size:25pt; line-height:1.15; font-weight:800; color:""" + NAVY + """; margin-top:6pt; letter-spacing:-.01em; }
.c-sub { font-family:'Be Vietnam Pro',sans-serif; font-size:10.5pt; color:#3d4656; }
.pills { display:flex; gap:5pt; flex-wrap:wrap; }
.pill { display:inline-block; font-size:7.9pt; font-weight:700; border-radius:20pt; padding:2.3pt 8pt; background:""" + CREAM + """; color:#6b5216; border:0.8pt solid #e6cf92; }
.pill.navy { background:""" + NAVY + """; color:#fff; border-color:""" + NAVY + """; }
.pill.red { background:#f7e3e3; color:""" + RED + """; border-color:#e6b9b9; }
.pill.org { background:#fbeadd; color:""" + ORANGE + """; border-color:#efc6a6; }
.pill.yel { background:#fbf1d2; color:#7d5d00; border-color:#ead58f; }
.pill.grn { background:#e2f1e8; color:""" + GREEN + """; border-color:#b6dcc4; }
.hero { display:grid; grid-template-columns: 1fr 1.12fr; gap:10pt; align-items:stretch; }
.herofig { background:""" + NAVY + """; color:#fff; border-radius:6pt; padding:12pt 14pt; display:flex; flex-direction:column; justify-content:space-between; }
.herofig .k { font-family:'Be Vietnam Pro',sans-serif; font-size:8.5pt; letter-spacing:.1em; font-weight:700; color:#f1d98f; }
.herofig .v { font-family:'Be Vietnam Pro',sans-serif; font-size:40pt; font-weight:800; line-height:1.0; margin-top:4pt; }
.herofig .v small { font-size:15pt; font-weight:600; margin-left:3pt; }
.herofig .s { font-family:'Be Vietnam Pro',sans-serif; font-size:9pt; color:#dbe3f2; margin-top:6pt; line-height:1.45; }
.herofig .bar { display:flex; height:9pt; border-radius:3pt; overflow:hidden; gap:1.5pt; margin-top:8pt; }
.herofig .bar div { height:100%; }
.herofig .leg { font-family:'Be Vietnam Pro',sans-serif; font-size:7.6pt; color:#dbe3f2; margin-top:5pt; display:flex; flex-wrap:wrap; gap:3pt 10pt; }
.herofig .leg i { display:inline-block; width:7pt; height:7pt; border-radius:2pt; margin-right:3pt; vertical-align:-0.5pt; }
.kpis { display:grid; grid-template-columns: repeat(3, 1fr); gap:6pt; }
.kpi { border:0.8pt solid #cfd8e6; border-radius:5pt; padding:6pt 8pt; background:#fff; }
.kpi .k { font-size:7.6pt; color:#5a6475; font-weight:600; }
.kpi .v { font-size:15pt; font-weight:800; color:""" + NAVY + """; line-height:1.15; margin-top:1pt; }
.kpi .v small { font-size:8.5pt; font-weight:600; margin-left:2pt; color:#3d4656; }
.kpi .s { font-size:7.4pt; color:#3d4656; margin-top:1pt; line-height:1.35; }
.kpi.r .v { color:""" + RED + """; } .kpi.o .v { color:""" + ORANGE + """; } .kpi.g .v { color:""" + GREEN + """; }
.keyband { background:""" + NAVY2 + """; color:#fff; border-radius:6pt; padding:10pt 13pt; }
.keyband .lab { font-family:'Be Vietnam Pro',sans-serif; font-size:8.3pt; font-weight:800; letter-spacing:.12em; color:#f1d98f; margin-bottom:4pt; }
.keyband ul { margin:0; padding:0; list-style:none; }
.keyband li { font-size:9.9pt; line-height:1.42; padding-left:11pt; position:relative; margin:1.6pt 0; text-align:left; }
.keyband li:before { content:''; position:absolute; left:0; top:6pt; width:5pt; height:5pt; border-radius:50%; background:""" + GOLD + """; }
.keyband li.first { font-weight:700; }
.three { display:grid; grid-template-columns: repeat(3, 1fr); gap:7pt; }
.three .card { border-top:3pt solid """ + GOLD + """; background:""" + ICE + """; padding:7pt 9pt; border-radius:0 0 5pt 5pt; }
.three .card .no { font-size:17pt; font-weight:800; color:""" + GOLD + """; line-height:1; }
.three .card .h { font-size:9pt; font-weight:700; color:""" + NAVY + """; margin-top:3pt; line-height:1.3; }
.three .card .t { font-family:'Liberation Serif',serif; font-size:9pt; margin-top:3pt; line-height:1.4; color:#222; }
.toc { font-size:8.2pt; color:#3d4656; border-top:0.8pt solid #cfd8e6; padding-top:6pt; line-height:1.6; }
.toc b { color:""" + NAVY + """; }
.disc { font-family:'Be Vietnam Pro',sans-serif; font-size:7.3pt; color:#6a7384; line-height:1.4; margin-top:auto; }
.sec { margin-top:4pt; }
.sec-h { display:flex; align-items:center; gap:8pt; background:""" + BAND + """; border-radius:4pt; padding:5pt 9pt; margin:10pt 0 7pt 0; break-after:avoid; }
.sec-h .no { font-family:'Be Vietnam Pro',sans-serif; font-size:13pt; font-weight:800; color:""" + GOLD + """; }
.sec-h h2 { font-size:12.2pt; font-weight:800; color:""" + NAVY + """; letter-spacing:-.005em; }
h3 { font-size:10pt; font-weight:700; margin:8pt 0 4pt 0; break-after:avoid; }
.kick { font-size:8.6pt; color:#3d4656; border-left:2.5pt solid """ + GOLD + """; padding:1pt 0 1pt 7pt; margin:0 0 6pt 0; line-height:1.45; }
table { width:100%; border-collapse:collapse; font-size:9pt; line-height:1.36; margin:3pt 0 4pt 0; }
thead { display:table-header-group; }
th { background:""" + NAVY + """; color:#fff; font-weight:700; text-align:left; padding:4pt 5pt; border:0.6pt solid """ + NAVY + """; vertical-align:bottom; }
td { padding:3.4pt 5pt; border:0.6pt solid #cfd6e2; vertical-align:top; }
tr { break-inside:avoid; }
tbody tr:nth-child(even) td { background:#f7f9fc; }
td.n, th.n { text-align:right; white-space:nowrap; font-variant-numeric: tabular-nums; }
td.c, th.c { text-align:center; }
tr.tot td { background:""" + BAND + """ !important; font-weight:700; color:""" + NAVY + """; }
tr.hl-r td { background:#fbeaea !important; } tr.hl-o td { background:#fdf0e6 !important; } tr.hl-y td { background:#fdf7e1 !important; }
td .sm { font-size:7.6pt; color:#5a6475; display:block; margin-top:1pt; }
.src { font-size:7.4pt; color:#6a7384; margin:1pt 0 6pt 0; font-style:normal; }
.nd { break-inside:avoid; background:#EDF1F7; border-left:3pt solid """ + NAVY + """; padding:6pt 9pt 5pt 9pt; margin:6pt 0 8pt 0; border-radius:0 4pt 4pt 0; }
.nd .lbl { font-size:8.3pt; font-weight:800; color:""" + NAVY + """; letter-spacing:.06em; margin-bottom:2pt; }
.nd ul { margin:0; padding:0; list-style:none; }
.nd li { position:relative; padding-left:10pt; margin:1.5pt 0; line-height:1.45; text-align:left; orphans:3; widows:3; }
.nd li:before { content:''; position:absolute; left:0; top:5.2pt; width:4.2pt; height:4.2pt; border-radius:50%; background:""" + GOLD + """; }
.nd li.first { font-weight:700; color:""" + NAVY2 + """; }
.nd.gold { background:""" + CREAM + """; border-left-color:""" + GOLD + """; }
.nd.gold .lbl { color:#7a5a12; }
.two { display:grid; grid-template-columns: 1fr 1fr; gap:9pt; }
.cardbox { border:0.8pt solid #cfd8e6; border-radius:5pt; padding:7pt 9pt; break-inside:avoid; }
.cardbox h4 { font-size:9.2pt; font-weight:700; margin-bottom:3pt; }
.fig { break-inside:avoid; margin:4pt 0 2pt 0; }
.fig svg { width:100%; height:auto; display:block; }
.cap { font-size:8.2pt; font-weight:700; color:""" + NAVY + """; margin:4pt 0 2pt 0; break-after:avoid; }
.legend { font-family:'Be Vietnam Pro',sans-serif; font-size:7.5pt; color:#3d4656; display:flex; gap:10pt; flex-wrap:wrap; margin-top:2pt; }
.legend i { display:inline-block; width:7pt; height:7pt; border-radius:2pt; margin-right:3pt; vertical-align:-0.5pt; }
.verdict { display:grid; grid-template-columns: 30pt 1fr; gap:9pt; align-items:center; background:#e2f1e8; border:0.8pt solid #b6dcc4; border-radius:6pt; padding:8pt 11pt; break-inside:avoid; }
.verdict .ok { width:28pt; height:28pt; border-radius:50%; background:""" + GREEN + """; display:flex; align-items:center; justify-content:center; }
.verdict h4 { font-size:10.5pt; color:""" + GREEN + """; font-weight:800; }
.verdict p { font-size:9.2pt; margin:2pt 0 0 0; }
.scan { border:0.8pt solid #cfd6e2; border-radius:4pt; overflow:hidden; break-inside:avoid; margin:4pt 0; }
.scan img { width:100%; display:block; }
.scan .sc { font-family:'Be Vietnam Pro',sans-serif; font-size:7.5pt; color:#3d4656; background:#f5f7fa; padding:3pt 6pt; border-top:0.6pt solid #dde3ec; }
.demo { break-inside:avoid; border:0.8pt solid #cfd8e6; border-radius:5pt; padding:6pt 9pt; margin:5pt 0; }
.demo .ln { display:grid; grid-template-columns: 34mm 1fr; gap:6pt; align-items:baseline; margin:2pt 0; }
.demo .lb { font-size:7.8pt; color:#5a6475; font-weight:600; }
.demo .tx { font-family:'Liberation Serif','Times New Roman',serif; font-size:13pt; }
.demo .u { color:""" + GREEN + """; font-weight:700; text-decoration:underline; }
.demo .k { background:#fbf1d2; border-radius:2pt; }
.find { border:0.8pt solid #cfd8e6; border-radius:5pt; padding:6pt 9pt; margin:0 0 6pt 0; break-inside:auto; box-decoration-break:clone; -webkit-box-decoration-break:clone; }
.find .hd, .find h4 { break-after:avoid; } .find .row { break-inside:avoid; }
.find .hd { display:flex; align-items:center; gap:6pt; margin-bottom:3pt; flex-wrap:wrap; }
.find .code { font-family:'Be Vietnam Pro',sans-serif; font-weight:800; font-size:8.4pt; color:""" + NAVY + """; }
.find .amt { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; color:#3d4656; margin-left:auto; }
.find h4 { font-size:9.6pt; font-weight:700; line-height:1.3; margin-bottom:3pt; }
.find .row { display:grid; grid-template-columns: 22mm 1fr; gap:6pt; font-size:9pt; line-height:1.4; margin:1.5pt 0; }
.find .row .l { font-family:'Be Vietnam Pro',sans-serif; font-size:7.5pt; font-weight:700; color:#5a6475; padding-top:1pt; }
.find .view { font-weight:700; color:""" + NAVY2 + """; }
.tl { display:grid; grid-template-columns: repeat(4, 1fr); gap:6pt; break-inside:avoid; margin:4pt 0; }
.tl .st { border-top:3pt solid """ + NAVY + """; background:""" + ICE + """; padding:6pt 8pt; border-radius:0 0 4pt 4pt; }
.tl .st .n { font-size:8pt; font-weight:800; color:""" + GOLD + """; letter-spacing:.08em; }
.tl .st .h { font-size:8.8pt; font-weight:700; color:""" + NAVY + """; margin:2pt 0; line-height:1.3; }
.tl .st .t { font-family:'Liberation Serif',serif; font-size:8.8pt; line-height:1.4; }
.quote { border-left:2pt solid #cfd6e2; padding:2pt 0 2pt 8pt; margin:3pt 0 6pt 0; font-size:9.2pt; }
.quote .w { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; font-weight:700; color:""" + NAVY + """; margin-bottom:1pt; }
.facts { display:grid; grid-template-columns: repeat(4, 1fr); gap:6pt; margin:4pt 0 6pt 0; break-inside:avoid; }
.facts .f { background:""" + ICE + """; border-radius:4pt; padding:6pt 7pt; }
.facts .f .v { font-family:'Be Vietnam Pro',sans-serif; font-size:15pt; font-weight:800; color:""" + NAVY + """; line-height:1.1; }
.facts .f .k { font-family:'Be Vietnam Pro',sans-serif; font-size:7.5pt; color:#3d4656; margin-top:2pt; line-height:1.35; }
.brand { display:flex; align-items:center; gap:9pt; }
.brand img { width:20mm; height:20mm; display:block; }
.brand .lab { font-family:'Be Vietnam Pro',sans-serif; font-size:8.5pt; font-weight:800; letter-spacing:.12em; color:""" + NAVY + """; }
.brand .lab2 { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; font-weight:700; color:#16294A; margin-top:1pt; }
.brand .idl { font-family:'Be Vietnam Pro',sans-serif; font-size:7.4pt; color:#5a6475; margin-top:2pt; line-height:1.35; max-width:118mm; }
.c-date { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:700; color:#fff; background:""" + NAVY + """; border-radius:20pt; padding:3pt 10pt; white-space:nowrap; align-self:flex-start; margin-top:2pt; }
.stp { display:inline-block; font-family:'Be Vietnam Pro',sans-serif; font-size:7.6pt; font-weight:700; border-radius:7pt; padding:1pt 6pt; line-height:1.3; border:0.6pt solid transparent; }
.stp.no { background:#f7e3e3; color:""" + RED + """; border-color:#e6b9b9; }
.stp.q { background:#fbeadd; color:""" + ORANGE + """; border-color:#efc6a6; }
.stp.na { background:#edf0f4; color:#4a5566; border-color:#d3d9e2; }
.stp.part { background:#fbf1d2; color:#7d5d00; border-color:#ead58f; }
.stp.n { background:#e8eef8; color:#1F3864; border-color:#c7d3e8; }
.stp.ok { background:#e2f1e8; color:""" + GREEN + """; border-color:#b6dcc4; }
.mxbar { display:flex; gap:1.5pt; height:8pt; border-radius:3pt; overflow:hidden; margin:2pt 0 5pt 0; break-inside:avoid; }
.mxbar div { flex:1; }
.facts.f5 { grid-template-columns: repeat(5, 1fr); }
.facts .f.no .v { color:""" + RED + """; } .facts .f.q .v { color:""" + ORANGE + """; } .facts .f.ok .v { color:""" + GREEN + """; } .facts .f.part .v { color:#7d5d00; } .facts .f.na .v { color:#4a5566; }
.chkg { display:grid; grid-template-columns: 1fr 1fr; gap:7pt; margin:4pt 0 6pt 0; }
.chk { border:0.8pt solid #cfd8e6; border-radius:5pt; padding:6pt 9pt 7pt 9pt; break-inside:avoid; background:#fff; }
.chk .hd { display:flex; justify-content:space-between; gap:6pt; align-items:flex-start; margin-bottom:2pt; }
.chk .hd .stp, table.mx .stp { white-space:nowrap; flex-shrink:0; }
.chk h4 { font-size:9.4pt; font-weight:700; line-height:1.3; }
.chk .ln { font-size:9pt; line-height:1.42; margin-top:2.5pt; text-align:left; }
.chk .ln b { font-family:'Be Vietnam Pro',sans-serif; font-size:7.2pt; color:#5a6475; letter-spacing:.05em; display:block; font-weight:700; }
.chk .imp { font-size:9pt; font-weight:700; color:""" + NAVY2 + """; border-top:0.6pt solid #dde3ec; margin-top:4pt; padding-top:3pt; line-height:1.42; text-align:left; }
table.mx td { font-size:9pt; }
table.mx td.dieu { font-family:'Be Vietnam Pro',sans-serif; font-weight:700; font-size:8.4pt; color:""" + NAVY + """; }
table.mx td.cd { font-family:'Be Vietnam Pro',sans-serif; font-size:7.8pt; color:#3d4656; }
.two.t64 { grid-template-columns: 1.25fr 1fr; }
.howto { display:grid; grid-template-columns: repeat(3, 1fr); gap:6pt; margin:0 0 8pt 0; break-inside:avoid; }
.howto .h { border:0.8pt solid #cfd8e6; border-top:3pt solid """ + GOLD + """; border-radius:0 0 5pt 5pt; padding:5pt 8pt 6pt 8pt; background:#fff; }
.howto .h .t { font-family:'Be Vietnam Pro',sans-serif; font-size:8pt; font-weight:800; color:#8A6A1E; letter-spacing:.08em; }
.howto .h .d { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; color:#16294A; margin-top:2pt; line-height:1.4; }
.vans { background:""" + NAVY2 + """; color:#fff; border-radius:6pt; padding:10pt 13pt; display:grid; grid-template-columns: 1fr auto; gap:14pt; align-items:center; break-inside:avoid; }
.vans .lab { font-family:'Be Vietnam Pro',sans-serif; font-size:8.2pt; font-weight:800; letter-spacing:.12em; color:#f1d98f; }
.vans .a { font-family:'Be Vietnam Pro',sans-serif; font-size:12.6pt; font-weight:800; line-height:1.36; margin-top:3pt; }
.vans .vst { display:flex; gap:12pt; }
.vans .vst div { text-align:center; min-width:17mm; }
.vans .vst .v { font-family:'Be Vietnam Pro',sans-serif; font-size:24pt; font-weight:800; line-height:1; }
.vans .vst .k { font-family:'Be Vietnam Pro',sans-serif; font-size:7.3pt; color:#dbe3f2; margin-top:3pt; line-height:1.3; max-width:22mm; }
.tier { border:0.8pt solid #cfd8e6; border-radius:5pt; margin:7pt 0 0 0; }
.tier .th { display:flex; align-items:baseline; gap:8pt; padding:5pt 9pt; color:#fff; font-family:'Be Vietnam Pro',sans-serif; border-radius:4pt 4pt 0 0; break-after:avoid; }
.tier .th b { font-size:10pt; font-weight:800; } .tier .th span { font-size:8pt; opacity:.92; }
.tier.r .th { background:""" + RED + """; } .tier.o .th { background:""" + ORANGE + """; } .tier.g .th { background:""" + GREEN + """; }
.tier .it { display:grid; grid-template-columns: 1fr 36mm; gap:8pt; padding:4pt 9pt 4.5pt 9pt; border-top:0.6pt solid #e3e8ef; break-inside:avoid; }
.tier .it h4 { font-size:9.5pt; font-weight:700; color:""" + NAVY + """; line-height:1.3; }
.tier .it p { font-size:9.2pt; margin:1.5pt 0 0 0; text-align:left; line-height:1.42; }
.tier .it .m { text-align:right; font-family:'Be Vietnam Pro',sans-serif; }
.tier .it .m .amt { font-size:11.5pt; font-weight:800; color:""" + NAVY2 + """; }
.tier .it .m .rl { font-size:7.5pt; color:#3d4656; margin-top:2pt; line-height:1.3; }
.tier .it .m .cd { font-size:7.3pt; color:#6a7384; margin-top:1pt; }
.tier.g .it { grid-template-columns: 1fr; }
.tier.g .its { display:grid; grid-template-columns: 1fr 1fr; }
.tier.g .its .it:nth-child(2) { border-left:0.6pt solid #e3e8ef; } .tier.g .its .it:nth-child(4) { border-left:0.6pt solid #e3e8ef; }
table.ic td, table.ic th { padding:2.6pt 4pt; font-size:8.8pt; }
table.ic th { white-space:normal; }
table.scd .stp { white-space:nowrap; }
table.scd td { padding:2.8pt 5pt; }
.keysbox { display:grid; grid-template-columns: repeat(3, 1fr); gap:6pt; margin:3pt 0 6pt 0; break-inside:avoid; }
.keysbox div { background:""" + CREAM + """; border-left:3pt solid """ + GOLD + """; border-radius:0 4pt 4pt 0; padding:5pt 8pt; font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; line-height:1.4; color:#16294A; }
.keysbox.k4 { grid-template-columns: 1fr 1fr; }
.keysbox div b { display:block; font-size:13pt; color:""" + GOLD + """; line-height:1; margin-bottom:2pt; }
.tln { margin:3pt 0 4pt 0; border-top:0.8pt solid #cfd8e6; }
.tln .r { display:grid; grid-template-columns: 25mm 9pt 1fr 25mm 17mm; gap:6pt; align-items:start; padding:2.3pt 0; border-bottom:0.5pt solid #e3e8ef; break-inside:avoid; }
.tln .d { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; font-weight:700; color:""" + NAVY + """; line-height:1.35; }
.tln .dot { width:8pt; height:8pt; border-radius:50%; margin-top:2.5pt; }
.tln .x { font-size:9.2pt; line-height:1.4; }
.tln .v { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; font-weight:700; text-align:right; white-space:nowrap; line-height:1.35; }
.tln .c { font-family:'Be Vietnam Pro',sans-serif; font-size:7.4pt; color:#5a6475; text-align:right; line-height:1.35; }
.gl { display:grid; grid-template-columns: 1fr 1fr; gap:0 12pt; margin:3pt 0 6pt 0; }
.gl div { padding:3pt 0; border-bottom:0.5pt solid #e3e8ef; font-size:9pt; line-height:1.4; break-inside:avoid; text-align:left; }
.gl div b { font-family:'Be Vietnam Pro',sans-serif; font-size:8.5pt; color:""" + NAVY + """; display:block; }
.kl { border:0.9pt solid #cfd8e6; border-left:4pt solid """ + NAVY + """; border-radius:0 5pt 5pt 0; padding:6pt 10pt 6pt 10pt; margin:0 0 8pt 0; background:#fff; break-inside:avoid; }
.kl.r { border-left-color:""" + RED + """; } .kl.o { border-left-color:""" + ORANGE + """; } .kl.g { border-left-color:""" + GREEN + """; } .kl.n { border-left-color:""" + NAVY + """; }
.kl .kh { display:flex; align-items:center; gap:8pt; margin-bottom:2pt; }
.kl .kh .lab { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; font-weight:800; letter-spacing:.1em; color:""" + NAVY + """; }
.kl .kt div { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; line-height:1.45; color:#16294A; margin:1pt 0; text-align:left; }
.kl .kt div.first { font-weight:700; }
.part { background:""" + NAVY + """; color:#fff; border-radius:6pt; padding:10pt 14pt 11pt 14pt; margin:0 0 9pt 0; break-after:avoid; break-inside:avoid; position:relative; overflow:hidden; }
.part:after { content:''; position:absolute; right:-18mm; top:-18mm; width:52mm; height:52mm; border-radius:50%; background:rgba(200,153,47,.16); }
.part .pn { font-family:'Be Vietnam Pro',sans-serif; font-size:8.6pt; font-weight:800; letter-spacing:.16em; color:#f1d98f; }
.part .pt { font-family:'Be Vietnam Pro',sans-serif; font-size:17pt; font-weight:800; line-height:1.2; margin-top:2pt; }
.part .pd { font-family:'Be Vietnam Pro',sans-serif; font-size:8.8pt; color:#dbe3f2; margin-top:3pt; line-height:1.4; max-width:140mm; }
.tocp { break-after:page; }
.tocp h1 { font-family:'Be Vietnam Pro',sans-serif; font-size:20pt; font-weight:800; color:""" + NAVY + """; margin:0 0 8pt 0; }
.tocp .pg { margin:8pt 0 0 0; break-inside:avoid; }
.tocp .ph { display:flex; align-items:baseline; gap:8pt; border-bottom:1.2pt solid """ + NAVY + """; padding-bottom:2pt; }
.tocp .ph .n { font-family:'Be Vietnam Pro',sans-serif; font-size:8.4pt; font-weight:800; letter-spacing:.14em; color:#8A6A1E; min-width:15mm; }
.tocp .ph .t { font-family:'Be Vietnam Pro',sans-serif; font-size:11.5pt; font-weight:800; color:""" + NAVY + """; flex:1; }
.tocp .ph .p { font-family:'Be Vietnam Pro',sans-serif; font-size:10pt; font-weight:800; color:""" + NAVY + """; }
.tocp .pdsc { font-size:8.8pt; color:#3d4656; margin:2pt 0 2pt 23mm; font-family:'Be Vietnam Pro',sans-serif; }
.tocp .row { display:flex; align-items:center; gap:6pt; padding:2.6pt 0; border-bottom:0.5pt dotted #b9c3d3; }
.tocp .row a { color:inherit; text-decoration:none; }
.tocp .row .no { font-family:'Be Vietnam Pro',sans-serif; font-size:9.5pt; font-weight:800; color:""" + GOLD + """; min-width:15mm; text-align:right; padding-right:8mm; }
.tocp .row .tt { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; color:#16294A; flex:1; }
.tocp .row .p { font-family:'Be Vietnam Pro',sans-serif; font-size:9.6pt; font-weight:700; color:""" + NAVY + """; min-width:8mm; text-align:right; }
.sec-h .sic { flex:0 0 auto; }
.figbox { border:0.8pt solid #cfd8e6; border-radius:6pt; padding:6pt 7pt 4pt 7pt; margin:4pt 0 6pt 0; break-inside:avoid; background:#fff; }
.figbox svg { width:100%; height:auto; display:block; }
.figbox.fl svg { width:88%; margin:0 auto; }
.dn { display:grid; grid-template-columns: 48mm 1fr; gap:10pt; align-items:center; margin:2pt 0 6pt 0; break-inside:avoid; }
.dn svg { width:48mm; height:48mm; display:block; }
.dn .lg div { display:flex; align-items:center; gap:7pt; padding:3pt 0; border-bottom:0.5pt solid #e3e8ef; font-family:'Be Vietnam Pro',sans-serif; font-size:9pt; }
.dn .lg i { width:10pt; height:10pt; border-radius:3pt; display:inline-block; flex:0 0 auto; }
.dn .lg b { font-size:12pt; min-width:8mm; }
.pb { break-before: page; }
.avoid { break-inside: avoid; }
"""

def sentences(t):
    if isinstance(t, (list, tuple)): return list(t)
    parts = re.split(r'(?<=[\.\!\?])\s+(?=[A-ZĐÀ-Ỹ0-9"“(])', t.strip())
    return [p.strip() for p in parts if p.strip()]

def nd(text, label="NHẬN ĐỊNH", gold=False):
    ss = sentences(text)
    lis = "".join(f'<li class="{"first" if i == 0 else ""}">{E(s)}</li>' for i, s in enumerate(ss))
    return f'<div class="nd{" gold" if gold else ""}"><div class="lbl">{E(label)}</div><ul>{lis}</ul></div>'

def sec(no, title):
    from viz import icon
    return f'<div class="sec-h" id="sec-{no}">{icon(no)}<span class="no">{no}</span><h2>{E(title)}</h2></div>'

def table(headers, rows, cls=None, widths=None, row_cls=None, total=None, esc=True, tcls=""):
    ncls = cls or [""] * len(headers)
    cg = "".join(f'<col style="width:{w}">' for w in widths) if widths else ""
    th = "".join(f'<th class="{ncls[i]}">{E(h)}</th>' for i, h in enumerate(headers))
    body = ""
    for ri, r in enumerate(rows):
        rc = row_cls[ri] if row_cls else ""
        body += f'<tr class="{rc}">' + "".join(f'<td class="{ncls[i]}">{(E(v) if esc else v) if v is not None else ""}</td>' for i, v in enumerate(r)) + "</tr>"
    if total:
        body += '<tr class="tot">' + "".join(f'<td class="{ncls[i]}">{E(v) if v is not None else ""}</td>' for i, v in enumerate(total)) + "</tr>"
    return f'<table class="{tcls}"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

def src(t): return f'<div class="src">Nguồn: {E(t)}</div>'
def kick(t): return f'<div class="kick">{t}</div>'

# ------------------------------------------------------------------ SVG charts
def svg_waterfall(steps, y0=120e9, y1=131e9, W=660, H=250):
    m = dict(l=34, r=8, t=18, b=46); iw = W - m["l"] - m["r"]; ih = H - m["t"] - m["b"]
    y = lambda v: m["t"] + ih - (v - y0) / (y1 - y0) * ih
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Be Vietnam Pro, sans-serif">']
    for v in range(120, 131, 2):
        yy = y(v * 1e9)
        out.append(f'<line x1="{m["l"]}" x2="{W-m["r"]}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{"#9aa6b8" if v == 120 else "#e1e6ee"}" stroke-width="0.8"/>')
        out.append(f'<text x="{m["l"]-5}" y="{yy+3:.1f}" font-size="8" fill="#6a7384" text-anchor="end">{v}</text>')
    n = len(steps); bw = iw / n; run = 0
    for i, s in enumerate(steps):
        w = min(bw * 0.58, 46); x = m["l"] + i * bw + (bw - w) / 2
        if s["t"] == "total":
            top, bot, col = y(s["v"]), y(y0), NAVY; run = s["v"]
        else:
            a, b = run, run + s["v"]; top, bot = y(max(a, b)), y(min(a, b)); col = GREEN if s["v"] > 0 else ORANGE; run = b
        h = max(bot - top, 1.6)
        out.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2" fill="{col}"/>')
        if s["t"] == "total":
            out.append(f'<path d="M{x-1:.1f} {bot-6:.1f} l5 -4 l5 4 l5 -4 l5 4 l5 -4 l5 4 l5 -4 l5 4 l5 -4" stroke="#fff" stroke-width="2.4" fill="none"/>')
        if i < n - 1:
            ny = y(run); out.append(f'<line x1="{x+w:.1f}" x2="{x+bw:.1f}" y1="{ny:.1f}" y2="{ny:.1f}" stroke="#9aa6b8" stroke-width="0.7"/>')
        lab = ty(s["v"], 2) if s["t"] == "total" else ("+" if s["v"] > 0 else "−") + ty(abs(s["v"]), 3 if abs(s["v"]) < 1e7 else 2)
        out.append(f'<text x="{x+w/2:.1f}" y="{top-4:.1f}" font-size="8.6" font-weight="700" fill="#16294A" text-anchor="middle">{lab}</text>')
        words = s["l"].split(); lines = []; cur = ""
        for wd in words:
            if len((cur + " " + wd).strip()) > 16 and cur: lines.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            out.append(f'<text x="{m["l"]+i*bw+bw/2:.1f}" y="{H-m["b"]+12+j*10:.1f}" font-size="7.6" fill="#3d4656" text-anchor="middle">{E(ln)}</text>')
    out.append("</svg>")
    return "".join(out)

def svg_hbars(items, W=660, rowH=22, labW=250, fmt=None, maxv=None, ref=None, ref_label=None, ticks=None):
    m = dict(t=14 if ref else 4, b=16 if ticks else 4, r=64); H = m["t"] + m["b"] + rowH * len(items)
    mx = maxv or max(i["v"] for i in items); iw = W - labW - m["r"]
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Be Vietnam Pro, sans-serif">']
    if ticks:
        for t, lab in ticks:
            xx = labW + t / mx * iw
            out.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{m["t"]}" y2="{H-m["b"]}" stroke="#e1e6ee" stroke-width="0.7"/>')
            out.append(f'<text x="{xx:.1f}" y="{H-m["b"]+10}" font-size="7.4" fill="#6a7384" text-anchor="middle">{lab}</text>')
    for i, it in enumerate(items):
        yy = m["t"] + i * rowH; bh = min(12, rowH - 8); by = yy + (rowH - bh) / 2
        words = it["l"].split(); lines = []; cur = ""
        for wd in words:
            if len((cur + " " + wd).strip()) > 44 and cur: lines.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            off = (j - (0.5 if len(lines) > 1 else 0)) * 9
            out.append(f'<text x="0" y="{yy+rowH/2+3+off:.1f}" font-size="7.8" fill="#222">{E(ln)}</text>')
        w = max(1.5, it["v"] / mx * iw)
        out.append(f'<rect x="{labW}" y="{by:.1f}" width="{w:.1f}" height="{bh}" rx="2" fill="{it.get("col", NAVY)}"/>')
        out.append(f'<text x="{labW+w+4:.1f}" y="{by+bh/2+3:.1f}" font-size="8" font-weight="700" fill="#16294A">{fmt(it["v"]) if fmt else tr(it["v"])}</text>')
    out.append(f'<line x1="{labW}" x2="{labW}" y1="{m["t"]}" y2="{H-m["b"]}" stroke="#9aa6b8" stroke-width="0.8"/>')
    if ref is not None:
        xx = labW + ref / mx * iw
        out.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{m["t"]-6}" y2="{H-m["b"]}" stroke="{RED}" stroke-width="1" stroke-dasharray="3 2"/>')
        out.append(f'<text x="{xx:.1f}" y="{m["t"]-8}" font-size="7.6" fill="{RED}" text-anchor="middle" font-weight="700">{E(ref_label or "")}</text>')
    out.append("</svg>")
    return "".join(out)

def svg_line(series, W=660, H=180, ymax=10e9, thr=1e9):
    m = dict(l=30, r=8, t=10, b=20); iw = W - m["l"] - m["r"]; ih = H - m["t"] - m["b"]
    import datetime as dt
    P = lambda s: dt.date.fromisoformat(s)
    t0, t1 = P(series[0][0]), P(series[-1][0]); span = (t1 - t0).days
    x = lambda d: m["l"] + (P(d) - t0).days / span * iw; y = lambda v: m["t"] + ih - v / ymax * ih
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Be Vietnam Pro, sans-serif">']
    for v in range(0, 11, 2):
        yy = y(v * 1e9); out.append(f'<line x1="{m["l"]}" x2="{W-m["r"]}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{"#9aa6b8" if v == 0 else "#e8ecf2"}" stroke-width="0.7"/>')
        out.append(f'<text x="{m["l"]-4}" y="{yy+3:.1f}" font-size="7.4" fill="#6a7384" text-anchor="end">{v}</text>')
    for d in ["2024-09-01", "2025-01-01", "2025-05-01", "2025-09-01", "2026-01-01", "2026-05-01"]:
        out.append(f'<text x="{x(d):.1f}" y="{H-6}" font-size="7.4" fill="#6a7384" text-anchor="middle">{d[5:7]}/{d[2:4]}</text>')
    pts = " ".join(f"{x(d):.1f},{y(b):.1f}" for d, b in series)
    area = f"M{x(series[0][0]):.1f},{y(0):.1f} L" + " L".join(f"{x(d):.1f},{y(b):.1f}" for d, b in series) + f" L{x(series[-1][0]):.1f},{y(0):.1f} Z"
    out.append(f'<path d="{area}" fill="{NAVY}" fill-opacity="0.10"/>')
    out.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="1.4" stroke-linejoin="round"/>')
    ty_ = y(thr); out.append(f'<line x1="{m["l"]}" x2="{W-m["r"]}" y1="{ty_:.1f}" y2="{ty_:.1f}" stroke="{ORANGE}" stroke-width="1" stroke-dasharray="4 3"/>')
    out.append(f'<text x="{W-m["r"]}" y="{ty_-3:.1f}" font-size="7.4" fill="{ORANGE}" text-anchor="end" font-weight="700">Mức cần giữ 1 tỷ</text>')
    peak = max(series, key=lambda p: p[1])
    out.append(f'<text x="{x(peak[0])+5:.1f}" y="{y(peak[1])+3:.1f}" font-size="7.4" fill="#16294A">9,22 tỷ ngày 29/08/2025</text>')
    out.append("</svg>")
    return "".join(out)
