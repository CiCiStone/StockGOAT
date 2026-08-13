# -*- coding: utf-8 -*-
"""
装配器：把「穿透三部曲」25 个原子心智模型（RIA++ 六节）内联进一个自包含的超级母技能，
并把作者原技能 penetrate-financial-report (v4.0) 作为执行层按路径只读引用（零触碰）。

输出：H:/WORKBBUDDY/books/penetrate-financial-report/NEW/skills/penetrate-super-skill/SKILL.md
"""
import os, io

BASE = "H:/WORKBBUDDY/books/penetrate-financial-report/NEW/skills"
OUT_DIR = os.path.join(BASE, "penetrate-super-skill")
OUT = os.path.join(OUT_DIR, "SKILL.md")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- 流水线步骤 → 原子 skill 映射（每个 skill 只嵌入一次，全覆盖 25 个）----
PIPELINE = [
    ("元层", "贯穿全局 · 跨层元原则（系统免疫层）", [
        "x-correlation-not-causation", "x-compound-lie", "x-buy-unloved",
    ]),
    ("Step 1", "反算隐含叙事（天花板 L）—— 估值层 · 打开上限", [
        "val-dcf-first-principle", "val-three-stage", "val-ceiling-decides-growth",
        "val-pe-quick-reference", "val-discount-rate-four-factor",
    ]),
    ("Step 2", "叙事定位与财报验证重点 · 行业背景锚定 —— 叙事层 + 财报锚", [
        "narr-two-mechanisms", "narr-narrative-template", "narr-three-levels-policy",
        "narr-era-defines-era", "report-balance-sheet-first",
    ]),
    ("Step 3", "资产负债表深度验证 —— 财报层 · 拉高下限", [
        "report-presumption-guilt", "report-fraud-balance-sheet-trace",
        "report-deferred-tax-mirror", "report-adjust-not-fraud", "report-bamboo-pole",
    ]),
    ("Step 4", "利润表拆解与现金流验证 —— 财报层 · 应用（判断逻辑已内联于 Step 3）", [
        # 本步是作者引擎的执行步，判断逻辑复用 Step 3 内联的 report-*；此处只给利润表专属应用指引
    ]),
    ("Step 5", "预期差结论与决策 —— 叙事层 + 跨层 · 统一框架落地", [
        "val-returns-are-valuation", "val-sensitivity-ranking",
        "val-relative-valuation-discipline", "val-cheap-is-king",
        "narr-bayesian-net", "narr-barbell", "narr-prosperity-trap",
    ]),
]

SKILL_TITLE = {}  # slug -> original H1 title text

def strip_frontmatter(text):
    """去掉 YAML frontmatter（首行 --- 到下一个 ---），返回正文。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i+1:])
    return text

def embed_skill(slug):
    path = os.path.join(BASE, slug, "SKILL.md")
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    body = strip_frontmatter(text)
    out = []
    title_skipped = False
    for line in body.splitlines():
        if not title_skipped and line.startswith("# "):
            # 记录原标题（用于 wrapper 标注），跳过该行
            SKILL_TITLE[slug] = line[2:].strip()
            title_skipped = True
            continue
        if line.startswith("#"):
            # 标题层级 +1（# -> ## ...），使其落入 Step wrapper (##) 之下
            cnt = 0
            while cnt < len(line) and line[cnt] == "#":
                cnt += 1
            out.append("#" + line)
        else:
            out.append(line)
    return "\n".join(out).strip()

# ========================= 静态包装（超级母技能骨架） =========================
FRONTMATTER = """---
name: penetrate-super-skill
display_name: 穿透三部曲超级母技能
version: 1.0.0
description: |
  穿透三部曲（《穿透财报》2023 + 《穿透估值》2024 + 《穿透叙事》2026，邹佩轩）统一超级母技能 ——
  携带 25 个原子心智模型完整方法论的六阶流水线（元层贯穿 → 反算隐含叙事 L → 叙事定位与验证重点 →
  资产负债表深度验证 → 利润表拆解 → 预期差结论），并零触碰编排作者原技能 penetrate-financial-report(v4.0)
  的 5 步法 + 报告生成器作为执行层。
  每个步骤自包含原子 skill 的完整 R/I/A1/A2/E/B 六节内容，无需外部 @skill 加载；判断层完全内联，
  执行层按路径只读引用作者引擎文件，不修改作者任何文件。
  触发信号：「分析XX公司」「XX穿透财报分析」「财务分析XX」「穿透财报XX」→ 自动按流水线产出完整报告(DOCX+HTML)；
  「DCF公理」「有罪推定」「两套定价机制」「便宜是硬道理」等概念 → 直接调用对应内联步骤作答。
  不适用于：期货/期权衍生品分析、纯短线技术分析、未指明具体公司的泛泛而谈。
