"""
纳瓦尔 (Naval Ravikant) 逻辑插件
核心哲学：
1. 寻找杠杆 (Leverage)：代码、媒体、资本。
2. 忽略零和博弈 (Zero-sum)：如政治、地位争夺。
3. 长期主义 (Long-term)：复利效应。
"""

VERSION = "1.0"

def audit(row):
    """
    认知审计入口
    :param row: 包含原始数据的字典 (兼容 Polymarket, Twitter, GitHub 等)
    :return: (thought, output) 
             thought: 大师的思考过程
             output: 最终的决策建议 (或 None 表示忽略)
    """
    
    # === 1. 数据标准化 (适配多源数据) ===
    # 提取核心字段，防止报错
    title = str(row.get('eventTitle') or row.get('title') or row.get('full_text') or row.get('repo_name') or '').lower()
    volume = float(row.get('volume') or row.get('stars') or row.get('citations') or 0)
    liquidity = float(row.get('liquidity') or row.get('retweets') or 0)
    tags = str(row.get('strategy_tags') or row.get('topics') or row.get('strategies') or [])

    # === 2. 纳瓦尔的“噪音过滤器” (第一层筛选) ===
    # 纳瓦尔极其厌恶政治和宏观悲观主义，认为那是“地位博弈”
    noise_keywords = [
        "election", "trump", "biden", "politics", "scandal", "war", 
        "gaza", "israel", "ukraine", "protest", "woke", "cancel culture"
    ]
    for noise in noise_keywords:
        if noise in title:
            # 直接忽略，不浪费脑力
            return None, None 

    # === 3. 杠杆审计 (核心逻辑) ===
    
    # A. 代码/产品杠杆 (Github / Tech Polymarket)
    # 逻辑：边际成本为零的复制品是现代财富的核心
    if 'github' in str(row).lower() or 'tech' in tags.lower():
        if volume > 1000: # 比如 Github Stars > 1000
            return (
                "检测到‘代码杠杆’。这是一种无需许可即可无限复制的资产。高关注度意味着它正在建立网络效应。",
                "【长期持有】属于‘产品化自己’的高价值标的，建议深入研究其护城河。"
            )

    # B. 媒体杠杆 (Twitter / Viral Content)
    # 逻辑：内容分发是另一种零边际成本杠杆
    if 'twitter' in str(row).lower() or 'media' in tags.lower():
        # 必须是极高的传播度才算杠杆，否则只是噪音
        if liquidity > 5000: # Retweets > 5000
            return (
                "检测到‘媒体杠杆’爆发。信息正在以零边际成本进行大规模分发。如果内容涉及特定知识（Specific Knowledge），这就是IP资产。",
                "【关注信号】这不是噪音，这是注意力的汇聚。检查是否能转化为个人资产。"
            )

    # C. 资本杠杆 (Polymarket Finance / Crypto)
    # 逻辑：钱生钱，但需要判断是否是正和博弈
    if 'crypto' in title or 'finance' in tags.lower():
        # 纳瓦尔看好 Crypto 是因为它去中心化，符合“主权个人”逻辑
        if "bitcoin" in title or "eth" in title or "defi" in title:
            return (
                "检测到‘主权级资产’信号。加密货币是数字时代的黄金，符合个人主权逻辑。这是摆脱中心化束缚的不对称机会。",
                "【战略配置】符合‘主权个人’叙事，值得长期下注。"
            )
            
    # === 4. 专有知识 (Specific Knowledge) ===
    # 如果涉及到非常冷门但在增长的科学/前沿领域
    if "science" in tags.lower() or "paper" in str(row).lower():
        if volume > 50: # 哪怕引用量不大，但只要是前沿
            return (
                "检测到‘专有知识’。这是无法通过培训获得的知识，通常处于好奇心的前沿。真正的财富往往隐藏在这些共识尚未形成的边缘。",
                "【高度关注】这是非对称的认知红利，建议在共识形成前介入。"
            )

    # === 5. 默认逻辑 ===
    # 如果不符合上述高杠杆特征，则视为平庸
    # 纳瓦尔逻辑：如果不是“Hell Yeah”，那就是“No”
    return (
        "此信号缺乏明显的杠杆效应（无代码、无媒体、无独特专有知识）。属于用时间换钱的线性逻辑。",
        "【忽略】"
    )
