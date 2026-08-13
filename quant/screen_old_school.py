# -*- coding: utf-8 -*-
"""
老登股（公用事业/自然资源周期股）跌幅榜筛选 + 企稳审查 + HTML 报表

流程：
  1. 从本地 SQLite 计算每只股票 60 日跌幅、企稳系数（最新收盘/近10日均价-1）
  2. 用关键词识别"老登股"（公用事业 + 自然资源周期股）
  3. 输出跌幅榜老登股 top（跌幅降序）
  4. 审查企稳系数 > -2% 的标的
  5. 人工精选 5 只"长期向好"标的（战略金属 + 公用事业），附调研结论
  6. 生成 HTML 报表

用法： conda activate eastmoney && python quant/screen_old_school.py
"""
import os, sqlite3
from collections import defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(BASE, "..", "dataset", "stock_daily.db"))
OUT = os.path.normpath(os.path.join(BASE, "..", "output"))
os.makedirs(OUT, exist_ok=True)

LOOKBACK = 60
STAB_WIN = 10
DROP_MIN = 28.0   # 跌幅榜 top 口径
STAB_MIN = -2.0   # 企稳审查阈值

KW = ["电力", "水电", "火电", "风电", "光伏", "太阳能", "新能源", "能源", "热电", "核电",
      "发电", "电网", "水务", "自来水", "供水", "燃气", "天然气", "供热", "供暖", "环保",
      "环境", "环卫", "生态", "煤", "焦", "铜", "铝", "锌", "铅", "镍", "锡", "黄金",
      "白银", "稀土", "锂", "钴", "钼", "钨", "矿业", "矿", "资源", "有色", "金属",
      "钢", "铁", "石油", "石化", "油气", "油服", "化工", "化学", "农业", "种业",
      "种植", "农", "牧", "养殖", "饲料", "糖", "化肥", "农药", "粮食", "棉", "橡胶",
      "渔业", "林业", "港口", "公路", "铁路", "机场", "航空", "海运", "航运", "物流"]

# 人工精选的 5 只"长期向好"标的（数据来自公开财报/研报，2026-08 时点）
PICKS = {
    "sh.600549": dict(
        name="厦门钨业", theme="钨战略金属", drop_note="跌幅最深之一",
        logic="钨钼/稀土/能源新材料三主业；钨战略金属（开采指标管控+硬质合金/刀具/光伏钨丝需求）；2026Q1 归母 11.07 亿(+89%)创历史新高。",
        fin="2025 营收 462.65 亿(+30.79%)，归母 23.09 亿(+34.89%)，连续 5 年增长；10 派 4 元。",
        risk="钨价/稀土价格波动；锂电正极受碳酸锂价格拖累；Q1 经营现金流为负。"),
    "sh.600392": dict(
        name="盛和资源", theme="稀土出海", drop_note="跌幅 33.7%",
        logic="全球稀土全产业链龙头（实控人财政部），'中国+美国+非洲'三极资源布局，不受国内配额约束；稀土出口管制+机器人/新能源需求。",
        fin="2025 归母净利同比 +305%；完成 Peak 稀土 100% 股权收购，海外布局加速。",
        risk="稀土价格高位回落风险；海外矿山爬坡不及预期；地缘政策风险。"),
    "sh.600301": dict(
        name="华锡有色", theme="锡锑战略金属", drop_note="企稳最好(+3.3%)",
        logic="广西关键金属集团唯一上市平台；锡锑双主业，锑为战略金属（供给刚性+光伏玻璃澄清剂+军工需求），锡锑供需缺口长期存在；体外矿山资产注入预期。",
        fin="2025-2027 归母预测 9.8/15.x 亿元；2025Q1 锡/银/铅锑精矿均价同比 +20.2%/+14.5%/+75.8%。",
        risk="锡锑价格高位波动；资产注入节奏不确定；海外复产（佤邦）供给冲击。"),
    "sh.600021": dict(
        name="上海电力", theme="电力新能源", drop_note="公用事业代表",
        logic="五大发电央企旗下平台；清洁能源装机占比突破 62%，风电光伏装机近半；新能源发电量同比 +21.16%，为业绩核心驱动。",
        fin="2025 营收 418.58 亿，归母 27.67 亿(+35%)；煤电受益煤价下行。",
        risk="电价市场化竞争；煤价反弹；新能源平价后电价走低。"),
    "sh.601958": dict(
        name="金钼股份", theme="钼全球龙头", drop_note="基本面最硬",
        logic="全球钼龙头（市占率约 13%）；钼从'钢铁配套'向'高端制造战略原料'价值重估（特钢/军工/新能源）；资产负债率仅 11.5%，累计分红 116 亿。",
        fin="2025 营收 138.34 亿(+1.94%)，归母 31.55 亿(+5.77%)；钼精矿价格维持 4400 元/吨度高位。",
        risk="钼价高位震荡，股价部分透支远期预期；下游特钢需求波动。"),
}