source_book: 《穿透财报》邹佩轩(2023) / 《穿透估值》邹佩轩(2024) / 《穿透叙事》邹佩轩(2026)
source_chapter: H:/WORKBBUDDY/books/penetrate-financial-report/（三书蒸馏 + 作者原技能 v4.0 只读引用）
tags: [穿透, 财报分析, 估值, 叙事, 母技能, super-skill, pipeline, DCF, 叙事估值, 零触碰]
related_skills: [engine-penetrate-report]
agent_created: true
disable: false
---
"""

OVERVIEW = r"""# 穿透三部曲 · 超级母技能

> 本技能自包含 25 个原子心智模型的完整方法论（R/I/A1/A2/E/B 六节），按六阶流水线编排，触发后**无需外部加载**即可逐级执行；判断层完全内联，执行层零触碰引用作者原技能 `penetrate-financial-report`(v4.0) 的 5 步法 + 报告生成器。

---

## 总览 · 核心命题与流水线

**系统核心命题**：A 股定价本质只有一套——**DCF 是估值公理，超额收益只来自"叙事变化"（预期差）**。财报拉高投资下限（看错少亏钱）、估值打开上限（看透多赚钱）、叙事把二者统一成一套可复用框架。三张表地位不等：**资产负债表是"存在"、利润表是"意见"、现金流量表是"事实"**。

```
 元层(贯穿) ── 跨层元原则 x-*（系统免疫：相关性≠因果 / 买无人问津 / 复利是谎言）
      │  统摄
      ▼
 ┌──────────────── 六阶流水线（不可跳序）────────────────┐
 │                                                        │
 │  Step 1  反算隐含叙事 L（天花板）    估值层 · 打开上限  │
 │      │  用 val-* 手算（替代缺失的 dcf_implied.py）       │
 │      ▼                                                 │
 │  Step 2  叙事定位 + 验证重点 + 行业背景  叙事层 + 财报锚  │
 │      ▼                                                 │
 │  Step 3  资产负债表深度验证          财报层 · 拉高下限   │
 │      ▼                                                 │
 │  Step 4  利润表拆解 + 现金流验证    财报层 · 应用        │
 │      ▼                                                 │
 │  Step 5  预期差结论与决策           叙事层 + 跨层 · 统一  │
 │      ▼                                                 │
 │  执行层  编排作者引擎 penetrate-financial-report          │
 │          （5步法 + generate_report.py → DOCX+HTML）       │
 │          按路径只读引用，零触碰                          │
 └────────────────────────────────────────────────────────┘
```

**步骤清单**：
| # | 步骤 | 嵌入原子 skill | 核心产出 |
|:--|:-----|:----------|:---------|
| 元层 | 跨层元原则（贯穿） | x-correlation-not-causation · x-compound-lie · x-buy-unloved | 研究纪律与风险观地基 |
| Step 1 | 反算隐含叙事 L | val-dcf-first-principle · val-three-stage · val-ceiling-decides-growth · val-pe-quick-reference · val-discount-rate-four-factor | 三档 L、L/E3、L/E0、隐含增速；叙事类型 |
| Step 2 | 叙事定位 + 验证重点 + 行业背景 | narr-two-mechanisms · narr-narrative-template · narr-three-levels-policy · narr-era-defines-era · report-balance-sheet-first | 主导定价机制、验证重点科目、行业坐标系 |
| Step 3 | 资产负债表深度验证 | report-presumption-guilt · report-fraud-balance-sheet-trace · report-deferred-tax-mirror · report-adjust-not-fraud · report-bamboo-pole | 资产科目红旗扫描、调节/舞弊痕迹、财务质量 |
| Step 4 | 利润表拆解 + 现金流验证 | （复用 Step 3 内联的 report-*；利润是"意见"的专属应用） | 利润质量、非经常性损益、三张表联动 |
| Step 5 | 预期差结论与决策 | val-returns-are-valuation · val-sensitivity-ranking · val-relative-valuation-discipline · val-cheap-is-king · narr-bayesian-net · narr-barbell · narr-prosperity-trap | 预期差方向、风险收益、关注信号 |
| 执行层 | 编排作者引擎 | engine-penetrate-report（只读引用作者 v4.0） | DOCX(≥20页) + 简要 HTML |

