# Skills 索引

本项目 `skills/` 目录集中管理股票投研相关的 AI Skill。每个 skill 是一个独立目录，内含 `SKILL.md` 说明（以及必要的脚本 / 数据）。

## 目录总览

| 目录 | 原始来源 | 说明 |
|------|---------|------|
| [`data-search-spec/`](./data-search-spec/SKILL.md) | `SKILL.MD` | **标的资料搜索规范**：数据来源白名单 + 两阶段调研流程 + 报告产出规范（红涨绿跌配色、超链接规范） |
| [`stock-drop-filter/`](./stock-drop-filter/SKILL.md) | `filterStockSkill.zip` | **A股超跌 + 换手率异动筛选**：`filter.py` 每日拉全市场日线，筛超跌股并生成 HTML 报表（依赖 baostock） |
| [`jingshui-growth-stock/`](./jingshui-growth-stock/README.md) | `jingshui-growth-stock-skill-main.zip` | **静水2008《极简成长股投资体系》**蒸馏出的 13 个成长股投资子 skill |
| [`penetrate-super-skill/`](./penetrate-super-skill/SKILL.md) | `penetrate-super-skill.rar` | **穿透三部曲超级母技能**：财报 + 估值 + 叙事统一流水线，内联 25 个原子心智模型 |

> 原始压缩包已移至 `../resource/` 归档。

---

## 1. data-search-spec（标的资料搜索规范）

- **作用**：约束数据来源（东方财富/同花顺/新浪/韭研公社等白名单）、定义调研两阶段流程（初稿 MD → Review 复核 → HTML）、报告章节与配色规范。
- **核心约定**：
  - 数据只用白名单来源，抓取优先级：Selenium 无头 Chrome > `web_fetch` > `web_search`。
  - 写作「结论先行 + 详细展开」，时序数据默认拉齐近三年（T-2 / T-1 / T）。
  - 红涨绿跌配色（🔴 利好 `.pos`，🟢 利空 `.neg`）。
- **产物路径**：`data/{类别}/{名称}/` + `output/{YYYYMMDD}-{简称}-调研报告-v{n}.md|html`。

## 2. stock-drop-filter（A股超跌筛选）

- **功能**：拉取非 ST 上市 A 股列表 → 近 N 天日 K → 条件一（较周期最高收盘价跌幅 ≥ 28%）→ 条件二（换手率异动，OR 逻辑）→ 输出 HTML 报表。
- **运行**：
  ```bash
  conda activate eastmoney
  python skills/stock-drop-filter/filter.py
  ```
- 参数在 `filter.py` 底部 `run_pipeline()` 调整（`lookback_days` / `drop_ratio` / `turn_delta` / `turn_abs`）。

## 3. jingshui-growth-stock（静水2008成长股体系）

把知乎作者 **静水2008** 的《极简成长股投资体系》用 RIA-TV++ 流水线蒸馏成 13 个可调用子 skill：

| # | 子 skill | 一句话 |
|---|---------|--------|
| 1 | `prosperity-and-inflection` | 景气度与拐点判断（体系总开关） |
| 2 | `super-growth-stock-criteria` | 超级成长股六条标准 |
| 3 | `industry-alpha-locking` | 行业 α 锁定法 |
| 4 | `three-selection-methods` | 三种选股方法地图 |
| 5 | `trend-following-entry` | 趋势跟随（创新高跟随） |
| 6 | `scale-in-and-risk-control` | 回调分仓 + 仓位风控 |
| 7 | `hold-or-cut-exit` | 持盈止损卖出框架 |
| 8 | `financial-report-signals` | 财报牛股信号 + 海量泛读 |
| 9 | `deliberate-observation` | 刻意观察法（消费股生活信号） |
| 10 | `minimalist-focus` | 极简专注原则 |
| 11 | `real-vs-fake-value-investing` | 真假价值投资辨析 |
| 12 | `seven-retail-sins` | 散户七大通病自检 |
| 13 | `ten-year-wealth-path` | 十年千万财富跃迁路径 |

完整引用图与推荐学习顺序见 [`jingshui-growth-stock/INDEX.md`](./jingshui-growth-stock/INDEX.md)，精华长文见 [`DIGEST.md`](./jingshui-growth-stock/DIGEST.md)。

## 4. penetrate-super-skill（穿透三部曲超级母技能）

- **来源**：邹佩轩《穿透财报》2023 +《穿透估值》2024 +《穿透叙事》2026 的蒸馏母技能。
- **核心命题**：DCF 是估值公理，超额收益来自「叙事变化（预期差）」；资产负债表是「存在」、利润表是「意见」、现金流量表是「事实」。
- **结构**：六阶不可跳序流水线（元层 → 反算隐含叙事 L → 叙事定位 → 资产负债表验证 → 利润表拆解 → 预期差结论）+ 执行层。
- **注意**：原文件引用的作者引擎路径 `H:/WORKBBUDDY/...` 在本机可能不存在，仅作方法论参考。

---

## 免责声明

以上 skill 均为认知与方法论学习工具，基于公开数据，仅供参考，**不构成投资建议**。
