"""
索罗斯 (George Soros) 逻辑插件
核心哲学：
1. 反身性 (Reflexivity)：价格影响基本面，基本面反过来影响价格，形成自我强化的反馈回路。
2. 易错性 (Fallibility)：市场共识往往是错的，寻找“主流偏见”与现实的背离。
3. 盛衰周期 (Boom/Bust)：在正反馈初期果断介入，在趋势逆转时毫不留情地做空。
"""

VERSION = "1.0"

def audit(row):
    """
    认知审计入口
    :param row: 包含原始数据的字典
    :return: (thought, output)
    """
    
    # === 1. 数据标准化 ===
    # 提取关键指标
    price = float(row.get('price') or row.get('probability') or 0) # 0-1 之间
    day_change = float(row.get('day_change') or row.get('dayChange') or row.get('growth_views') or 0)
    volume = float(row.get('volume') or row.get('vol24h') or 0)
    liquidity = float(row.get('liquidity') or 0)
    title = str(row.get('eventTitle') or row.get('full_text') or '').lower()
    
    # 绝对值处理，方便计算力度
    abs_change = abs(day_change)

    # === 2. 捕捉“正反馈回路” (Positive Feedback Loop) ===
    # 索罗斯最喜欢的猎物：价格上涨引发更多的关注和资金，从而引发进一步上涨
    # 判据：价格剧烈波动 + 巨量成交 + 趋势向上
    if day_change > 0.10: # 日涨幅超过 10% (Polymarket/Crypto 语境)
        if volume > 50000: # 成交量巨大，说明不是干拉，有资金共识
            return (
                "检测到典型的‘反身性’正反馈。价格飙升正在吸引投机资本，而投机资本的涌入进一步验证了看涨叙事。基本面已不再重要，重要的是偏见正在自我强化。",
                "【果断做多】正反馈初期，顺势而为，并在趋势减弱时第一时间离场。"
            )

    # === 3. 捕捉“负反馈崩盘” (Negative Feedback Loop) ===
    # 判据：价格剧烈下跌 + 巨量成交
    if day_change < -0.10:
        if volume > 50000:
            return (
                "检测到恐惧驱动的负反馈回路。下跌导致保证金追缴和止损，从而导致进一步下跌。这是市场结构的崩溃，而非价值回归。",
                "【做空/做空波动率】市场进入恐慌模式，顺应‘总投降’趋势。"
            )

    # === 4. 识别“主流偏见”的裂痕 (The Flaw in Consensus) ===
    # 索罗斯名言：“我通过寻找由于错误的观念而产生的泡沫赚钱。”
    # 判据：胜率极高（共识极强）但开始出现松动（价格下跌）
    if price > 0.85: # 市场认为这件事 85% 稳了
        if day_change < -0.05: # 但是今天突然跌了 5%
            return (
                "检测到‘主流偏见’出现裂痕。市场过度确信（>85%），但价格走势与共识背离。一旦信念动摇，这种不对称的预期差会导致剧烈的修正。",
                "【尝试做空】利用市场的‘易错性’，博弈共识崩塌的非对称收益。"
            )

    # === 5. 宏观叙事与政经博弈 (Macro & Politics) ===
    # 与纳瓦尔不同，索罗斯热衷于政治和宏观，因为政策会强行改变游戏规则
    political_keywords = ["election", "fed", "rate", "policy", "regulation", "ban", "tariff"]
    if any(k in title for k in political_keywords):
        if volume > 100000: # 必须是大钱在博弈
            return (
                "检测到宏观政策干预信号。在非均衡市场中，监管或政策的变化是最大的基本面变量。资金流向表明聪明钱正在重新定价政策风险。",
                "【密切监视】政策导致的不均衡状态是套利的温床。"
            )

    # === 6. 默认逻辑 ===
    # 索罗斯对平庸的市场波动不感兴趣
    return None, None
