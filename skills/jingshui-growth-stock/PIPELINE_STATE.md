# 流水线状态 — jingshui-growth-stock-investing

- **slug**: jingshui-growth-stock-investing
- **来源**: 知乎专栏 https://zhuanlan.zhihu.com/p/2056833702274110592 （本地 /home/sti/skill/zhihu.txt）
- **作者**: 静水2008
- **类型**: 长文（成长股投资体系）
- **状态**: ✅ 全部完成（2026-07-07/08）

## 阶段进度

- [x] 阶段 0 — 整文理解 → `BOOK_OVERVIEW.md`（用户已确认骨架）
- [x] 阶段 1 — 5 提取器并行提取 → `candidates/`（170 条候选）
- [x] 阶段 1.5 — 三重验证 → `verified.md`（13 单元通过，37%）+ `rejected/rejected.md`（用户已确认全做）
- [x] 阶段 2 — RIA++ 构造 13 个 SKILL.md（description 均 ≤300 字）
- [x] 阶段 3 — Zettelkasten 链接 → `INDEX.md`（mermaid 图 + 学习顺序）+ `GLOSSARY.md`（18 术语）+ 各 skill related_skills 回填
- [x] 阶段 4 — 压力测试 → 13 个 `test-prompts.json` + `test-results.md`；独立 sub-agent 盲测 30/30 = 100%（13 跨 skill 诱饵全正确、4 无关全 none、13 正面全命中），无需回炉
- [x] 阶段 5 — 交付 → `DIGEST.md`（约 7000 字精华长文）+ **已安装 13 个 skill 到 `~/.claude/skills/`**（用户级，宿主已加载）

## 13 个 skill

V01 super-growth-stock-criteria / V02 industry-alpha-locking / V03 prosperity-and-inflection /
V04 three-selection-methods / V05 trend-following-entry / V06 scale-in-and-risk-control /
V07 hold-or-cut-exit / V08 financial-report-signals / V09 deliberate-observation /
V10 seven-retail-sins / V11 real-vs-fake-value-investing / V12 minimalist-focus / V13 ten-year-wealth-path

## 安装位置

`~/.claude/skills/<slug>/`（用户级，所有项目可用）。宿主已成功加载（已出现在可用 skill 列表）。

## 后续

如需持续进化，喂给 darwin-skill：`darwin evolve books/jingshui-growth-stock-investing/`（用各 skill 的 test-prompts.json 做 ratcheting 自动进化）。
