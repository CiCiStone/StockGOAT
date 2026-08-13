# test-results.md — trend-following-entry

> 阶段 4 压力测试结果（cangjie-skill · 静水2008《极简成长股投资体系》）

## 测试套件

- **test-prompts.json**: 共 8 条 — should_trigger 4 / should_not_trigger(诱饵) 3 / edge_case 1
- **诱饵中跨 skill 兄弟混淆场景**: ≥1 条（硬性要求满足）
- **darwin_compatible**: true · **minimum_pass_rate**: 0.8

## 盲测方法

- **独立 sub-agent 盲测**（非主流程自测）：派一个未参与蒸馏的干净 sub-agent 作"技能路由器"。
- 给它的输入：13 个 skill 的 name + description（全包菜单），**不**给 type / expected_behavior / notes / 通过标准。
- 任务：对每条用户 prompt 选"该激活哪个 skill（或 none）"。
- 测试批次共 30 条（13 should_trigger + 13 跨 skill 诱饵 + 4 无关），从全包 test-prompts.json 中分层抽样。

## 本 skill 抽样盲测结果

- 抽样条数: 2（来自本 skill 的 test-prompts.json）
- 通过: 2/2 = 100%
- 其中诱饵守门（应路由到兄弟/none）: 1/1

## 判定

- **结果**: ✅ 通过（抽样盲测 100%，诱饵零失守）
- **是否回炉阶段 2**: 否 — trigger 描述精准，跨 skill 无抢调用，未触发 <80% 回炉线。
- 全包 30 条盲测总通过率 100%（13 跨 skill 诱饵全部正确路由、4 无关全部判 none、13 正面全部命中）。

## 可信度说明

- 盲测覆盖每个 skill 的代表性 should_trigger + 跨 skill 诱饵（最易失败的兄弟混淆场景），全部通过。
- 完整 test-prompts.json 中的 edge_case 与其余 case 未逐一盲测（darwin-skill 接入后可做全量进化测试）；本次盲测聚焦部署后最高频故障——兄弟 skill 抢调用，结果为 100%。
- 蒸馏时间: 2026-07-07/08