---

## 🚨 流水线约束规则（硬性，不可违反）

### ① 不可跳序
分析必须按 元层 → Step 1 → 2 → 3 → 4 → 5 → 执行层 的顺序逐级推进，**不允许跳步或提前完成下游步骤**。每步结论是下一步输入，前一步未完成则后一步不能启动。

### ② 每步按内联内容执行
每执行一步，必须按本技能中该步**内联的对应原子 skill 完整指令（R/I/A1/A2/E/B）**执行，不能凭记忆或摘要代替。所有 25 个原子 skill 已完整内联于下方，无需外部 @skill 加载。

### ③ 判断层与执行层分离
- **判断**（该看什么、怎么解读、叙事是否成立）→ 由内联原子 skill 提供；
- **产出**（20 页 DOCX + 简要 HTML）→ 由执行层驱动作者 `generate_report.py` 生成。
凡"该不该买/卖""叙事是否成立"等判断，必须引用内联原子 skill，不得凭模板填空下结论。

### ④ 零触碰红线（作者文件）
绝不对作者目录（`H:/WORKBBUDDY/books/penetrate-financial-report/` 下的 `SKILL.md` / `data/` / `references/` / `scripts/`）做写/改名/移动/新增操作。执行层只**按路径读取**这些文件，任何"改进作者模板"的需求记录到本技能 notes，由用户决定是否另起文件。

### ⑤ L 手算替代缺环
作者引擎第 1 步原需外部技能 `penetrate-narrative-stock-analysis` 的 `dcf_implied.py`，本机未安装；但 `generate_report.py` 不 import 它（L 为 `___` 占位符）。本技能统一用内联的 `val-*` 系列**手算**三档 L（前3年一致预期、第4-8年匀速至 L、第9年起 g=0、r=8/10/12%），填实后续模板的 `___` 占位，完整复现作者公式，不依赖缺失脚本。

### ⑥ 三张表联动 + 六大循环配平（作者红线）
利润表每个科目变化，须在资产负债表/现金流量表找到对应（利润表是"意见"、资产负债表是"存在"、现金流量表是"事实"）；六大循环（投资筹资/采购付款/生产存货/销售收款/人力资源/货币资金）每个循环局部配平。

### ⑦ 数据质量红线（作者硬规则）
总市值=股价×总股本自洽；金额 `/1e8` 转「亿元」严禁 `/1e9`；一致预期净利润 > 当年营收×历史最高净利率 → 触发异常告警并人工复核；季度同季对比（Q1 比 Q1）。
**PE 自洽校验**：`PE(TTM) ≈ 总市值 ÷ 归母净利(TTM)`；若偏差 > 5% 必须先复核口径（TTM vs 单季/累计、归母 vs 扣非、总股本是否含回购）再使用，禁止用矛盾的 PE/市值同时下结论。

### ⑧ 报告输出
完整分析必须在最终报告呈现六阶流水线全部结论；详细版 DOCX 正文 ≥ 20 页（第二部分≥9页、第三部分≥7页），变动 > 20% 科目标红；同时输出简要版 HTML。图表配色遵循中国惯例：上涨红、下跌绿。

---

## 📡 数据获取路径（已验证 · 防踩坑 · 必须先用）

本流水线 Step 1（反算 L）与 Step 2（叙事定位）强依赖 **一致预期** 与 **主营构成** 数据，但这几类数据在本机 TDX MCP 上的可取路径有坑，务必按本表执行，避免重复踩雷（赛轮轮胎 601058 实战踩过的坑已固化于此）。

