# -*- coding: utf-8 -*-
"""
使用 baostock 拉取 A 股日线数据并存入本地 SQLite。

依赖: baostock (已装在 conda 环境 eastmoney 中)

用法:
    conda activate eastmoney

    # 拉取全部上市股票，指定日期区间
    python quant/fetch_daily.py --start 2024-01-01 --end 2026-08-14

    # 只拉最近 N 个自然日
    python quant/fetch_daily.py --days 30

    # 增量更新：从库中已有最新日期继续拉到今天
    python quant/fetch_daily.py --update

    # 只拉某几只股票（逗号分隔，如 sh.600000,sz.000001）
    python quant/fetch_daily.py --codes sh.600000,sz.000001 --start 2025-01-01

数据表:
    stock_basic  股票基础信息（代码/名称/上市日期/退市日期/类型/状态）
    daily_k      日线行情（开/高/低/收/前收/量/额/换手/涨跌幅/ST标记，不复权）
"""

import argparse
import datetime as dt
import sqlite3
import sys
import time

import baostock as bs

# baostock 日线字段 -> 表列名
DAILY_FIELDS = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

DEFAULT_DB = "dataset/stock_daily.db"


def parse_args():
    p = argparse.ArgumentParser(description="baostock 日线数据 -> SQLite")
    p.add_argument("--start", help="开始日期 YYYY-MM-DD")
    p.add_argument("--end", help="结束日期 YYYY-MM-DD（默认今天）")
    p.add_argument("--days", type=int, default=0, help="只拉最近 N 个自然日（与 --start 互斥）")
    p.add_argument("--update", action="store_true", help="增量更新：从库中最新日期续拉到今天")
    p.add_argument("--codes", help="只拉指定股票，逗号分隔，如 sh.600000,sz.000001")
    p.add_argument("--db", default=DEFAULT_DB, help="SQLite 文件路径")
    p.add_argument("--adjustflag", default="3", choices=["1", "2", "3"],
                   help="复权方式: 1后复权 2前复权 3不复权(默认)")
    p.add_argument("--batch", type=int, default=200, help="每多少只股票提交一次事务")
    return p.parse_args()


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_basic (
            code      TEXT PRIMARY KEY,
            name      TEXT,
            ipo_date  TEXT,
            out_date  TEXT,
            type      TEXT,
            status    TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_k (
            code        TEXT,
            date        TEXT,
            open        REAL,
            high        REAL,
            low         REAL,
            close       REAL,
            preclose    REAL,
            volume      REAL,
            amount      REAL,
            adjustflag  TEXT,
            turn        REAL,
            tradestatus TEXT,
            pct_chg     REAL,
            is_st       TEXT,
            PRIMARY KEY (code, date)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_k (date)")
    conn.commit()


def last_date(conn):
    row = conn.execute("SELECT MAX(date) FROM daily_k").fetchone()
    return row[0] if row and row[0] else None


def resolve_dates(conn, args):
    end = args.end or dt.date.today().strftime("%Y-%m-%d")
    if args.update:
        start = last_date(conn)
        if start is None:
            start = (dt.date.today() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
    elif args.days > 0:
        start = (dt.date.today() - dt.timedelta(days=args.days)).strftime("%Y-%m-%d")
    else:
        start = args.start or (dt.date.today() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
    return start, end


def get_stock_list(codes=None):
    """返回 [(code, name, ipo_date, out_date, type, status), ...]，仅保留上市股票。"""
    if codes:
        result = []
        for code in [c.strip() for c in codes.split(",") if c.strip()]:
            result.append((code, "", "", "", "", ""))
        return result
    rs = bs.query_stock_basic()
    rows = []
    while rs.next():
        row = rs.get_row_data()
        # 过滤非股票 / 已退市
        if row[4] == "1" and row[5] == "1":
            rows.append(tuple(row))
    return rows


def fetch_daily(code, start, end, adjustflag):
    rs = bs.query_history_k_data_plus(
        code, DAILY_FIELDS, start_date=start, end_date=end,
        frequency="d", adjustflag=adjustflag,
    )
    rows = []
    while rs.next():
        row = rs.get_row_data()
        # 过滤无成交记录
        if row[8] == "" or float(row[8]) <= 0:
            continue
        rows.append(row)
    return rows


def main():
    args = parse_args()
    conn = sqlite3.connect(args.db)
    init_db(conn)

    start, end = resolve_dates(conn, args)
    print(f"[fetch_daily] 区间 {start} ~ {end} | 复权方式 {args.adjustflag} | 库 {args.db}")

    lg = bs.login()
    if lg.error_code != "0":
        print(f"[fetch_daily] 登录失败: {lg.error_code} {lg.error_msg}")
        sys.exit(1)

    try:
        stocks = get_stock_list(args.codes)
        print(f"[fetch_daily] 待拉取股票数: {len(stocks)}")

        total_days = 0
        for i, stock in enumerate(stocks, 1):
            code, name, ipo, out, typ, status = stock
            # 更新基础信息
            conn.execute(
                "INSERT OR REPLACE INTO stock_basic VALUES (?,?,?,?,?,?)",
                (code, name, ipo, out, typ, status),
            )
            rows = fetch_daily(code, start, end, args.adjustflag)
            if rows:
                # 重排为 (code,date,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pct_chg,is_st)
                # pctChg 为空 -> None
                norm = [
                    (r[1], r[0], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9],
                     r[10], r[11], (r[12] if r[12] != "" else None), r[13])
                    for r in rows
                ]
                conn.executemany(
                    """INSERT OR REPLACE INTO daily_k
                       (code,date,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pct_chg,is_st)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    norm,
                )
                total_days += len(rows)
            if i % args.batch == 0:
                conn.commit()
                print(f"[fetch_daily] {i}/{len(stocks)} 累计 {total_days} 条 | {code}")
            time.sleep(0.05)  # 轻微限速，避免触发风控

        conn.commit()
        print(f"[fetch_daily] 完成: {len(stocks)} 只股票, 累计写入 {total_days} 条日线")
    finally:
        bs.logout()
        conn.close()


if __name__ == "__main__":
    main()
