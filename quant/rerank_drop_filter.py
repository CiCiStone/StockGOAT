# -*- coding: utf-8 -*-
"""超跌+换手率异动筛选 + 双维度 Rerank + HTML 报表（数据源：本地 SQLite）"""
import os, sqlite3
from collections import defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(BASE, "..", "dataset", "stock_daily.db"))
OUT = os.path.normpath(os.path.join(BASE, "..", "skills", "stock-drop-filter", "output"))
os.makedirs(OUT, exist_ok=True)

LOOKBACK, DROP, TURN_DELTA, TURN_ABS, TURN_RATE, STAB, TOPN = 60, 0.28, 1.0, 8.0, 1.5, 10, 20


def load():
    c = sqlite3.connect(DB)
    names = {r[0]: r[1] for r in c.execute("SELECT code,name FROM stock_basic")}
    rows = c.execute("SELECT code,date,close,turn FROM daily_k ORDER BY code,date").fetchall()
    c.close()
    by = defaultdict(list)
    for code, d, close, turn in rows:
        by[code].append((d, close, turn))
    return names, by


def screen(names, by):
    both, c1 = [], 0
    for code, s in by.items():
        if len(s) < STAB + 2:
            continue
        recent = s[-LOOKBACK:]
        ld, lc, lt = recent[-1]
        if lc is None or lc <= 0:
            continue
        closes = [x for _, x, _ in recent if x is not None]
        pk = max(closes)
        pd = recent[closes.index(pk)][0]
        drop = (pk - lc) / pk * 100
        if drop < DROP * 100:
            continue
        c1 += 1
        pt = recent[-2][2] if len(recent) >= 2 else 0
        p2 = recent[-3][2] if len(recent) >= 3 else 0
        lt = lt if lt is not None else 0
        pt = pt if pt is not None else 0
        if not (lt > pt + TURN_DELTA or lt >= TURN_ABS or lt / (pt + 1e-9) >= TURN_RATE):
            continue
        wc = [x for _, x, _ in s[-STAB:] if x is not None]
        if len(wc) < 3:
            continue
        ma = sum(wc) / len(wc)
        stab = (lc / ma - 1) * 100 if ma > 0 else 0.0
        both.append(dict(code=code, code_name=names.get(code, ""), peak_close=round(pk, 2),
                         peak_date=pd, last_close=round(lc, 2), drop_pct=round(drop, 2),
                         last_turn=round(lt, 2), prev_turn=round(pt, 2), prev2_turn=round(p2, 2),
                         stab=round(stab, 2), last_date=ld))
    return both, c1


def rerank(both):
    td = sorted(both, key=lambda x: x["drop_pct"], reverse=True)[:TOPN]
    ts = sorted(both, key=lambda x: x["stab"], reverse=True)[:TOPN]
    m = {r["code"]: r for r in td + ts}
    merged = list(m.values())

    def norm(v):
        lo, hi = min(v), max(v)
        return [(x - lo) / (hi - lo) if hi > lo else 0.5 for x in v]

    dn, sn = norm([r["drop_pct"] for r in merged]), norm([r["stab"] for r in merged])
    for r, d, s in zip(merged, dn, sn):
        r["drop_norm"], r["stab_norm"], r["score"] = round(d, 3), round(s, 3), round(0.5 * d + 0.5 * s, 4)
    top5 = sorted(merged, key=lambda x: x["score"], reverse=True)[:5]
    return td, ts, merged, top5


HEAD = ["代码", "名称", "最新收盘", "60日最高", "最高价日期", "跌幅%", "最新换手%", "前日换手%", "企稳%", "最新交易日"]
KEY = ["code", "code_name", "last_close", "peak_close", "peak_date", "drop_pct", "last_turn", "prev_turn", "stab", "last_date"]
H5 = ["排名", "代码", "名称", "跌幅%", "企稳%", "跌幅分", "企稳分", "加权分"]
K5 = ["code", "code_name", "drop_pct", "stab", "drop_norm", "stab_norm", "score"]


def tbl(rows, head, key, top5=False):
    if not rows:
        return '<div class="no-data">暂无数据</div>'
    h = "<table><thead><tr>" + "".join(f"<th>{x}</th>" for x in head) + "</tr></thead><tbody>"
    for i, r in enumerate(rows):
        h += "<tr>"
        if top5:
            h += f'<td><span class="rank rank-{i+1}">{i+1}</span></td>'
        for k in key:
            v = r.get(k, "")
            cls = ""
            if k == "drop_pct":
                fv = float(v)
                cls = "drop-high" if fv >= 40 else ("drop-mid" if fv >= 30 else "drop-low")
            elif k == "stab":
                fv = float(v)
                cls = "stab-pos" if fv > 0 else ("stab-neg" if fv < -10 else "")
            h += f'<td class="{cls}">{v}</td>'
        h += "</tr>"
    return h + "</tbody></table>"