| 数据 | 推荐调用（已验证可用） | 坑 / 注意 |
|:--|:--|:--|
| 实时行情 + 估值 | `tdx_quotes`(codes="601058", hasCwInfo=1, hasExtInfo=1) → 现价 / 总市值 / PE(TTM) / PB / 每股净资产 / CwInfo 营收净利 | CwInfo 口径可能是单季或累计，须与三张表对齐；**先用规则⑦做 PE 自洽校验** |
| 资产负债表 | `tdx_api_data`(entry="TdxShareCW.ph_agf10_cw_zcfzb")（无需 fixedTag） | — |
| 利润表 | `tdx_api_data`(entry="TdxShareCW.ph_agf10_cw_lyb", fixedTag="00101") | — |
| 现金流量表 | `tdx_api_data`(entry="TdxShareCW.ph_agf10_cw_xjllb", fixedTag="00101") | — |
| **一致预期（净利润 / EPS）** | ⚠️ **`CWServ.tdxf10_gg_ybpj` 在本机 TDX 服务端 `503 模块不存在`，禁止调用！** 改用：① `wenda_report_query`(symbol="601058", query="研报 评级 目标价") 提取具体券商预测（如华泰 26E/27E 净利、EPS、目标价）；② `tdx_indicator_select`(message="公司 一致预期")。**必须标注来源券商与日期**；若都取不到，用最新年报 + Q1 run-rate + 指引推算并明确标「估算」 | 缺失 dcf_implied 时代替方案见规则⑤；严禁用虚假/臆造的「一致预期」 |
| **主营构成** | `tdx_api_data`(entry="TdxShareCW.ph_agf10_jyfx", fixedTag="00201")（有效范围 00201–00210） | ⚠️ **`fixedTag=00202` 无效 → validation 报错**；该接口返回报告期列表，需再取具体期。实际构成建议用 `tdx_indicator_select`(message="公司 主营构成") 直取（赛轮轮胎实测：轮胎占营收 ≈ 98.9%，境外第一大市场） |
| 研报评级 / 目标价线索 | `wenda_report_query`(symbol="601058", count=10) | 作为一致预期与叙事验证的辅助，不替代三张表 |

> 取数后逐项回填到附录C汇总表的「数据来源」列；任一接口失败都按上表 fallback，不得停滞或臆造。

---

## 母技能元方法论（核心命题 · 贯穿全流程）

### R — 原文锚点
> 「我们不是给财报估值，我们是给叙事估值。……所谓的'未来'就是终局，只要终局足够精彩，资本市场对过程的容忍度可以非常高。」—— 作者 v4.0 核心理念
> 「逻辑推理优于归纳总结……做反方观点的最佳辩手……三张表联动分析。」—— 作者方法论红线
> 「DCF 是估值第一性原理，一切相对估值法都是它的近似。」—— 《穿透估值》
> 「超额收益只来自叙事变化（预期差），而非增速本身。」—— 《穿透叙事》

### I — 方法论骨架
本技能把三部曲统一成一条**不可跳序的六阶流水线**：先用 DCF 公理反算当前股价隐含的终局叙事（天花板 L），再据叙事类型锚定财报验证重点与行业背景，然后对三张表完整科目逐项做结合行业背景的深度分析以验证/证伪该叙事，最后给出预期差判断。跨层三原则（相关性≠因果 / 买无人问津 / 复利是谎言）贯穿始终，是系统的"免疫系统"。

### A2 — 触发场景
1. **完整分析请求**：「分析XX公司」「XX穿透财报分析」「财务分析XX」→ 执行完整六阶流水线 + 产出报告。
2. **概念请求**：「DCF公理」「有罪推定」「两套定价机制」「便宜是硬道理」→ 直接调对应内联步骤作答，不出报告。
3. **单点质疑**：「XX应收增速远超营收是不是造假迹象」→ 优先调 `report-fraud-balance-sheet-trace` + `report-presumption-guilt`；若要出完整报告再转执行层。

---

