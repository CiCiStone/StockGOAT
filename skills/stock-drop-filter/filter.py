"""
股票筛选 Skill：
  1. 获取当前在市的非 ST A 股列表（~5000 只，不包含已退市和 ST）
  2. 拉取近 N 天数据（默认 60 天）
  3. 条件一：收盘价相对周期内最高点跌幅 >= DROP_RATIO（默认 28%）
     -> 符合条件的写入 JSON 库（自动清理 > MAX_AGE_DAYS 的旧记录）
  4. 条件二：最后一天换手率 > 倒数第二天 + TURN_DELTA（默认 1%）
              或 最后一天换手率 >= TURN_ABS（默认 8%）
  5. 生成美观 HTML 报表（三个折叠区域），输出到 output/ 目录
"""

import baostock as bs
import json
import os
import time
from datetime import date, datetime, timedelta
from collections import OrderedDict

# ============================================================
# 配置
# ============================================================
LOOKBACK_DAYS = 60          # 回溯天数
DROP_RATIO = 0.28           # 跌幅阈值（28%）
TURN_DELTA = 1.0            # 换手率差值阈值（%）
TURN_ABS = 8.0              # 换手率绝对值阈值（%），当天换手率 >= 此值也算条件二
TURN_DELTA_RATE = 1.5
MAX_AGE_DAYS = 300          # JSON 库中最高点距今超过此天数则删除

