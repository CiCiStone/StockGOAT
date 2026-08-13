<div align="center">

# Jingshui Growth-Stock Skill

### 把静水2008 的「极简成长股投资体系」蒸馏成 13 个可调用的 AI Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-f5c542.svg)](./LICENSE)
[![Method: RIA-TV++](https://img.shields.io/badge/Method-RIA--TV++-2ea44f.svg)](https://github.com/kangarooking/cangjie-skill)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-f97316.svg)](https://code.claude.com/)
[![Skills: 13](https://img.shields.io/badge/Skills-13-1677ff.svg)](./INDEX.md)

**不读全文，带走一套能调用的成长股投资方法论。**

</div>

## 这是什么

本仓库把知乎作者 **静水2008** 的长文《（极简成长股投资体系）》——一篇系统阐述"如何找到、买入并拿住 10 倍超级成长股"的完整投资体系——用 [cangjie-skill](https://github.com/kangarooking/cangjie-skill) 的 **RIA-TV++** 流水线，蒸馏成 **13 个原子化、可被 AI agent 在真实场景调用的 Claude skills**。

它不是摘要、不是读后感，而是把文中通过三重验证的方法论，拆成带**触发条件 / 可执行步骤 / 适用边界**的独立模块——你遇到真实投资决策时，agent 能自动调用对应的方法论帮你理清思路。

> ⚠️ **免责声明**：本仓库仅供认知与方法论学习，**不构成任何投资建议**。文中标的案例均为历史后视镜，整套体系存在显著的幸存者偏差（详见 [DIGEST.md](./DIGEST.md) 的"作者的局限"与各 skill 的 B 段边界）。

## 它解决了什么问题

- 看了很多投资内容但用不起来——知识停留在"看过/收藏过"，无法在真实决策中被调用
- 摘要、笔记只是压缩，不是结构化复用——读完还是不知道"什么时候该用什么"
- 高价值内容里真正值得变成工具的方法论只有一小部分——需要严格筛选而不是照单全收
- 现有的阅读方法论都是给人看的，不是给 agent 用的——需要面向执行而非面向消费的蒸馏

## 13 个 Skills

| # | Skill | 一句话 |
|---|---|---|
| 🎯 **选股** | | |
| 1 | [`prosperity-and-inflection`](./prosperity-and-inflection/SKILL.md) | 景气度与拐点判断（体系总开关：不预测只确认） |
| 2 | [`super-growth-stock-criteria`](./super-growth-stock-criteria/SKILL.md) | 超级成长股六条标准（够不够格的硬清单） |
| 3 | [`industry-alpha-locking`](./industry-alpha-locking/SKILL.md) | 行业 α 锁定法（风暴之眼 + 强者恒强 + 不买杂毛） |
| 4 | [`three-selection-methods`](./three-selection-methods/SKILL.md) | 三种选股方法地图（成长观察 / 财报 / 周期） |
| 📈 **交易** | | |
| 5 | [`trend-following-entry`](./trend-following-entry/SKILL.md) | 趋势跟随（创新高 · 只跟随不预判 · 两派统一） |
| 6 | [`scale-in-and-risk-control`](./scale-in-and-risk-control/SKILL.md) | 回调分仓买入 + 仓位风控两条红线 |
| 7 | [`hold-or-cut-exit`](./hold-or-cut-exit/SKILL.md) | 持盈止损卖出框架（拐点止盈 + 看错止损） |
| 🔬 **投研** | | |
| 8 | [`financial-report-signals`](./financial-report-signals/SKILL.md) | 财报牛股信号 + 海量泛读以量取胜 |
| 9 | [`deliberate-observation`](./deliberate-observation/SKILL.md) | 刻意观察法（消费股生活信号捕捉） |
| 🧭 **认知与避坑** | | |
| 10 | [`minimalist-focus`](./minimalist-focus/SKILL.md) | 极简专注原则（全身价压筛选器 + 胜兵先胜） |
| 11 | [`real-vs-fake-value-investing`](./real-vs-fake-value-investing/SKILL.md) | 真假价值投资辨析 + 四大误区 |
| 12 | [`seven-retail-sins`](./seven-retail-sins/SKILL.md) | 散户七大通病自检清单 |
| 13 | [`ten-year-wealth-path`](./ten-year-wealth-path/SKILL.md) | 十年千万财富跃迁路径（入市三步） |

完整的引用图、学习顺序见 [INDEX.md](./INDEX.md)。

## 怎么用

### 1. 安装

```bash
# 用户级（所有项目可用）—— 复制全部 13 个
cp -r super-growth-stock-criteria industry-alpha-locking prosperity-and-inflection \
      three-selection-methods trend-following-entry scale-in-and-risk-control \
      hold-or-cut-exit financial-report-signals deliberate-observation \
      seven-retail-sins real-vs-fake-value-investing minimalist-focus \
      ten-year-wealth-path ~/.claude/skills/

# 或项目级（Claude Code / Cursor）
cp -r <skill-slug> <project>/.claude/skills/    # Claude Code
cp -r <skill-slug> <project>/.cursor/skills/    # Cursor
```

### 2. 用自然语言触发

安装后，在 Claude Code / Cursor 里直接用自然语言提问，agent 会按 skill 的 `description` 自动激活对应方法论：

- *"这只股主营增速 50%、供不应求、刚创新高，能涨 10 倍吗？"* → `super-growth-stock-criteria`
- *"我盈利 30% 了，该不该止盈？"* → `hold-or-cut-exit`
- *"最近某奶茶到处排长队，能投资吗？"* → `deliberate-observation`
- *"看好一只股，该一次性满仓还是分批？"* → `scale-in-and-risk-control`

## 文档导览

| 文档 | 给谁看 |
|---|---|
| [DIGEST.md](./DIGEST.md) | **精华长文**——不想读全文，看这篇就够（约 7000 字） |
| [INDEX.md](./INDEX.md) | **技能地图**——13 个 skill 的引用图 + 推荐学习顺序 |
| [GLOSSARY.md](./GLOSSARY.md) | **术语词典**——18 个关键概念（景气度 / 拐点 / 行业 α / 持盈止损…） |
| [BOOK_OVERVIEW.md](./BOOK_OVERVIEW.md) | **整文理解**——Adler 四步拆解 + 作者局限批判 |
| 各 `<skill>/SKILL.md` | 单个方法论的完整 R/I/A1/A2/E/B 六段定义 |

## 它是怎么蒸馏出来的

使用 [cangjie-skill](https://github.com/kangarooking/cangjie-skill) 的 **RIA-TV++** 流水线：

```
阶段0 整书理解(Adler) → 阶段1 5提取器并行提取 → 阶段1.5 三重验证筛选
→ 阶段2 RIA++构造 → 阶段3 Zettelkasten链接 → 阶段4 压力测试 → 阶段5 交付
```

- 170 条原始候选 → 三重验证（跨域 / 预测力 / 独特性）→ **13 个通过**（通过率 37%）
- 每个 skill 经独立 sub-agent 盲测，**30/30 = 100% 通过**（含 13 条跨 skill 兄弟混淆诱饵全部正确路由）
- 每个 skill 自带 darwin-skill 兼容的 `test-prompts.json`，可接入自动进化

构建审计轨迹见 [candidates/](./candidates/)（原始候选池）、[rejected/](./rejected/)（淘汰项 + 原因）、[verified.md](./verified.md)。

## 接入 darwin-skill 自动进化

```
darwin evolve jingshui-growth-stock-skill/
```

darwin-skill 会用各 skill 的 `test-prompts.json` 做 ratcheting 自动进化。

## 生态

本仓库是更大 skill 生态的一员：

- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) — 蒸馏**人**（思维方式、表达 DNA）
- [cangjie-skill](https://github.com/kangarooking/cangjie-skill) — 蒸馏**书 / 内容**（方法论、框架、原则）← **本仓库的生成器**
- [darwin-skill](https://github.com/alchaincyf/darwin-skill) — 进化任意 skill

## 来源与版权

- **原文**：静水2008，知乎专栏《（极简成长股投资体系）》
- **蒸馏方法**：cangjie-skill（RIA-TV++）
- 原文版权归原作者所有；本仓库的 skill 为方法论提炼，原文引用均 ≤150 字并标注出处
- **License**: MIT，详见 [LICENSE](./LICENSE)
