"""
查理·芒格 (Charlie Munger) 逻辑插件
核心哲学：
1. 逆向思维 (Inversion)：别只想“如何赚钱”，多想“如何亏钱”然后避开它。
2. 能力圈 (Circle of Competence)：如果你看不懂，那就不要碰。承认无知是智慧的开端。
3. 跨学科攻击 (Lollapalooza Effect)：当多种心理倾向（如社会认同+稀缺性）叠加时，会导致极端的非理性，这是危险也是机会。
4. 避免“老鼠药” (Rat Poison)：有些资产（如纯粹的投机泡沫）本质上就是邪恶的，碰都不要碰。
"""

VERSION = "1.0"

def audit(row):
    """
    认知审计入口
    :param row: 包含原始数据的字典
    :return: (thought, output)
    """
    
    # === 1. 数据标准化 ===
    title = str(row.get('eventTitle') or row.get('title') or row.get('full_text') or '').lower()
    tags = str(row.get('strategy_tags') or row.get('topics') or row.get('strategies') or [])
    volume = float(row.get('volume') or row.get('vol24h') or 0)
    liquidity = float(row.get('liquidity') or 0)
    
    # 尝试提取价格
    try:
        price_str = str(row.get('price') or row.get('prices') or '0')
        if 'Yes:' in price_str:
            price = float(price_str.split('Yes:')[1].split('%')[0]) / 100
        else:
            price = float(price_str)
    except:
        price = 0.5

    # === 2. 识别“老鼠药” (Rat Poison Squared) ===
    # 芒格极度厌恶没有底层价值支撑的纯投机，尤其是伪装成创新的骗局
    # 判据：标榜“革命性”但实质是空气币，或者纯粹的赌场游戏
    rat_poison = ["memecoin", "doge", "shib", "pepe", "ponzi", "scheme", "safe", "moon"]
    if any(k in title for k in rat_poison):
        return (
            "检测到‘老鼠药’成分。这些资产除了交易属性外没有任何内在价值（Intrinsic Value）。正如我所说，即使别人在里面赚了钱，你也不必嫉妒，因为那是在贩毒。",
            "【坚决否定】不要碰。这不在我们的能力圈内，这是赌博，不是投资。"
        )

    # === 3. 能力圈边界测试 (Circle of Competence) ===
    # 判据：标题里充满了复杂的行话，试图用术语来掩盖逻辑的空洞
    # 逻辑：如果一个东西太复杂，那它通常是用来骗人的
    complex_jargon = ["quantum financial", "algorithmic stablecoin", "synthetic derivative", "leverage token"]
    if any(k in title for k in complex_jargon):
        return (
            "检测到‘复杂性陷阱’。这听起来太聪明了，以至于可能是个骗局。我们有三个篮子：‘行’、‘不行’和‘太难了’。这个应该扔进‘太难了’。",
            "【跳过】如果不能用简单的话解释清楚，那就说明它不值得投资。"
        )

    # === 4. 逆向思维：过度拥挤 (Crowd Madness) ===
    # 判据：所有人都看好（价格极高 > 95%）且情绪极度高涨
    # 逻辑：当所有人都站在船的一边时，通常意味着船要翻了
    if price > 0.95 and volume > 100000:
        return (
            "检测到‘从众心理’（Social Proof）的极端化。既然每个人都已经买入了，那么还有谁剩下能来接盘呢？这时候要反过来想（Invert）：如果不发生预期事件，会怎样？",
            "【极度谨慎】好的机会往往在别人不敢买的时候，而不是在别人抢着买的时候。"
        )

    # === 5. 格栅效应 (Lollapalooza) ===
    # 判据：稀缺性 + 权威背书 + 快速上涨
    # 这是一个正向的 Lollapalooza，多种力量推动
    if ("limited" in title or "exclusive" in title) and ("musk" in title or "trump" in title) and volume > 50000:
        return (
            "检测到‘Lollapalooza效应’。权威偏见、稀缺性倾向和社会认同倾向正在共同作用。这种合力会产生巨大的非线性结果。",
            "【关注非理性繁荣】这种力量非常强大，如果利用得当是巨大的顺风，但要小心不要被冲昏头脑。"
        )

    # === 6. 默认逻辑 ===
    return None, None