def load():
    c = sqlite3.connect(DB)
    names = {r[0]: r[1] for r in c.execute("SELECT code, name FROM stock_basic")}
    ipo = {r[0]: (r[1] or "")[:4] for r in c.execute("SELECT code, ipo_date FROM stock_basic")}
    rows = c.execute("SELECT code, date, close, turn FROM daily_k ORDER BY code, date").fetchall()
    c.close()
    by = defaultdict(list)
    for code, d, close, turn in rows:
        by[code].append((d, close, turn))
    return names, ipo, by


def screen(names, ipo, by):
    res = []
    for code, s in by.items():
        name = names.get(code, "")
        if not any(k in name for k in KW):
            continue
        if len(s) < 15:
            continue
        closes = [x for _, x, _ in s[-LOOKBACK:] if x is not None]
        if not closes:
            continue
        pk = max(closes)
        lc = closes[-1]
        drop = (pk - lc) / pk * 100 if pk else 0
        w = closes[-STAB_WIN:]
        ma = sum(w) / len(w)
        stab = (lc / ma - 1) * 100 if ma else 0
        res.append(dict(code=code, name=name, drop=round(drop, 2), stab=round(stab, 2),
                        close=round(lc, 2), peak=round(pk, 2), ipo=ipo.get(code, "")))
    res.sort(key=lambda x: x["drop"], reverse=True)
    return res


def main():
    names, ipo, by = load()
    res = screen(names, ipo, by)
    top = [r for r in res if r["drop"] >= DROP_MIN]
    stable = [r for r in res if r["drop"] >= DROP_MIN and r["stab"] > STAB_MIN]
    latest = max((s[-1][0] for s in by.values() if s), default="N/A")
    picks = [dict(r, **PICKS[r["code"]]) for r in res if r["code"] in PICKS]

    print(f"老登股总数: {len(res)} | 最新交易日: {latest}")
    print(f"跌幅>=28%: {len(top)} | 其中企稳>-2%: {len(stable)}")
    print("\n=== 精选 5 只 ===")
    for r in picks:
        print(f"{r['code']} {r['name']} 跌幅{r['drop']}% 企稳{r['stab']:+.2f}%")

    render_html(res, top, stable, picks, latest)
    print(f"\n报表: {os.path.join(OUT, 'old_school_report.html')}")


def render_html(res, top, stable, picks, latest):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    def row_html(r, extra=False):
        s = f"<tr><td>{r['code']}</td><td>{r['name']}</td><td class='drop'>{r['drop']:.2f}%</td>"
        s += f"<td class='{'pos' if r['stab']>0 else 'neg'} stab'>{r['stab']:+.2f}%</td>"
        s += f"<td>{r['close']:.2f}</td><td>{r['peak']:.2f}</td><td>{r['ipo']}</td></tr>"
        return s

    top_rows = "\n".join(row_html(r) for r in top[:40])
    pick_cards = []
    for i, r in enumerate(picks, 1):
        pick_cards.append(f"""
<div class="pick">
  <div class="pick-head"><span class="p-rank">#{i}</span><span class="p-name">{r['name']}（{r['code']}）</span><span class="p-theme">{r['theme']}</span></div>
  <div class="p-meta">跌幅 <b class="drop">{r['drop']:.2f}%</b> ｜ 企稳 <b class="{'pos' if r['stab']>0 else 'neg'}">{r['stab']:+.2f}%</b> ｜ 60日最高 {r['peak']:.2f} ｜ 最新收盘 {r['close']:.2f} ｜ {r['drop_note']}</div>
  <div class="p-block"><div class="p-label">长期向好逻辑</div><div class="p-body">{r['logic']}</div></div>
  <div class="p-block"><div class="p-label">财务要点</div><div class="p-body">{r['fin']}</div></div>
  <div class="p-block"><div class="p-label">风险提示</div><div class="p-body risk">{r['risk']}</div></div>
</div>""")

    css = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;background:#0f172a;color:#e2e8f0;padding:24px;line-height:1.7}