CSS = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;background:#0f172a;color:#e2e8f0;padding:24px}
.container{max-width:1400px;margin:0 auto}h1{text-align:center;font-size:26px;color:#f8fafc;margin-bottom:6px}
.subtitle{text-align:center;color:#94a3b8;font-size:13px;margin-bottom:22px;line-height:1.6}
.summary{display:flex;gap:14px;justify-content:center;margin-bottom:26px;flex-wrap:wrap}
.card{background:#1e293b;border-radius:12px;padding:16px 24px;text-align:center;min-width:130px;border:1px solid #334155}
.card .num{font-size:30px;font-weight:700}.card .label{font-size:12px;color:#94a3b8;margin-top:4px}
.red .num{color:#f87171}.green .num{color:#4ade80}.orange .num{color:#fb923c}.blue .num{color:#60a5fa}.purple .num{color:#c084fc}.slate .num{color:#e2e8f0}
.section{margin-bottom:24px}.section-title{font-size:17px;font-weight:700;margin-bottom:10px;color:#f1f5f9}
.badge{font-size:12px;padding:2px 10px;border-radius:20px;color:#fff;font-weight:600;margin-right:6px}
.badge-red{background:#dc2626}.badge-green{background:#16a34a}.badge-orange{background:#ea580c}.badge-purple{background:#7c3aed}
table{width:100%;border-collapse:collapse;background:#1e293b;border-radius:10px;overflow:hidden;font-size:13px}
th{background:#0f172a;color:#94a3b8;padding:10px 8px;text-align:left;white-space:nowrap;font-weight:600}
td{padding:8px;border-bottom:1px solid #334155}tr:hover td{background:#283548}
.drop-high{color:#f87171;font-weight:700}.drop-mid{color:#fb923c;font-weight:600}.drop-low{color:#fbbf24}
.stab-pos{color:#4ade80;font-weight:600}.stab-neg{color:#f87171}
.rank{display:inline-block;width:24px;height:24px;line-height:24px;text-align:center;border-radius:6px;font-weight:700;color:#fff}
.rank-1{background:#dc2626}.rank-2{background:#ea580c}.rank-3{background:#f59e0b}.rank-4{background:#64748b}.rank-5{background:#475569}
.no-data{text-align:center;padding:30px;color:#64748b}
.note{background:#1e293b;border-left:3px solid #f59e0b;padding:12px 16px;border-radius:8px;font-size:13px;color:#cbd5e1;margin-top:20px}
.footer{text-align:center;color:#64748b;font-size:12px;margin-top:30px}"""


def render(td, ts, merged, top5, both, c1, stats):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lt = stats["latest"]
    t1, t2 = tbl(td, HEAD, KEY), tbl(ts, HEAD, KEY)
    t3 = tbl(sorted(both, key=lambda x: x["drop_pct"], reverse=True), HEAD, KEY)
    t5 = tbl(top5, H5, K5, True)
    body = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>超跌筛选 Rerank 报表</title><style>{css}</style></head><body><div class="container">
<h1>超跌 + 换手率异动 · Rerank 报表</h1>
<p class="subtitle">数据源：本地 SQLite（baostock 不复权）｜ 最新交易日：{lt} ｜ 回溯 {lb} 交易日 ｜ 跌幅阈值 {dr}% ｜ 换手率差值&gt;{tde}% 或&gt;={ta}% 或比值&gt;={tr}<br>生成：{now} ｜ Rerank：维度1(跌幅)与维度2(企稳)各取 top{tn}，去重后 0.5:0.5 加权</p>
<div class="summary">
<div class="card slate"><div class="num">{tot}</div><div class="label">本地股票数</div></div>
<div class="card red"><div class="num">{c1}</div><div class="label">条件一命中</div></div>
<div class="card orange"><div class="num">{bc}</div><div class="label">同时命中两条件</div></div>
<div class="card green"><div class="num">{nd}</div><div class="label">维度1 top{tn}</div></div>
<div class="card blue"><div class="num">{ns}</div><div class="label">维度2 top{tn}</div></div>
<div class="card purple"><div class="num">{n5}</div><div class="label">最优标的</div></div></div>
<div class="section"><div class="section-title"><span class="badge badge-purple">最优</span>加权后最优 {n5} 只（55开）</div>{t5}</div>
<div class="section"><div class="section-title"><span class="badge badge-red">维度1</span>跌幅最大 top{tn}</div>{t1}</div>
<div class="section"><div class="section-title"><span class="badge badge-green">维度2</span>企稳最好 top{tn}</div>{t2}</div>
<div class="section"><div class="section-title"><span class="badge badge-orange">同时命中</span>条件一+条件二 全部（{bc}只）</div>{t3}</div>
<div class="note">企稳指标=最新收盘/近10日均价-1，正值=止跌反弹，负值=仍下跌。加权分=0.5×跌幅归一化+0.5×企稳归一化（去重池内 min-max）。仅覆盖本地已拉取 {tot} 只（全市场约5000只），仅供参考。</div>
<div class="footer">Generated by rerank_drop_filter.py | {now}</div></div></body></html>"""
    repl = dict(css=CSS, lt=lt, lb=str(LOOKBACK), dr=str(int(DROP * 100)), tde=str(TURN_DELTA),
                ta=str(TURN_ABS), tr=str(TURN_RATE), now=now, tn=str(TOPN), tot=str(stats["total"]),
                c1=str(c1), bc=str(len(both)), nd=str(len(td)), ns=str(len(ts)), n5=str(len(top5)),
                t5=t5, t1=t1, t2=t2, t3=t3)
    for k, v in repl.items():
        body = body.replace("{" + k + "}", v)
    ts_ = datetime.now().strftime("%Y%m%d_%H%M%S")
    p = os.path.join(OUT, f"rerank_report_{ts_}.html")
    open(p, "w", encoding="utf-8").write(body)
    return p


def main():
    names, by = load()
    both, c1 = screen(names, by)
    latest = max((s[-1][0] for s in by.values() if s), default="N/A")
    stats = {"total": len(by), "latest": latest}
    td, ts, merged, top5 = rerank(both)
    p = render(td, ts, merged, top5, both, c1, stats)
    print(f"本地股票: {len(by)} | 最新交易日: {latest}")
    print(f"条件一: {c1} | 同时命中: {len(both)}")
    print(f"维度1 top{TOPN}: {[r['code'] for r in td]}")
    print(f"维度2 top{TOPN}: {[r['code'] for r in ts]}")
    print(f"去重池: {len(merged)} | 最优5: {[(r['code'], r['score']) for r in top5]}")
    print(f"报表: {p}")


if __name__ == "__main__":
    main()