"""

# 元层/各步的"职责一句话"引导
STEP_INTRO = {
    "元层": "本层为系统免疫层，在任何具体分析前加载，贯穿全流程。它约束研究纪律与风险观，是所有量化/研究/决策请求的默认统领。",
    "Step 1": "本步用 DCF 第一性原理反算当前股价隐含的终局利润 L（天花板），判定市场预期的是什么叙事。L 由内联 val-* 手算（替代缺失的 dcf_implied.py）。一致预期/行情取数按 📡 数据获取路径（已验证）执行——CWServ 一致预期接口本机已失效，改用研报/indicator 提取并标注来源；PE 先用规则⑦自洽校验。",
    "Step 2": "本步据 Step 1 的 L 判定主导定价机制与叙事类型，锚定财报验证重点科目，并建立行业背景坐标系（作为后续每项变动分析的锚点）。主营构成按 📡 数据获取路径（ph_agf10_jyfx fixedTag=00201 或 indicator 提取）取得。",
    "Step 3": "本步对资产负债表完整科目逐项做结合行业背景的深度分析（有罪推定 + 舞弊逆向 + 递延税照妖镜 + 调节识别 + 竹竿认知差），是拉高投资下限的核心。",
    "Step 4": "本步把 Step 3 内联的 report-* 判断逻辑应用到利润表与现金流量表（利润是「意见」），做收入质量、非经常性损益、三张表联动分析。判断逻辑已内联于 Step 3，此处给利润表专属应用指引。",
    "Step 5": "本步汇总叙事预期 vs 财报现实，给出预期差方向与风险收益结构，并用贝叶斯链→网、杠铃、景气度陷阱等统一框架落地决策。",
}

EXEC_LAYER = r"""---

## 执行层 · 编排作者引擎（零触碰）

> 本超级母技能的判断层已完全内联（无需 @skill 加载 25 个原子 skill）。当用户要**产出完整报告**时，由本层驱动作者原技能 `penetrate-financial-report`(v4.0) 的执行引擎——**按路径只读引用，绝不修改作者任何文件**。

### 作者引擎位置（只读）
- `H:/WORKBBUDDY/books/penetrate-financial-report/SKILL.md`（v4.0 流程与模板权威来源）
- `H:/WORKBBUDDY/books/penetrate-financial-report/references/*.md`（5 份：financial-methodology / statement-notes / fraud-detection / narrative-finance-integration / scoring-model-guide）
- `H:/WORKBBUDDY/books/penetrate-financial-report/scripts/generate_report.py`（报告生成器，依赖 python-docx）
- `H:/WORKBBUDDY/books/penetrate-financial-report/data/statement-template.xlsx`（报表科目模板）

### 执行编排步骤
1. **确认输入**：用户须指明公司名（A 股/港股）。未指明 → 先追问，不臆造。
2. **填实 L（替代缺环）**：Step 1 已用内联 `val-*` 手算三档 L、L/E3、L/E0、第4-8年隐含复合增速；将结果填实作者模板中的 `___` 占位。
3. **逐步编排**：对作者 5 步法的 Step2–Step5，每步先引用本技能对应内联原子 skill 取判断逻辑，再按作者 `references/*.md`（只读）做科目级深度分析，落实「变动 > 5% 必配四要素分析 ≥ 150 字」硬规则。
4. **驱动生成**：调 `scripts/generate_report.py`（依赖 python-docx），传入公司与 L 数据，产出 DOCX + HTML 两份。
   - `{公司简称}_穿透财报分析报告_增强版_v5.docx`
   - `{公司简称}_穿透财报分析报告_简要版.html`
5. **判停条件**：若一致预期净利润 > 当年营收 × 历史最高净利率（作者数据红线第 4 条）→ 触发异常告警并人工复核，不盲目生成。

### 零触碰校验
作者 4 类目录（SKILL.md / data/ / references/ / scripts/）在本流程中只读取、不写入/改名/移动/新增。任何"改进作者模板"的需求，记录到本技能 notes，由用户决定是否另起文件。

---

## 母技能边界 (Boundary)

