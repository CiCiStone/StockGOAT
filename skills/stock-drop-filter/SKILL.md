# filterStockSkill

A 股跌幅筛选 + 换手率异动检测技能，每日自动拉取全市场数据，筛选符合条件的股票并生成 HTML 报表。

## 功能概述

1. 获取当前在市的非 ST A 股列表（约 5000 只，自动过滤退市、ST、指数等）
2. 拉取近 N 天日 K 线数据（默认 60 天）
3. **条件一**：收盘价相对周期内最高点跌幅 ≥ 阈值（默认 28%），命中写入 JSON 持久化库
4. **条件二**：从 JSON 库中筛选换手率异动（差值或绝对值），OR 逻辑
5. 生成美观 HTML 报表（三折叠区域），输出到 `output/` 目录

## 文件结构

```
filterStockSkill/
├── SKILL.md              # 本说明文档
├── filter.py             # 主脚本
├── data/
│   ├── stock_list.json   # 股票列表缓存（1天有效）
│   └── condition1_db.json # 条件一命中库（持久化）
└── output/
    └── report_YYYYMMDD_HHMMSS.html  # HTML 报表
```

## 使用方法

```bash
cd /data/workspace/filterStockSkill
conda activate py312
python filter.py
```

### 自定义参数

在 `filter.py` 底部 `__main__` 中调整：

```python
run_pipeline(
    lookback_days=60,    # 回溯天数
    drop_ratio=0.28,     # 跌幅阈值（28%）
    turn_delta=1.0,      # 换手率差值阈值（%）
    turn_abs=8.0,        # 换手率绝对值阈值（%）
)
```

## 筛选条件详解

### 条件一：超跌筛选

- 近 N 天内最高收盘价 vs 最后一天收盘价
- 跌幅 = (最高价 - 最后收盘价) / 最高价 ≥ `DROP_RATIO`
- 命中后写入 `data/condition1_db.json`
- 自动清理最高点距今超过 `MAX_AGE_DAYS`（300天）的过期记录

### 条件二：换手率异动（OR 逻辑）

满足任一即命中：
- 最后一天换手率 > 倒数第二天换手率 + `TURN_DELTA`（1%）
- 最后一天换手率 ≥ `TURN_ABS`（8%）

### 黑名单机制

拉取股票列表时自动过滤：
- 名称含 `ST` / `*ST` / `退市` / `PT`
- 名称为空
- `type != 1`（非股票，如指数、ETF）
- `status != 1`（已退市）

## 数据来源

- 股票列表：`baostock.query_stock_basic()`
- K 线数据：`baostock.query_history_k_data_plus()`，日线不复权

## HTML 报表

三个可折叠区域：
1. **条件一命中**：所有超跌股票，按跌幅降序排列
2. **条件二命中**：换手率异动股票
3. **同时符合**：两个条件都满足的（最有价值的候选）

包含字段：代码、名称、最高价（日期）、最后收盘价、跌幅%、近三天换手率。

## 依赖

- Python 3.12
- baostock
- 标准库：json, os, time, datetime, collections