FIELDS = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DB_PATH = os.path.join(BASE_DIR, "data", "condition1_db.json")
STOCK_LIST_PATH = os.path.join(BASE_DIR, "data", "stock_list.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 0. 获取在市的非 ST A 股列表
# ============================================================
def get_active_stock_list(force_refresh=False):
    """
    获取当前在市的非 ST A 股列表，缓存到 JSON。
    条件：type=1(股票), status=1(上市), code_name 不含 ST, 代码以 sh./sz. 开头
    """
    if not force_refresh and os.path.exists(STOCK_LIST_PATH):
        with open(STOCK_LIST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 缓存 1 天内有效
        cache_time = datetime.fromtimestamp(os.path.getmtime(STOCK_LIST_PATH))
        if (datetime.now() - cache_time).days < 1:
            print(f"从缓存加载股票列表: {len(data)} 只")
            return data

    print("正在获取全市场股票列表...")
    lg = bs.login()
    if lg.error_code != '0':
        print(f"登录失败: {lg.error_msg}")
        return []

    rs = bs.query_stock_basic()
    if rs.error_code != '0':
        print(f"获取股票列表失败: {rs.error_msg}")
        bs.logout()
        return []

    # 黑名单关键词：名称包含以下任一关键词的股票直接过滤
    BLACKLIST_KEYWORDS = ["ST", "退市", "PT"]

    stocks = []
    while rs.next():
        row = rs.get_row_data()
        rec = dict(zip(rs.fields, row))
        code = rec.get("code", "")
        code_name = (rec.get("code_name", "") or "").strip()

        # 只保留 A 股（sh.6xxxxx / sz.0xxxxx / sz.3xxxxx）
        if not (code.startswith("sh.6") or code.startswith("sz.0") or code.startswith("sz.3")):
            continue

        # 黑名单过滤：名称含 ST/退市/PT，或名称为空
        if not code_name:
            continue
        if any(kw in code_name for kw in BLACKLIST_KEYWORDS):
            continue

        # type 和 status 用 int 比较（baostock 返回的可能是整数）
        try:
            stock_type = int(rec.get("type", 0))
            stock_status = int(rec.get("status", 0))
        except (ValueError, TypeError):
            continue

        # 必须是股票(type=1) 且 上市(status=1)
        if stock_type != 1 or stock_status != 1:
            continue

        stocks.append({"code": code, "code_name": code_name})

    bs.logout()

    with open(STOCK_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

    print(f"获取到 {len(stocks)} 只在市非 ST A 股")
    return stocks


# ============================================================
# 1. 数据拉取
# ============================================================
def fetch_stock_data(lg, stock_code, start_date, max_retries=3):
    """拉取单只股票数据，返回 [{date, close, turn, ...}, ...] 列表。"""
    end_date = date.today().strftime('%Y-%m-%d')

    for attempt in range(max_retries):
        try:
            rs = bs.query_history_k_data_plus(
                stock_code, FIELDS,
                start_date=start_date, end_date=end_date,
                frequency="d", adjustflag="3")

            if rs.error_code == '10002007':
                wait = (attempt + 1) * 5
                time.sleep(wait)
                continue

            if rs.error_code != '0':
                return []

            data_list = []
            while rs.next():
                data_list.append(dict(zip(rs.fields, rs.get_row_data())))
            return data_list

        except OSError:
            wait = (attempt + 1) * 5
            time.sleep(wait)

    return []


# ============================================================
# 2. 条件一筛选 + JSON 库维护
# ============================================================
def load_condition1_db():
    """加载条件一 JSON 库。"""
    if os.path.exists(JSON_DB_PATH):
        with open(JSON_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_condition1_db(db):
    """保存条件一 JSON 库。"""
    with open(JSON_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def clean_old_records(db, today_str):
    """删除最高点距今超过 MAX_AGE_DAYS 的记录。"""
    today = datetime.strptime(today_str, "%Y-%m-%d")
    to_delete = []
    for code, info in db.items():
        peak_date = datetime.strptime(info["peak_date"], "%Y-%m-%d")
        if (today - peak_date).days > MAX_AGE_DAYS:
            to_delete.append(code)
    for code in to_delete:
        del db[code]
    if to_delete:
        print(f"  清理 {len(to_delete)} 条过期记录（最高点距今 > {MAX_AGE_DAYS} 天）")


def check_condition1(data_list, drop_ratio=DROP_RATIO):
    """
    条件一：最后一天收盘价相对周期内最高收盘价跌幅 >= drop_ratio。
    返回 dict 或 None。
    """
    if len(data_list) < 5:
        return None

    for row in data_list:
        row["close_f"] = float(row["close"]) if row["close"] else 0.0
        row["turn_f"] = float(row["turn"]) if row["turn"] else 0.0

    last = data_list[-1]
    last_close = last["close_f"]
    if last_close <= 0:
        return None

    peak = max(data_list, key=lambda r: r["close_f"])
    peak_close = peak["close_f"]
    peak_date = peak["date"]

    drop = (peak_close - last_close) / peak_close
    if drop >= drop_ratio:
        last_turn = last["turn_f"]
        prev_turn = data_list[-2]["turn_f"] if len(data_list) >= 2 else 0.0
        prev2_turn = data_list[-3]["turn_f"] if len(data_list) >= 3 else 0.0
        return {
            "code": last["code"],
            "code_name": "",  # 后面补
            "peak_close": round(peak_close, 2),
            "peak_date": peak_date,
            "last_close": round(last_close, 2),
            "drop_pct": round(drop * 100, 2),
            "last_turn": round(last_turn, 2),
            "prev_turn": round(prev_turn, 2),
            "prev2_turn": round(prev2_turn, 2),
            "last_date": last["date"],
        }
    return None


def run_condition1(stock_list, lookback_days=LOOKBACK_DAYS):
    """
    拉取股票列表近 N 天数据，筛选条件一，更新 JSON 库。
    """
    today_str = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=lookback_days + 5)).strftime("%Y-%m-%d")

    print(f"\n=== 条件一筛选（近 {lookback_days} 天，跌幅 >= {DROP_RATIO*100:.0f}%）===")
    print(f"数据范围: {start_date} ~ {today_str}")
    print(f"待扫描股票: {len(stock_list)} 只")

    lg = bs.login()
    if lg.error_code != '0':
        print(f"登录失败: {lg.error_msg}")
        return {}

    db = load_condition1_db()
    clean_old_records(db, today_str)

    # 股票名称映射
    name_map = {s["code"]: s["code_name"] for s in stock_list}

    matched = 0
    new_stocks = 0

    for i, stock in enumerate(stock_list):
        code = stock["code"]
        data_list = fetch_stock_data(lg, code, start_date)
        if not data_list:
            continue

        result = check_condition1(data_list)
        if result:
            matched += 1
            result["code_name"] = name_map.get(code, "")
            if code not in db:
                new_stocks += 1
            db[code] = result

        if (i + 1) % 500 == 0:
            print(f"  已扫描 {i+1}/{len(stock_list)} 只，命中 {matched} 只，新增 {new_stocks} 只")

    bs.logout()

    save_condition1_db(db)
    print(f"\n扫描完成: 共 {len(stock_list)} 只，条件一命中 {matched} 只（新增 {new_stocks}），库内共 {len(db)} 只")
    return db


# ============================================================
# 3. 条件二筛选
# ============================================================
def check_condition2(stock_info, turn_delta=TURN_DELTA, turn_abs=TURN_ABS, turn_delta_rate=TURN_DELTA_RATE):
    """
    条件二（OR 逻辑）：
    - 最后一天换手率 > 倒数第二天 + turn_delta(%)
    - 或 最后一天换手率 >= turn_abs(%)
    """
    last_turn = stock_info["last_turn"]
    prev_turn = stock_info["prev_turn"]
    return (last_turn > prev_turn + turn_delta) or  (last_turn >= turn_abs)  or last_turn / (prev_turn + 0.00000001) >= turn_delta_rate 


def run_condition2(db):
    """从 JSON 库中筛选符合条件二的股票。"""
    print(f"\n=== 条件二筛选（换手率差值 > {TURN_DELTA}% 或 当天 >= {TURN_ABS}%）===")
    result = []
    for code, info in db.items():
        if check_condition2(info):
            result.append(info)
    result.sort(key=lambda x: x["drop_pct"], reverse=True)
    print(f"条件二命中: {len(result)} 只")
    return result


# ============================================================
# 4. HTML 报表生成（三折叠区）
# ============================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>股票筛选报表 - {timestamp}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #333; padding: 20px; }}
  .container {{ max-width: 1400px; margin: 0 auto; }}
  h1 {{ text-align: center; color: #1a1a2e; margin-bottom: 8px; font-size: 28px; }}
  .subtitle {{ text-align: center; color: #666; margin-bottom: 24px; font-size: 14px; }}
  .summary {{ display: flex; gap: 16px; justify-content: center; margin-bottom: 32px; flex-wrap: wrap; }}
  .card {{ background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 20px 28px; text-align: center; min-width: 150px; }}
  .card .num {{ font-size: 36px; font-weight: 700; }}
  .card .label {{ font-size: 13px; color: #888; margin-top: 4px; }}
  .card.red .num {{ color: #e74c3c; }}
  .card.green .num {{ color: #27ae60; }}
  .card.blue .num {{ color: #3498db; }}
  .card.orange .num {{ color: #e67e22; }}

  /* 折叠 */
  .section {{ margin-bottom: 24px; }}
  .section-header {{ display: flex; align-items: center; gap: 12px; cursor: pointer; user-select: none; padding: 14px 18px; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: background 0.2s; }}
  .section-header:hover {{ background: #f0f4ff; }}
  .section-header .arrow {{ font-size: 14px; transition: transform 0.3s; color: #888; }}
  .section-header.collapsed .arrow {{ transform: rotate(-90deg); }}
  .section-header .title {{ font-size: 17px; font-weight: 700; }}
  .section-header .badge {{ font-size: 13px; padding: 2px 10px; border-radius: 20px; color: #fff; font-weight: 600; }}
  .badge-red {{ background: #e74c3c; }}
  .badge-green {{ background: #27ae60; }}
  .badge-orange {{ background: #e67e22; }}
  .section-body {{ overflow: hidden; transition: max-height 0.4s ease; max-height: 99999px; }}
  .section-body.hidden {{ max-height: 0; }}

  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 0 0 10px 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
  th {{ background: #1a1a2e; color: #fff; padding: 12px 10px; font-size: 12px; text-align: left; white-space: nowrap; }}
  td {{ padding: 10px; font-size: 12px; border-bottom: 1px solid #eee; }}
  tr:hover td {{ background: #f0f4ff; }}
  .drop-high {{ color: #e74c3c; font-weight: 700; }}
  .drop-mid {{ color: #e67e22; font-weight: 600; }}
  .drop-low {{ color: #f39c12; }}
  .turn-high {{ color: #e74c3c; font-weight: 700; }}
  .no-data {{ text-align: center; padding: 40px; color: #999; font-size: 14px; }}
  .footer {{ text-align: center; color: #aaa; font-size: 12px; margin-top: 40px; }}

  @media (max-width: 768px) {{
    table {{ font-size: 11px; }}
    th, td {{ padding: 8px 6px; }}
  }}
</style>
</head>
<body>
<div class="container">
  <h1>股票筛选报表</h1>
  <p class="subtitle">
    数据日期: {today} | 回溯: {lookback}天 | 跌幅阈值: {drop_ratio}% | 换手率差值: {turn_delta}% | 换手率绝对值: {turn_abs}%
  </p>

  <div class="summary">
    <div class="card red"><div class="num">{cond1_count}</div><div class="label">条件一命中</div></div>
    <div class="card green"><div class="num">{cond2_count}</div><div class="label">条件二命中</div></div>
    <div class="card orange"><div class="num">{both_count}</div><div class="label">同时符合</div></div>
    <div class="card blue"><div class="num">{db_count}</div><div class="label">库内总计</div></div>
    <div class="card"><div class="num" style="color:#8e44ad">{total_stocks}</div><div class="label">扫描股票数</div></div>
  </div>

  <!-- 条件一 -->
  <div class="section">
    <div class="section-header" onclick="toggleSection(this)">
      <span class="arrow">&#9660;</span>
      <span class="title">条件一：跌幅 >= {drop_ratio}%</span>
      <span class="badge badge-red">{cond1_count}</span>
    </div>
    <div class="section-body">{table1}</div>
  </div>

  <!-- 条件二 -->
  <div class="section">
    <div class="section-header" onclick="toggleSection(this)">
      <span class="arrow">&#9660;</span>
      <span class="title">条件二：换手率差值 > {turn_delta}% 或 当天换手率 >= {turn_abs}%</span>
      <span class="badge badge-green">{cond2_count}</span>
    </div>
    <div class="section-body">{table2}</div>
  </div>

  <!-- 同时符合 -->
  <div class="section">
    <div class="section-header" onclick="toggleSection(this)">
      <span class="arrow">&#9660;</span>
      <span class="title">同时符合条件一 + 条件二</span>
      <span class="badge badge-orange">{both_count}</span>
    </div>
    <div class="section-body">{table3}</div>
  </div>

  <div class="footer">Generated by filterStockSkill | {timestamp}</div>
</div>

<script>
function toggleSection(header) {{
  header.classList.toggle("collapsed");
  var body = header.nextElementSibling;
  body.classList.toggle("hidden");
}}
</script>
</body>
</html>"""


TABLE_HEADERS = ["代码", "名称", "最高价", "最高价日期", "最后收盘价", "跌幅(%)",
                 "最后换手(%)", "前日换手(%)", "前前日换手(%)", "最后日期"]
TABLE_KEYS = ["code", "code_name", "peak_close", "peak_date", "last_close", "drop_pct",
              "last_turn", "prev_turn", "prev2_turn", "last_date"]


def _build_table(rows):
    """构建 HTML 表格。"""
    if not rows:
        return '<div class="no-data">暂无符合条件的数据</div>'

    html = '<table><thead><tr>'
    for h in TABLE_HEADERS:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'

    for row in rows:
        html += '<tr>'
        for key in TABLE_KEYS:
            val = row.get(key, "")
            cls = ""
            if key == "drop_pct":
                v = float(val)
                if v >= 40:
                    cls = 'drop-high'
                elif v >= 30:
                    cls = 'drop-mid'
                else:
                    cls = 'drop-low'
            elif key == "last_turn" and float(val) >= TURN_ABS:
                cls = 'turn-high'
            html += f'<td class="{cls}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def generate_html(db, cond2_list, stock_count, lookback_days=LOOKBACK_DAYS,
                  drop_ratio=DROP_RATIO, turn_delta=TURN_DELTA, turn_abs=TURN_ABS):
    """生成 HTML 报表并保存。"""
    today_str = date.today().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    cond1_list = sorted(db.values(), key=lambda x: x["drop_pct"], reverse=True)

    # 同时符合的
    cond2_codes = {r["code"] for r in cond2_list}
    both_list = [r for r in cond1_list if r["code"] in cond2_codes]

    table1 = _build_table(cond1_list)
    table2 = _build_table(cond2_list)
    table3 = _build_table(both_list)

    html = HTML_TEMPLATE.format(
        timestamp=timestamp,
        today=today_str,
        lookback=lookback_days,
        drop_ratio=int(drop_ratio * 100),
        turn_delta=turn_delta,
        turn_abs=turn_abs,
        cond1_count=len(cond1_list),
        cond2_count=len(cond2_list),
        both_count=len(both_list),
        db_count=len(db),
        total_stocks=stock_count,
        table1=table1,
        table2=table2,
        table3=table3,
    )

    output_path = os.path.join(OUTPUT_DIR, f"report_{timestamp}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n报表已生成: {output_path}")
    return output_path


# ============================================================
# 主流程
# ============================================================
def run_pipeline(lookback_days=LOOKBACK_DAYS, drop_ratio=DROP_RATIO,
                 turn_delta=TURN_DELTA, turn_abs=TURN_ABS):
    """执行完整流水线。"""
    print("=" * 60)
    print(f"  filterStockSkill - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 0: 获取在市的非 ST A 股列表
    stock_list = get_active_stock_list()

    if not stock_list:
        print("获取股票列表失败！")
        return

    # Step 1 & 2: 拉取数据 + 条件一筛选 + 更新 JSON 库
    db = run_condition1(stock_list, lookback_days)

    if not db:
        print("条件一无命中。")
        generate_html({}, [], len(stock_list), lookback_days, drop_ratio, turn_delta, turn_abs)
        return

    # Step 3: 条件二筛选
    cond2_list = run_condition2(db)

    # Step 4: 生成 HTML 报表
    generate_html(db, cond2_list, len(stock_list), lookback_days, drop_ratio, turn_delta, turn_abs)

    print("\n完成!")


if __name__ == "__main__":
    run_pipeline(lookback_days=60, drop_ratio=0.28, turn_delta=1.0, turn_abs=8.0)
