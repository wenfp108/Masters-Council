
"""
塔勒布 (Nassim Nicholas Taleb) 逻辑插件
核心哲学：
1. 反脆弱 (Antifragile)：从混乱和波动中获益。
2. 凸性 (Convexity)：寻找“损失有限，收益无限”的不对称机会。
3. 林迪效应 (Lindy Effect)：对于非自然事物，存活越久，预期剩余寿命越长。
4. 风险共担 (Skin in the Game)：不信任没有下注的决策者。
"""

VERSION = "2.1"

def audit(row):
    """
    认知审计入口
    :param row: 包含原始数据的字典
    :return: (thought, output)
    """
    
    # === 1. 数据标准化 ===
    # 提取关键指标，兼容 Polymarket / Twitter / GitHub / Paper
    title = str(row.get('eventTitle') or row.get('title') or row.get('full_text') or '').lower()
    
    # 价格/概率：如果是 GitHub/Twitter，默认视为空
    try:
        price_str = str(row.get('price') or row.get('prices') or row.get('probability') or '0.5')
        # 简单清洗：提取 Yes 的价格 (针对 Polymarket)
        if 'Yes:' in price_str:
            price = float(price_str.split('Yes:')[1].split('%')[0]) / 100
        else:
            price = float(price_str)
    except:
        price = 0.5

    volume = float(row.get('volume') or row.get('vol24h') or row.get('stars') or 0)
    liquidity = float(row.get('liquidity') or row.get('retweets') or 0)
    tags = str(row.get('strategy_tags') or row.get('topics') or row.get('strategies') or [])

    # === 2. 尾部风险狩猎 (Tail Risk Hunting) ===
    # 塔勒布策略的核心：买入极度便宜的“虚值期权”，赌黑天鹅
    # 判据：价格极低 (< 5%) 但有显著的流动性（说明有人在对冲）
    if 0 < price < 0.05: 
        if liquidity > 50000: # 必须有足够的流动性，否则是死盘
            return (
                "检测到典型‘凸性’机会（Convexity）。市场认为该事件发生概率极低（<5%），但巨大的流动性表明 smart money 正在进行尾部对冲。如果黑天鹅发生，收益是不对称的（10x-100x）。",
                "【配置彩票】买入作为反脆弱配置。损失仅限于 5%，但潜在收益不可估量。"
            )

    # === 3. 林迪效应检测 (Lindy Effect) ===
    # 判据：老旧的技术/事物 + 依然保持高热度
    # 比如：Bitcoin, Gold, 或者经典的算法仓库
    lindy_assets = ["bitcoin", "gold", "linux", "python", "tcp/ip", "sql"]
    if any(asset in title for asset in lindy_assets):
        if volume > 1000: # 依然活跃
            return (
                "检测到强‘林迪效应’。这些事物已经经受住了时间的考验，其预期寿命随着存活时间的增加而增加。不要赌它们会消失。",
                "【长期做多】时间是它们的朋友，不是敌人。"
            )

    # === 4. 伪科学与干预主义过滤 (Iatrogenics) ===
    # 塔勒布厌恶没有经过时间检验的复杂“新科技”或“专家干预”
    # 判据：标榜“颠覆性”但极其新、波动率低（伪稳态）
    fragile_keywords = ["central bank", "modern monetary theory", "mmt", "risk free", "guaranteed"]
    if any(k in title for k in fragile_keywords):
        return (
            "检测到‘脆弱性’（Fragility）。试图消除波动性的系统往往在积累隐性风险，最终导致毁灭性的崩溃。这是典型的医源性损伤（Iatrogenics）。",
            "【极度警惕/做空】该系统试图违背自然规律，最终会以惨烈的方式回归均值。"
        )
    
    # === 5. 风险共担 (Skin in the Game) ===
    # 判据：如果是 Twitter/言论，检查是否是实干家
    if 'user_name' in row: # 这是一个推文或言论
        user = str(row.get('user_name', '')).lower()
        # 塔勒布喜欢：创业者、交易员 (Elon Musk, Naval, etc.)
        # 塔勒布讨厌：官僚、只有理论的学者、记者
        operators = ["musk", "founder", "builder", "trader"]
        bureaucrats = ["journalist", "columnist", "official", "analyst"]
        
        if any(op in user or op in str(row.get('user_bio', '')).lower() for op in operators):
            return (
                "检测到‘风险共担’者。此人不仅在发表观点，而且在游戏中下注。由于他在承担下行风险，他的观点更值得信赖。",
                "【增加权重】听取实干家的建议，忽略空谈家。"
            )
        
        if any(b in user or b in str(row.get('user_bio', '')).lower() for b in bureaucrats):
            return (
                "检测到‘代理人问题’。此人不需要为自己的错误预测承担后果（No Skin in the Game）。他们往往为了博取眼球而制造噪音。",
                "【忽略】切勿听信不需要为错误买单的人。"
            )

    # === 6. 默认逻辑 ===
    # 如果没有显著的不对称性，那就是“平均斯坦”的噪音
    return None, None