### 何时不用
- **期货/期权衍生品分析**：本技能基于 A 股/港股财报与叙事，不涵盖衍生品持仓量维度。
- **纯短线技术分析**：本技能以基本面叙事估值为核心，量价技术面需另调对应技能。
- **未指明具体公司**：泛泛而谈「A 股怎么看」不触发完整流水线，应先澄清标的。

### 作者警告的失败模式（沿用）
- 只看增速绝对值/边际/超预期，忽略估值水平与隐含叙事（须先判 L 再验证）。
- 把相关性当因果、用统计回归"先有结论再找论据"（见 x-correlation-not-causation）。
- 有罪推定的系统性错杀代价（见 report-presumption-guilt 边界）。
- 10% 折现率为经验中枢但边界模糊（见 val-discount-rate-four-factor 边界）。

### 作者盲点（批判性提醒）
- 卖方/分析师视角、对市场有效的乐观预设、对"失败预测力"较弱、有罪推定的系统性错杀代价——已写入各内联原子 skill 的 B 段，编排时一并提示。

### 易混淆的邻近方法论
| 本技能 | 常见误解 |
|---|---|
| 超额收益来自叙事变化（预期差），非增速本身 | "增速高=能涨" |
| 资产负债表是存在/利润是意见/现金是事实 | 单看净利润 |
| DCF 公理 + 相对法是近似 | PE/PB 直接定价 |
| 判断层内联 + 执行层零触碰引用作者引擎 | 复制/修改作者文件 |

---

## 附录A：执行流程表（手动调用顺序）

```
元层 ── 【已内联】x-correlation-not-causation / x-compound-lie / x-buy-unloved
         （研究纪律与风险观地基，贯穿全流程）

Step 1 ── 【已内联】val-dcf-first-principle / val-three-stage / val-ceiling-decides-growth
          / val-pe-quick-reference / val-discount-rate-four-factor
          （反算三档 L、L/E3、L/E0，判叙事类型；手算替代 dcf_implied.py）
          │
Step 2 ── 【已内联】narr-two-mechanisms / narr-narrative-template
          / narr-three-levels-policy / narr-era-defines-era / report-balance-sheet-first
          （定主导定价机制 + 验证重点 + 行业背景锚）
          │
Step 3 ── 【已内联】report-presumption-guilt / report-fraud-balance-sheet-trace
          / report-deferred-tax-mirror / report-adjust-not-fraud / report-bamboo-pole
          （资产负债表完整科目深度验证）
          │
Step 4 ── 【复用 Step 3 内联 report-*】利润表拆解 + 现金流验证（利润是意见）
          │
Step 5 ── 【已内联】val-returns-are-valuation / val-sensitivity-ranking
          / val-relative-valuation-discipline / val-cheap-is-king
          / narr-bayesian-net / narr-barbell / narr-prosperity-trap
          （预期差结论与决策）
          │
执行层 ── 【只读引用】作者 penetrate-financial-report v4.0
          （5步法 + generate_report.py → DOCX≥20页 + HTML）
```

### 调用规则
| 规则 | 说明 |
|------|------|
| **串联执行** | 必须按 元层→Step1→2→3→4→5→执行层 顺序，不可跳步 |
| **自包含** | 25 个原子 skill 已完整内联，无需外部 @skill 加载 |
| **判断/执行分离** | 判断用内联原子 skill，产出用作者引擎（只读） |
| **零触碰** | 作者目录只读取不修改 |
| **L 手算** | 用内联 val-* 替代缺失的 dcf_implied.py |

---

## 附录B：原子 skill 内联清单（全覆盖 25 个）

| 内联位置 | 原子 skill | 内容完整性 |
|---|---|---|
| 元层 | x-correlation-not-causation · x-compound-lie · x-buy-unloved | R/I/A1/A2/E/B 完整六节 |
| Step 1 | val-dcf-first-principle · val-three-stage · val-ceiling-decides-growth · val-pe-quick-reference · val-discount-rate-four-factor | R/I/A1/A2/E/B 完整六节 |
| Step 2 | narr-two-mechanisms · narr-narrative-template · narr-three-levels-policy · narr-era-defines-era · report-balance-sheet-first | R/I/A1/A2/E/B 完整六节 |
| Step 3 | report-presumption-guilt · report-fraud-balance-sheet-trace · report-deferred-tax-mirror · report-adjust-not-fraud · report-bamboo-pole | R/I/A1/A2/E/B 完整六节 |
| Step 4 | （复用 Step 3 内联 report-*） | 判断逻辑已内联 |
| Step 5 | val-returns-are-valuation · val-sensitivity-ranking · val-relative-valuation-discipline · val-cheap-is-king · narr-bayesian-net · narr-barbell · narr-prosperity-trap | R/I/A1/A2/E/B 完整六节 |

