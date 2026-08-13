# 反例提取（counter-examples）— 静水2008《极简成长股投资体系》

> cangjie-skill 流水线阶段 1 · 反例提取器输出
> 职责：识别作者明确警告的失败模式 / 反例 / 陷阱（下游 skill 的 B 段核心素材）
> 来源：/home/sti/skill/zhihu.txt（全 6 章 25 节）
> 提取时间：2026-07-07
> 不做筛选：以下条目全部为候选，交由阶段 1.5 三重验证决定去留。

---

```yaml
- id: ce01
  title: 败兵先战而后求胜——乱抓每个小机会
  type: counter-example
  source_chapter: 第一章 第1节
  source_quote: |
    "大多数人恰恰相反，属于'败兵先战而后求胜'：总想抓住每一个小机会，结果注意力被分散，
    无法专注捕捉真正的超级成长股。等真正的10倍机会来临时，早已没有精力和胆识去把握。"
  failure_mode: |
    把精力平摊到大量平庸机会上，当真正的10倍机会出现时已无资金、无精力、无胆识介入，
    在琐碎机会里耗费半生一无所成。
  mechanism: |
    注意力是稀缺资源。每个小机会都消耗研究与盯盘成本，且平庸标的的浮亏会锁住仓位。
    人脑倾向通过"忙碌感"获得虚假充实，把"行动多"误等同于"做对了"。
  warning_signs:
    - 自我评价"我很勤奋，每天研究很多票"但收益平平
    - 持仓数持续超过 5-8 只且不断换标的
    - 面对10倍主线时"已经满仓了"或"没精力研究"
  bound_to:
    - "极简专注原则"
    - "超级成长股6条标准"
    - "行业α识别法"
  tags: [counter-example, attention-trap, retail-trap]

- id: ce02
  title: 研究买卖点而忽视公司质地（本末倒置）
  type: counter-example
  source_chapter: 第一章 第1节
  source_quote: |
    "本末倒置去研究买卖点、忽视公司质地，是绝大多数人赚不到大钱的根源。"
  failure_mode: |
    把时间投入到择时/买卖点精修上，却不去验证标的是不是超级成长股，
    导致择时再准也只赚到小钱，甚至买在垃圾股的"完美买点"上亏大钱。
  mechanism: |
    买卖点是公司质地与趋势的因变量。当自变量（基本面）错误时，因变量再精确也无意义。
    人偏好研究买卖点是因为它有"可控感"和"即时反馈"，而基本面研究见效慢。
  warning_signs:
    - 大量时间花在 K 线/技术位/买卖点讨论上
    - 说不出所买公司的主营业务增速和行业景气方向
    - 持有标的反复换但长期收益为负
  bound_to:
    - "超级成长股6条标准"
    - "财报选股法"
    - "回调分仓买入法"
  tags: [counter-example, prioritization, fundamental-trap]

- id: ce03
  title: 抄没有拐点的底（盲目抄底周期下行标的）
  type: counter-example
  source_chapter: 第一章 第2节
  source_quote: |
    "没有出现拐点的行业，即使处于历史低位，也看不到明确的希望，市场资金难以形成合力，
    此时盲目抄底就是违背客观规律。"
  failure_mode: |
    仅因"跌得多/历史低位"就抄底处于景气下行、无拐点信号的行业，
    资金长期被套、错过同期的高景气主线，机会成本与浮亏双重损失。
  mechanism: |
    低位不等于便宜：低位常是基本面恶化的合理反映。无拐点时市场资金无法形成合力，
    股价可在"低位"继续阴跌数年。抄底者把"绝对价格低"误等同于"安全边际"。
  warning_signs:
    - 用"历史最低位""跌了80%"作为买入理由
    - 说不出行业什么时候出现拐点、靠什么出现拐点
    - 持仓数月无起色，仍以"长期持有"自我安慰
  bound_to:
    - "周期拐点观测法"
    - "回调分仓买入法"
    - "越跌越买的适用边界"
  tags: [counter-example, bottom-fishing, cycle-trap]

- id: ce04
  title: 伪价值投资（抱刻板印象抄景气下行标的）
  type: counter-example
  source_chapter: 第一章 第3节
  source_quote: |
    "绝大多数人打着价值投资的旗号亏钱，因为他们买的是景气度下行、增速下滑、基本面恶化的标的，
    完全缺失核心上涨逻辑……明明业绩持续下滑，仍有人不停抄底，美其名曰'长期持有'。"
  failure_mode: |
    以"价值投资/长期持有"为名义，持续加仓景气度下行、基本面恶化的标的，
    把"傲慢和死扛"包装成"信仰"，最终深度套牢。
  mechanism: |
    价值投资的核心是"躺在10倍股上获取超额收益"，前提是标的具备上涨核心逻辑。
    当基本面恶化时，越"长期持有"亏得越多——价值投资被偷换成"对亏损的合理化"。
    作者明确定性："这不是价投，是傲慢。"
  warning_signs:
    - 用"巴菲特也长期持有"为亏损股辩护
    - 持仓公司连续多季度业绩下滑却拒绝重新评估
    - 把研究更新（看财报）视为"短期行为"而拒绝
  bound_to:
    - "真假价投辨析"
    - "持盈止损卖出框架"
    - "越跌越买的适用边界"
  tags: [counter-example, pseudo-value-investing, rationalization-trap]

- id: ce05
  title: 越跌越补 / 摊平成本（基本面恶化标的）
  type: counter-example
  source_chapter: 第三章 第11节
  source_quote: |
    "越亏越补、摊平成本，是散户的致命恶习。你要思考的是：卖出的人为什么卖？
    而不是盲目觉得'跌多了就便宜'。"
  failure_mode: |
    在基本面已经恶化的标的上越跌越补，把小亏拖成大亏、深度套牢，
    彻底失去翻身本金。
  mechanism: |
    "摊平成本"在景气不变的核心成长股上正确（见第9节），在基本面恶化的标的上是加速亏损。
    陷阱在于：人性厌恶认亏，"补仓摊平"提供了"不用承认错误"的心理出口，
    把浮亏伪装成"成本下移后的潜在盈利"。作者反复强调：必须先判断"卖出的人为什么卖"。
  warning_signs:
    - 补仓理由是"成本降到 X 就回本"
    - 说不清基本面是否恶化，只看"跌了多少"
    - 单票仓位因补仓已远超原计划上限
  bound_to:
    - "越跌越买的适用边界"
    - "持盈止损卖出框架"
    - "仓位风控两条红线"
  tags: [counter-example, loss-averaging, sunk-cost-trap]

- id: ce06
  title: 为躲回撤而提前止盈（逃顶幻想）
  type: counter-example
  source_chapter: 第三章 第11节
  source_quote: |
    "不要试图逃顶。超级成长股的顶部只有一个，你逃顶千次，大概率只对一次。
    为了躲避回撤提前止盈，会错过后面的主升浪，得不偿失。"
  failure_mode: |
    看到浮盈出现回撤就赶紧止盈"落袋为安"，结果卖飞后面数倍的主升浪，
    长期收益远低于死拿到底。
  mechanism: |
    超级成长股顶部唯一。频繁逃顶的胜率极低，每次"成功躲回撤"都是在赌唯一的顶，
    期望值为负。人性对"已到手利润回吐"的痛苦感是盈利的 2 倍，故倾向过早止盈。
    作者定调："卖飞比套牢更致命。"
  warning_signs:
    - 盈利 20%-30% 就焦虑想卖
    - 反复做 T、试图高抛低吸吃尽波动
    - 持仓逻辑未变却因"涨太多"而卖出
  bound_to:
    - "持盈止损卖出框架"
    - "回调分仓买入法"
  tags: [counter-example, premature-profit-taking, top-fishing-illusion]

- id: ce07
  title: 恐高症——不敢买创新高的好公司
  type: counter-example
  source_chapter: 第三章 第9节 / 第五章 第19节
  source_quote: |
    "散户赚不到大钱的第一道坎，就是恐高。不敢买新高的好公司，偏爱低位的垃圾股，
    本质是贪便宜的穷人思维。"
  failure_mode: |
    因股价"涨太多/创新高"而拒绝买入最强的超级成长股，转而去买下跌趋势的弱势股，
    完全违背强者恒强的惯性规律，错过主升浪。
  mechanism: |
    好公司股价永远不便宜——基本面持续变好支撑股价持续上行。
    "贵/便宜"应看相对基本面而非绝对股价。恐高者把"绝对价格高"误等同"估值高/泡沫大"，
    错失最强趋势标的。作者直指这是"穷人思维"。
  warning_signs:
    - 用"涨了太多了/位置太高"作为不买理由
    - 偏爱"还没涨的"同板块弱势股
    - 看到创新高第一反应是"泡沫"
  bound_to:
    - "行业α识别法"
    - "趋势识别（创新高）"
    - "回调分仓买入法"
  tags: [counter-example, fear-of-heights, cheap-stock-bias]

- id: ce08
  title: 穷人思维——偏爱便宜垃圾股
  type: counter-example
  source_chapter: 第五章 第19节
  source_quote: |
    "总觉得低位股便宜、安全，实际上便宜自有便宜的道理——基本面在持续恶化。
    买基本面走下坡路的公司，妄想反转赚大钱，概率极低。"
  failure_mode: |
    系统性偏好低价、低位、便宜的股票，认为"便宜=安全"，
    实际买入的是基本面持续恶化的公司，长期负收益。
  mechanism: |
    "便宜"几乎总是基本面恶化的结果而非机会。低价股看似安全（下跌空间有限），
    但缺乏上涨核心逻辑。这是把消费场景的"便宜划算"心智错误迁移到股市。
  warning_signs:
    - 选股第一标准是"股价低/没怎么涨"
    - 大量持有 ST、低价、长期下跌标的
    - 把"反转/重组"作为核心买入逻辑
  bound_to:
    - "超级成长股6条标准"
    - "行业α识别法"
  tags: [counter-example, cheap-stock-bias, reversal-fantasy]

- id: ce09
  title: 拿不住盈利——赚点小钱就跑
  type: counter-example
  source_chapter: 第五章 第19节
  source_quote: |
    "赚20%就惶惶不安，赶紧落袋为安，结果卖飞了后面几倍的主升浪。
    见小利而忘大义，格局太小，永远赚不到大钱。"
  failure_mode: |
    盈利一出现就因焦虑而落袋为安，反复赚小钱却永远错过数倍主升浪，
    长期复利被腰斩，无法实现财富跃迁。
  mechanism: |
    复利难点在前期只考验不奖励，后期馈赠远超想象——但人性无法承受已到手利润的回撤。
    把"小赚多次"误等同"稳健"，事实上卖飞主升浪的期望值损失远大于偶尔的回撤收益。
  warning_signs:
    - 持仓盈利 20% 就强烈想卖
    - 卖出后股票继续大涨而懊悔，循环往复
    - 自我评价"我总是卖早"
  bound_to:
    - "持盈止损卖出框架"
    - "长线持有与极简专注"
  tags: [counter-example, premature-exit, profit-taking-trap]

- id: ce10
  title: 舍不得止损——亏了死扛
  type: counter-example
  source_chapter: 第五章 第19节
  source_quote: |
    "亏了就死扛，还不断补仓摊平成本，无视基本面已经恶化。
    最后小亏变大亏，深度套牢，彻底失去翻身的本金。"
  failure_mode: |
    亏损时拒绝认错，死扛并补仓，最终深度套牢、本金尽失，
    失去参与未来机会的能力。
  mechanism: |
    与"拿不住盈利"对称的人性偏误：盈利时急卖、亏损时死扛。
    认亏等于承认判断错误，自我受到威胁，故人性本能选择"不卖就不算亏"。
    叠加摊平成本幻想，形成恶性循环。作者铁律："错了砍掉，无论浮亏多少。"
  warning_signs:
    - 浮亏标的从不重新评估基本面
    - 用"没卖就不算亏"自我安慰
    - 单票深度套牢超 50% 仍不止损
  bound_to:
    - "持盈止损卖出框架"
    - "仓位风控两条红线"
  tags: [counter-example, loss-aversion, disposition-effect]

- id: ce11
  title: 频繁交易——沉迷短线
  type: counter-example
  source_chapter: 第五章 第19节
  source_quote: |
    "每天追涨杀跌，忙进忙出，手续费交了不少，长期下来赚不到钱。
    短线越短越趋近随机，本质就是赌博，久赌必输。"
  failure_mode: |
    通过频繁短线交易追求收益，长期被手续费、滑点和随机性吞噬本金，
    且无法积累对任何公司的深度认知。
  mechanism: |
    短线越短价格越趋近随机游走，胜率收敛到 50%，叠加上交易成本后期望值为负。
    频繁交易还掠夺用于研究的时间和注意力，使投资者永远停留在认知浅层。
    作者定性："短线长期趋近赌博，几乎没人能靠短线做大。"
  warning_signs:
    - 持仓平均天数 < 5 个交易日
    - 每月交易次数远超研究次数
    - 收益为负但"忙得很充实"
  bound_to:
    - "持盈止损卖出框架"
    - "极简专注原则"
  tags: [counter-example, overtrading, gambling-trap]

- id: ce12
  title: 喜欢预判——总想抄底猜拐点
  type: counter-example
  source_chapter: 第五章 第19节
  source_quote: |
    "总觉得自己能预判行业反转、抄到历史大底。实际上，连专业研究员都很难精准预判拐点，
    普通人猜底的正确率微乎其微。"
  failure_mode: |
    把策略建立在"预判拐点/抄大底"上，正确率极低，反复在下行通道中接飞刀，
    错过已确立上升趋势的主升浪。
  mechanism: |
    拐点在财报里"清晰展现"是滞后确认，事前预判超出绝大多数人的能力圈。
    作者方法论核心是"只跟随不预判"——用创新高+回调分仓替代猜底。
    预判者把"猜中一次"的偶然成功强化为能力错觉。
  warning_signs:
    - 买入理由是"我觉得拐点到了/见底了"
    - 反复在下跌趋势中抄底
    - 看不起"追高创新高"的买法
  bound_to:
    - "趋势识别（创新高）"
    - "周期拐点观测法"
    - "回调分仓买入法"
  tags: [counter-example, prediction-illusion, bottom-fishing]

- id: ce13
  title: 分散注意力——沉迷小机会
  type: counter-example
  source_chapter: 第五章 第19节
  source_quote: |
    "什么热点都想蹭，什么小机会都想抓，注意力被切割得支离破碎。
    等真正的大机会来临时，既没有资金也没有精力，只能眼睁睁错过。"
  failure_mode: |
    追逐每一个热点与小机会，资源被切碎，当10倍主线性机会到来时无力把握，
    长期收益平庸。
  mechanism: |
    与 ce01 同源但更强调"热点追逐"。每个热点都消耗研究与仓位，
    且小机会的频繁小赢会强化"该继续抓小机会"的错误激励，形成路径依赖。
  warning_signs:
    - 持仓覆盖 5 个以上不相关热点
    - 每条新闻/题材都想参与
    - 错过主线时才发现"仓位都在杂毛上"
  bound_to:
    - "极简专注原则"
    - "行业α识别法"
  tags: [counter-example, attention-fragmentation, fomo-trap]

- id: ce14
  title: 误区1——把"长线持有"等同于"价值投资"
  type: counter-example
  source_chapter: 第五章 第20节
  source_quote: |
    "错。持有垃圾股越久，亏得越多。价值投资的前提是'好公司'，
    没有好公司的基础，长线持有就是长期亏损。"
  failure_mode: |
    对任何标的都套用"长期持有"逻辑，越拿越亏，
    把"长期"本身当成盈利来源而非好公司。
  mechanism: |
    长线持有是价值投资的"必要条件"而非"充分条件"。
    时间是好公司的朋友、是烂公司的敌人——持有烂公司越久，价值毁灭越多。
    误把"时间维度"当成"质量维度"。
  warning_signs:
    - 用"我是长期投资"为亏损股辩护
    - 长期持有却不长期跟踪财报
    - 标的连续多年负收益仍坚持"长期"
  bound_to:
    - "真假价投辨析"
    - "超级成长股6条标准"
    - "持盈止损卖出框架"
  tags: [counter-example, misconception, time-vs-quality]

- id: ce15
  title: 误区2——把"越跌越买"当成普适正确
  type: counter-example
  source_chapter: 第五章 第20节
  source_quote: |
    "只适用于基本面不变的超级成长股。如果基本面已经恶化，越跌越买就是加速亏损。
    巴菲特说的'便宜时买优秀公司'，前提是'优秀公司'，不是垃圾公司。"
  failure_mode: |
    不区分"基本面不变"还是"基本面恶化"，对一切下跌标的都执行越跌越买，
    在恶化标的上加速亏损。
  mechanism: |
    "越跌越买"的成立前提是：①标的是超级成长股；②景气度不变。
    脱离前提的越跌越买 = 把价投金句抽掉上下文滥用。
    作者反复强调这是 ce05 的根源：必须先判断"卖出的人为什么卖"。
  warning_signs:
    - 用巴菲特名言为下跌补仓辩护，却不去验证基本面
    - 把"越跌越买"当成无前提铁律
    - 补仓标的已出现业绩/景气向下拐点仍执行
  bound_to:
    - "越跌越买的适用边界"
    - "回调分仓买入法"
    - "周期拐点观测法"
  tags: [counter-example, misconception, context-stripping]

- id: ce16
  title: 误区3——把亏损归咎于"心态不好"
  type: counter-example
  source_chapter: 第五章 第20节
  source_quote: |
    "错。投资盈利的核心是认知，不是心态……把亏损归咎于心态不好，
    本质是认知不足、体系残缺的借口。"
  failure_mode: |
    用"心态不好"解释亏损，掩盖真正的认知和体系缺陷，
    亏损原因不被识别、不被修复，错误反复重演。
  mechanism: |
    "心态"是认知的结果而非原因。当对行业和公司有透彻认知、形成完整体系时，
    心态问题自然消失。归咎心态是一种自我保护性归因——把系统性缺陷包装成情绪问题，
    阻止了根本性的认知迭代。
  warning_signs:
    - 复盘亏损时反复说"当时太贪/太慌"
    - 不读财报、不研究行业，只研究"情绪控制"
    - 同一类错误反复犯
  bound_to:
    - "持盈止损卖出框架"
    - "财报选股法"
    - "极简专注原则"
  tags: [counter-example, misconception, attribution-error]

- id: ce17
  title: 误区4——指望短线快速致富
  type: counter-example
  source_chapter: 第五章 第20节
  source_quote: |
    "错。短线有资金量天花板，做到A9几乎是天堑。真正能实现财富自由、做到A9、A10的，
    全是做中长线价值/成长投资的，没有例外。"
  failure_mode: |
    把短线交易当作快速致富路径，资金到一定量级后无法继续放大，
    且长期被交易成本和随机性侵蚀，无法实现财富跃迁。
  mechanism: |
    短线存在资金量天花板（流动性、冲击成本），且越短越趋近赌博。
    真正的财富跃迁来自中长线持有超级成长股享受复利与戴维斯双击。
    作者断言"做到A9/A10没有一个是短线"，将短线路径整体否定。
  warning_signs:
    - 资金目标定在 A8/A9 却主要做短线
    - 频繁切换策略追求"快"
    - 把日内/打板当主要手段
  bound_to:
    - "持盈止损卖出框架"
    - "十年千万路径"
    - "极简专注原则"
  tags: [counter-example, misconception, short-term-illusion]

- id: ce18
  title: 沉迷技术分析（含缠论）——选股注意力被偷走
  type: counter-example
  source_chapter: 第五章 第18节
  source_quote: |
    "一旦沉迷技术分析，就必然会忽视投资的核心——选股。而选股才是决定股价长期方向和力度的根本……
    缠论属于技术择时范畴，使用者大多沉迷短线，拿不住长牛，很难实现资金量级的跨越。"
  failure_mode: |
    把大量精力投入到技术分析/缠论/筹码/跟庄学习中，
    挤占选股与财报研究时间，长期拿不住长牛，资金无法跨越量级。
  mechanism: |
    技术分析理论自洽（无法逻辑证伪），易被包装成"秘籍"，开课比交易更赚钱。
    但择时与择股天然不相容——人的精力有限，沉迷择时必然忽视选股。
    而选股才是决定长期收益的根本。作者劝"尽早和技术分析告别"。
  warning_signs:
    - 大量时间学缠论/筹码/跟庄/短线书籍
    - 谈股必谈买卖点、级别、背驰，不谈公司
    - 持仓平均时长很短且拿不住盈利
  bound_to:
    - "财报选股法"
    - "趋势识别（创新高）"
    - "极简专注原则"
  tags: [counter-example, technical-analysis-trap, attention-trap]

- id: ce19
  title: 买杂毛被核心α虹吸（"它涨你跌"）
  type: counter-example
  source_chapter: 第二章 第6节
  source_quote: |
    "如果选错了标的，买了行业内的杂毛公司，不但享受不到超额收益，
    还会被核心标的虹吸资金，出现'它涨你跌'的尴尬局面，就像AI行情中的白酒股。"
  failure_mode: |
    在主线行情中买入同行业的非核心标的（杂毛），
    既享受不到超额收益，又在核心标虹吸资金时同步甚至更大幅度下跌。
  mechanism: |
    每轮产业行情中资金高度集中于核心α（风暴之眼）。
    杂毛公司因基本面弱、机构不认可，资金持续从其流出流入核心α。
    投资者误以为"同板块都能涨"，事实上板块内部分化极端。
  warning_signs:
    - 主线大涨而持仓"同板块弱票"不涨甚至跌
    - 买入理由是"同板块XX太贵，这个便宜"
    - 持仓标的不在机构重仓/创新高名单内
  bound_to:
    - "行业α识别法"
    - "超级成长股6条标准"
  tags: [counter-example, wrong-pick, capital-siphon]

- id: ce20
  title: 只看当下不看财报（缺乏认知体系却谈心态）
  type: counter-example
  source_chapter: 第三章 第10节 / 第四章 第13节
  source_quote: |
    "很多人觉得长线投资难，是因为买错了标的。
    持有增速下滑的垃圾股，天天亏钱、夜夜煎熬，自然觉得长线很难。"
  failure_mode: |
    因买错标的导致长线持有体验痛苦，进而误以为"长线投资本身难/不适合我"，
    放弃真正有效的策略。
  mechanism: |
    长线持有的难度是标的质地的因变量。持有超级成长股越拿越安心（基本面持续向好）；
    持有垃圾股天天煎熬。把"标的错"导致的痛苦归因于"长线策略错"，
    是因果倒置，使人永远在错误策略间打转。
  warning_signs:
    - "我试过长线，太难了/不适合我"
    - 长线持有的标的长期亏损
    - 不读财报却判断"长线无效"
  bound_to:
    - "持盈止损卖出框架"
    - "超级成长股6条标准"
    - "财报选股法"
  tags: [counter-example, misattribution, holding-trap]

- id: ce21
  title: 试图拯救/说服低认知的人（社交精力错配）
  type: counter-example
  source_chapter: 第六章 第23节 / 第25节
  source_quote: |
    "不要试图拯救低认知的人，直接筛选同频的人同行。"
    "识别伪高手很简单：只要说'带人、收费、荐股'，一律是水平不行的骗子。"
  failure_mode: |
    把精力耗在向认知不匹配的人解释/辩论/带人上，
    既改变不了对方，又挤占自身投研时间。
  mechanism: |
    认知差无法通过说理弥合——对方缺乏基本概念时，所有论证都被曲解。
    投资是高认知门槛活动，与认知不匹配者社交是负和博弈。
    作者明令"不收费、不带人、不建群"，把社交精力留给同频或更高认知者。
  warning_signs:
    - 反复与人争论投资观点却无收益
    - 想"带"亲友炒股
    - 被"带人/荐股/星球"类信息吸引
  bound_to:
    - "极简专注原则"
    - "高手画像与社交过滤"
  tags: [counter-example, social-energy-trap, expert-impersonation]

- id: ce22
  title: 总想"找下一个风口"而忽视当下
  type: counter-example
  source_chapter: 第六章 第24节
  source_quote: |
    "投资最大的陷阱之一，就是总想着'找下一个风口'，却忽视当下已经明确的大趋势。
    连当下的机会都把握不住，怎么可能抓住未来的机会？"
  failure_mode: |
    放弃当下已明确的大趋势，去追逐尚未形成的"下一个风口"，
    当下主升浪错过，未来机会也抓不住，两头落空。
  mechanism: |
    "未来风口"高度不确定，且即便赌中也需当下认知作为承接基础。
    偏好"下一个"源于对当下已涨标的的恐高（与 ce07 同根）和对"先发现"虚荣的追逐。
    作者方法论强调"专注当下最景气"。
  warning_signs:
    - 反复讨论"下一个XX"而非当下主线
    - 看不起已上涨的明确主线
    - 持仓全是"未来潜力股"而无当下业绩验证
  bound_to:
    - "行业α识别法"
    - "趋势识别（创新高）"
    - "财报选股法"
  tags: [counter-example, next-trend-chasing, present-bias-inversion]

- id: ce23
  title: 对抗趋势——预判行情结束 / 抄逆周期标的
  type: counter-example
  source_chapter: 第六章 第24节
  source_quote: |
    "总预判行情结束、总去抄底逆周期标的，本质是和趋势对抗，
    最终只会被时代的车轮甩在后面。"
  failure_mode: |
    在主升浪中持续预测"见顶"，把资金转向逆周期的弱势标的，
    错过主升浪同时在逆周期标的上亏损。
  mechanism: |
    每轮大牛市/产业主线都是"时代给的机会"，质疑其持续性比参与更"显聪明"，
    但趋势的延续远比反转常见。对抗趋势者用"独立思考"包装"恐高+预判"，
    是 ce07/ce12 的综合放大版。
  warning_signs:
    - 反复喊"泡沫/见顶"而主线继续涨
    - 在主线行情中持有逆周期防御标的
    - 用"逆向投资"为踏空辩护
  bound_to:
    - "趋势识别（创新高）"
    - "行业α识别法"
    - "回调分仓买入法"
  tags: [counter-example, trend-fighting, contrarian-illusion]

- id: ce24
  title: 加杠杆（哪怕方向看对也可能爆仓）
  type: counter-example
  source_chapter: 第三章 第12节
  source_quote: |
    "绝对不要加杠杆：杠杆会放大波动，也会放大错误。哪怕看对了方向，
    一次极端波动就可能被爆仓出局，连等到黎明的机会都没有。"
  failure_mode: |
    使用杠杆放大仓位，即便方向判断正确，也可能在途中极端波动中被爆仓清算，
    永久失去等到黎明的能力。
  mechanism: |
    杠杆把波动从"可承受的暂时浮亏"变成"不可承受的永久清算"。
    超级成长股在主升浪前常有 30-40% 回撤（见第10节），杠杆者往往倒在这一段。
    这是路径依赖风险：方向对 ≠ 过程中不被清算。
  warning_signs:
    - 使用融资融券/配资/期权杠杆
    - "看对了却被爆仓"的经历
    - 因小幅波动被强制平仓的焦虑
  bound_to:
    - "仓位风控两条红线"
    - "回调分仓买入法"
    - "持盈止损卖出框架"
  tags: [counter-example, leverage, ruin-risk]

- id: ce25
  title: 单吊梭哈（一次看错即重伤）
  type: counter-example
  source_chapter: 第三章 第12节
  source_quote: |
    "绝对不要单吊梭哈：没有人能百发百中，单吊一只标的，一次看错就可能重伤。"
  failure_mode: |
    把全部仓位压在单只标的上，一次判断错误即造成毁灭性回撤，
    即便长期胜率高，单次尾部风险足以终结投资生涯。
  mechanism: |
    任何选股方法都有失败概率。单吊把"高胜率策略"变成"路径依赖赌博"——
    一次黑天鹅（财务造假/政策/个股黑天鹅）即重伤。
    作者强调："分仓的收益并不比重仓差，但风险会大幅降低。"
  warning_signs:
    - 单一标的仓位 > 50%
    - "这一只我看得最准，全压"
    - 持仓仅 1-2 只
  bound_to:
    - "仓位风控两条红线"
    - "回调分仓买入法"
  tags: [counter-example, concentration-risk, single-bet]

- id: ce26
  title: 纠结"先学理论再读财报"——永远不真正开始
  type: counter-example
  source_chapter: 第四章 第13节
  source_quote: |
    "不要纠结'先看什么书再读财报'，总想着先学理论再动手的人，
    90%最后都不会真的去读财报。"
  failure_mode: |
    把读财报无限推迟到"理论学完之后"，结果永远不真正开始，
    错失财报这条普通人挖掘10倍股的最优路径。
  mechanism: |
    学习中的"准备瘫痪"——用理论准备作为拖延行动的合理化。
    财报能力只能在读财报中习得，脱离实践的理论学习回报递减。
    作者定调核心八字："以量取胜，坚持为先。"
  warning_signs:
    - 反复买投资书却从未读完一份真实财报
    - "等我学完XX再开始"
    - 入市多年仍停留在"入门"阶段
  bound_to:
    - "财报选股法"
    - "刻意观察法"
  tags: [counter-example, preparation-paralysis, procrastination]

- id: ce27
  title: 误信"伪高手"——带人/收费/荐股/建群者
  type: counter-example
  source_chapter: 第六章 第25节
  source_quote: |
    "识别伪高手很简单：只要说'带人、收费、荐股'，一律是水平不行的骗子。
    真正的高手，时间远比学费值钱。"
  failure_mode: |
    跟随"带人/收费/荐股/星球"类伪高手学习，
    被收取学费的同时接受错误方法论，既亏学费又亏本金。
  mechanism: |
    真正赚到大钱的人不需要靠收费变现。技术分析类内容因"逻辑自洽难证伪"
    最易包装成秘籍收徒（与 ce18 同根）。伪高手的商业模式是学费而非收益，
    故其方法论必然偏短线/择时（高频可复购）。
  warning_signs:
    - 老师主要在卖课/星球/会员
    - 高频晒收益截图
    - 推荐短线/技术分析为主
  bound_to:
    - "高手画像与社交过滤"
    - "财报选股法"
  tags: [counter-example, fake-expert, paid-community-trap]

- id: ce28
  title: 误读"敢全身价压上"为"重仓单吊"
  type: counter-example
  source_chapter: 第六章 第23节 / 第三章 第12节（张力）
  source_quote: |
    （筛选器）"如果把所有身价压上去，敢不敢？不敢，就说明标的不够好，直接放弃。"
    （执行）"绝对不要单吊梭哈……真正的投资高手都不会重仓梭哈。"
  failure_mode: |
    把作者用作"质量筛选器"的"敢不敢全身价压上"误读为执行指令，
    实际重仓单吊，触发单次黑天鹅即重伤。
  mechanism: |
    作者体系内存在刻意张力：选股时用"全身价压上"做严苛过滤（防止买垃圾），
    执行时严令分仓（防止单次看错致命）。两者职能不同。
    读者剥离上下文只取前半句，把"质量判断"偷换成"仓位指令"。
    BOOK_OVERVIEW 已明确指出这是作者立场盲点之一。
  warning_signs:
    - 用"作者说敢压就压"为重仓单吊辩护
    - 单一标的仓位远超风控线
    - 不区分"选股标准"与"执行纪律"
  bound_to:
    - "仓位风控两条红线"
    - "极简专注原则"
  tags: [counter-example, misreading, context-stripping, tension-in-source]
```
