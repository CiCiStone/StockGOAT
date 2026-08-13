# StockGOAT

面向 A 股投资 / 量化研究的个人工作区，集成数据获取、量化脚本与投研 AI Skill。

## 目录结构

| 目录 | 说明 |
|------|------|
| [`dataset/`](./dataset/) | 本地数据：baostock 拉取的 SQLite 日线库等（已 gitignore） |
| [`quant/`](./quant/) | 量化脚本：数据拉取、筛选等 |
| [`resource/`](./resource/) | 原始资源：skill 压缩包等归档 |
| [`skills/`](./skills/) | 投研 AI Skill（详见 [skills/README.md](./skills/README.md)） |

## 数据获取（baostock）

依赖 baostock，已装在 conda 环境 `eastmoney` 中。

```bash
conda activate eastmoney

# 全市场日线（可指定区间）
python quant/fetch_daily.py --start 2023-01-01 --end 2026-08-14

# 增量更新（从库中最新日期续拉到今天）
python quant/fetch_daily.py --update

# 只拉指定股票
python quant/fetch_daily.py --codes sh.600000,sz.000001 --start 2025-01-01
```

- 数据落库：`dataset/stock_daily.db`
- 表：`stock_basic`（基础信息）、`daily_k`（日线，不复权）
- 更多用法：`python quant/fetch_daily.py -h`

## Skills

投研 skill 概览见 [skills/README.md](./skills/README.md)，含：

- `data-search-spec` — 标的资料搜索规范
- `stock-drop-filter` — A 股超跌 + 换手率异动筛选
- `jingshui-growth-stock` — 静水2008 成长股投资体系（13 个子 skill）
- `penetrate-super-skill` — 穿透三部曲（财报/估值/叙事）母技能

## 免责声明

本仓库内容基于公开数据，仅供研究学习，**不构成投资建议**。