---

## 附录C：六阶流水线汇总表模板

完整分析必须在最终报告中呈现以下汇总表：

| 步骤 | 核心结论 | 判停状态 | 数据来源 |
|:--:|:--|:--|:--|
| 元层 | 三原则已加载（相关性≠因果/买无人问津/复利谎言） | [通过] | 内联 |
| Step 1 反算 L | L/E3=[倍数]→叙事类型=[...]；三档 L=[...] | [通过] | val-* 手算 |
| Step 2 定位 | 主导机制=[空间叙事/拍卖]；验证重点=[科目] | [通过] | narr-* |
| Step 3 资产负债表 | 红旗=[科目列表]；财务质量=[高/中/低] | [通过/判停] | report-* |
| Step 4 利润表 | 利润质量=[...]；非经占比=[...] | [通过] | report-* 复用 |
| Step 5 预期差 | 预期差=[中性偏正/偏负]；关注信号=[...] | [通过] | val-*/narr-* |
| 执行层 | 报告已生成（DOCX+HTML） | [完成] | 作者引擎(只读) |

**操作建议**：[执行+结论 / 不操作+原因 / 等待+路标条件]
**数据来源标注**：[哪个接口/文件取的什么数据]
"""

# ========================= 组装 =========================
parts = [FRONTMATTER, OVERVIEW]

for tag, step_name, skills in PIPELINE:
    intro = STEP_INTRO.get(tag, "")
    parts.append("\n---\n\n")
    parts.append("## 【%s】%s\n\n" % (tag, step_name))
    if intro:
        parts.append("> %s\n\n" % intro)
    if not skills:
        # Step 4 专属应用指引
        parts.append(
            "本步是作者引擎的执行步，**判断逻辑已内联于 Step 3**（report-balance-sheet-first / report-presumption-guilt /\n"
            "report-fraud-balance-sheet-trace / report-deferred-tax-mirror / report-adjust-not-fraud / report-bamboo-pole）。\n"
            "此处给出利润表专属应用指引：\n\n"
            "1. **利润是意见**：用 Step 3 的「资产负债表优先」排序，把利润表每个科目变化在资产负债表/现金流量表找到对应；\n"
            "   净利润 vs 经营现金流长期背离 = 红旗（report-balance-sheet-first）。\n"
            "2. **调节识别**：收入确认时点、折旧方法、减值计提的会计选择会改写利润——用 report-adjust-not-fraud 判断「挪」的痕迹。\n"
            "3. **递延税照妖镜**：所得税费用与利润总额偏离时，用 report-deferred-tax-mirror 看二阶导方向（压利润 or 放利润）。\n"
            "4. **非经常性损益**：政府补助/投资收益/公允价值变动占比 > 30% 须扣非看（report-* 联动）。\n"
            "5. **回归警惕**：拆分量价/结构时，慎用统计回归，先建逻辑再拟合（x-correlation-not-causation 贯穿）。\n\n"
            "> 完成标准：利润表 28 科目完整、{最新Q1}单季度同比；每个维度配套四要素深度分析（≥150 字/条）。\n"
        )
        continue
    for slug in skills:
        body = embed_skill(slug)
        title = SKILL_TITLE.get(slug, slug)
        parts.append("\n### ▌ %s（原名《%s》）\n\n" % (slug, title))
        parts.append(body)
        parts.append("\n\n")

parts.append(EXEC_LAYER)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))

# 统计
n_embed = sum(len(s) for _, _, s in PIPELINE if s)
print("已生成:", OUT)
print("内联原子 skill 数:", n_embed)
print("输出行数:", len("".join(parts).splitlines()))