.wrap{max-width:1280px;margin:0 auto}
h1{font-size:24px;color:#f8fafc;text-align:center;margin-bottom:6px}
.sub{color:#94a3b8;font-size:13px;text-align:center;margin-bottom:22px;line-height:1.6}
.cards{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:26px}
.card{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:16px 24px;text-align:center;min-width:130px}
.card .n{font-size:28px;font-weight:700}.card .l{font-size:12px;color:#94a3b8;margin-top:4px}
.c-red .n{color:#f87171}.c-green .n{color:#4ade80}.c-orange .n{color:#fb923c}.c-blue .n{color:#60a5fa}.c-purple .n{color:#c084fc}
.sec{margin-bottom:26px}.sec h2{font-size:18px;font-weight:700;color:#f1f5f9;margin-bottom:12px;border-left:4px solid #f59e0b;padding-left:10px}
table{width:100%;border-collapse:collapse;background:#1e293b;border-radius:10px;overflow:hidden;font-size:13px}
th{background:#0f172a;color:#94a3b8;padding:10px 8px;text-align:left;font-weight:600}
td{padding:8px;border-bottom:1px solid #334155}tr:hover td{background:#283548}
.drop{color:#f87171;font-weight:700}.pos{color:#4ade80;font-weight:600}.neg{color:#f87171}
.pick{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px;margin-bottom:16px}
.pick-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.p-rank{background:#f59e0b;color:#0f172a;font-weight:700;width:26px;height:26px;line-height:26px;text-align:center;border-radius:8px;display:inline-block}
.p-name{font-size:17px;font-weight:700;color:#f8fafc}
.p-theme{font-size:12px;padding:2px 10px;border-radius:20px;background:#7c3aed;color:#fff}
.p-meta{font-size:13px;color:#cbd5e1;margin-bottom:10px}
.p-block{margin:8px 0}.p-label{font-size:12px;color:#94a3b8;margin-bottom:2px}
.p-body{font-size:13.5px;color:#e2e8f0}.risk{color:#fca5a5}
.note{background:#1e293b;border-left:3px solid #f59e0b;padding:12px 16px;border-radius:8px;font-size:13px;color:#cbd5e1;margin-top:20px}
.foot{text-align:center;color:#64748b;font-size:12px;margin-top:30px}"""

    tpl = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<title>老登股跌幅榜筛选 · 企稳审查 · 精选标的</title><style>{css}</style></head><body><div class="wrap">
<h1>老登股跌幅榜 · 企稳审查 · 精选标的</h1>
<p class="sub">数据源：本地 SQLite（baostock 不复权）｜ 最新交易日：{latest} ｜ 回溯 {lb} 交易日 ｜ 老登股=公用事业/自然资源周期股<br>生成：{now}</p>
<div class="cards">
<div class="card c-blue"><div class="n">{total}</div><div class="l">老登股总数</div></div>
<div class="card c-red"><div class="n">{ntop}</div><div class="l">跌幅≥28%</div></div>
<div class="card c-orange"><div class="n">{nstable}</div><div class="l">跌幅≥28% 且企稳&gt;-2%</div></div>
<div class="card c-purple"><div class="n">{npick}</div><div class="l">精选长期向好</div></div>
</div>
<div class="sec"><h2>精选 5 只长期向好标的（战略金属 + 公用事业）</h2>{picks_html}</div>
<div class="sec"><h2>跌幅榜老登股 TOP 40（跌幅降序）</h2>
<table><thead><tr><th>代码</th><th>名称</th><th>60日跌幅</th><th>企稳系数</th><th>最新收盘</th><th>60日最高</th><th>上市年份</th></tr></thead><tbody>{top_rows}</tbody></table></div>
<div class="note">企稳系数 = 最新收盘价 / 近10日均价 - 1，&gt;-2% 视为初步止跌。仅覆盖本地已拉取 {total} 只老登股（全市场约5000只，深市部分资源股如紫金矿业、锡业股份等未在本地库）。本报表仅供研究参考，不构成投资建议。</div>
<div class="foot">Generated by screen_old_school.py | {now}</div>
</div></body></html>"""

    html = tpl.replace("{css}", css).replace("{latest}", latest).replace("{lb}", str(LOOKBACK)) \
        .replace("{now}", now).replace("{total}", str(len(res))).replace("{ntop}", str(len(top))) \
        .replace("{nstable}", str(len(stable))).replace("{npick}", str(len(picks))) \
        .replace("{picks_html}", "\n".join(pick_cards)).replace("{top_rows}", top_rows)

    path = os.path.join(OUT, "old_school_report.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


if __name__ == "__main__":
    main()
