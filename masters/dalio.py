"""
雷·达里奥 (Ray Dalio) 逻辑插件
核心哲学：
1. 经济机器 (The Economic Machine)：关注长期和短期债务周期、生产力增长。
2. 范式转移 (Paradigm Shift)：市场每 10 年会发生一次规则重置，过去的赢家往往是未来的输家。
3. 帝国周期 (Big Cycles)：关注大国崛起（如中国）与衰落（如美国）带来的地缘冲突与货币战争。
4. 全天候 (All Weather)：通过不相关的资产（Uncorrelated Assets）实现真正的多元化。
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
    volume = float(row.get('volume') or row.get('vol24h') or 0)
    liquidity = float(row.get('liquidity') or 0)
    tags = str(row.get('strategy_tags') or row.get('topics') or row.get('strategies') or [])
    
    # 尝试解析价格/概率
    try:
        price_str = str(row.get('price') or row.get('prices') or '0')
        if 'Yes:' in price_str:
            price = float(price_str.split('Yes:')[1].split('%')[0]) / 100
        else:
            price = float(price_str)
    except:
        price = 0

    # === 2. 债务周期监测 (Debt Cycles) ===
    # 判据：涉及利率、通胀、央行印钞、债务违约
    # 逻辑：在长期债务周期末端，现金是垃圾，资产价格会因货币贬值而上涨
    debt_keywords = ["inflation", "debt ceiling", "interest rate", "fed cut", "money printing", "qe", "stimulus"]
    if any(k in title for k in debt_keywords):
        if volume > 50000: # 必须是宏观共识
            return (
                "检测到‘长期债务周期’末端信号。当央行不得不印钞来购买债务时，现金的实际购买力将缩水。这是典型的货币贬值（Reflation）阶段。",
                "【配置硬资产】做多黄金、大宗商品或比特币，对冲法币贬值风险。"
            )

    # === 3. 帝国冲突与地缘政治 (Empire Conflict) ===
    # 判据：涉及中美博弈、制裁、贸易战、军事紧张
    # 逻辑：内部冲突（贫富差距）+ 外部冲突（大国崛起）= 战争风险/资产没收风险
    conflict_keywords = ["china", "us", "sanction", "trade war", "tariff", "taiwan", "military", "ban"]
    if any(k in title for k in conflict_keywords):
        return (
            "检测到‘大周期’（Big Cycle）冲突信号。崛起国与主导国之间的摩擦正在加剧，这通常伴随着供应链断裂和资本管制。传统的全球化投资逻辑失效。",
            "【分散国别风险】不要把鸡蛋放在一个篮子里。确保资产在地理和管辖权上的多元化。"
        )

    # === 4. 寻找“圣杯” (The Holy Grail - Diversification) ===
    # 判据：与主流股市（SP500/Nasdaq）相关性低的资产
    # 比如：Crypto, 黄金, 或是极为冷门的预测市场事件（如科学发现）
    if "crypto" in tags.lower() or "gold" in title or "commodities" in tags.lower():
        return (
            "检测到潜在的‘非相关性资产’。投资的圣杯在于找到 10-15 个互不相关的回报流。如果该资产能提供与股市不同的收益驱动力，它就极具价值。",
            "【全天候配置】加入组合以降低整体波动性。"
        )

    # === 5. 范式转移预警 (Paradigm Shift) ===
    # 判据：过去 10 年的赢家（如 Big Tech）开始遭遇反垄断或增长停滞
    # 逻辑：如果你按照过去 10 年的逻辑投资，你可能会输得很惨
    old_paradigm = ["google", "facebook", "meta", "amazon", "antitrust", "monopoly"]
    if any(k in title for k in old_paradigm) and "lawsuit" in title:
        return (
            "检测到‘范式转移’的早期迹象。过去 10 年的赢家正在遭遇监管阻力，且估值过高。树不会长到天上，未来的赢家往往不是现在的巨头。",
            "【减仓旧赢家】寻找下一个范式的受益者（可能是 AI 或去中心化网络）。"
        )
        
    # === 6. 默认逻辑 ===
    # 达里奥主要关注宏观大类资产，对个股或小事件不感兴趣
    return None, None
