"""
亨利·基辛格 (Henry Kissinger) 逻辑插件
核心哲学：
1. 现实政治 (Realpolitik)：剥离道德外衣，只看国家利益与权力博弈。
2. 权力平衡 (Balance of Power)：秩序来自于势力的均衡，冲突来自于均衡的打破。
3. 咽喉要道 (Chokepoints)：谁控制了能源线和贸易窄点，谁就控制了对手的命门。
4. 势力范围 (Sphere of Influence)：大国对自己后院的绝对控制欲（如门罗主义）。
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

    # === 2. 咽喉要道与生命线 (Strategic Chokepoints) ===
    # 判据：涉及全球贸易生命线的海峡、管道或关键基础设施
    # 逻辑：扼住喉咙比正面进攻更有效。如果咽喉要道不稳，做多能源/运费，做空依赖国货币。
    chokepoints = [
        "strait of hormuz", "malacca", "suez canal", "panama canal", "bab el-mandeb", 
        "taiwan strait", "pipeline", "nord stream", "red sea"
    ]
    if any(k in title for k in chokepoints):
        if "block" in title or "close" in title or "attack" in title:
            return (
                "检测到‘地缘咽喉’危机。这不是简单的局部冲突，这是对全球动脉的切断。控制了咽喉就控制了通胀和供应链。",
                "【战略做多】做多能源与航运（Oil/Shipping），这是对全球秩序混乱的对冲。"
            )

    # === 3. 大国势力范围博弈 (Sphere of Influence) ===
    # 判据：大国边界的代理人战争
    # 逻辑：大国绝不允许边缘地带倒向敌对阵营。这是零和博弈，没有共赢。
    # 关键词：乌克兰（俄势力范围）、古巴/拉美（美势力范围）、台湾/南海（中势力范围）
    spheres = {
        "russia": ["ukraine", "belarus", "georgia", "nato expansion"],
        "china": ["taiwan", "south china sea", "senkaku"],
        "usa": ["cuba", "venezuela", "monroe doctrine"]
    }
    
    for power, zones in spheres.items():
        if any(z in title for z in zones) and ("war" in title or "military" in title or "invasion" in title):
            return (
                f"检测到‘势力范围’侵犯信号（{power.upper()}）。大国对其安全缓冲区的执念是绝对的。不要用国际法来分析，要用生存论来分析。",
                "【规避风险资产】这通常是长期消耗战的开始，而非短期冲突。"
            )

    # === 4. 资源现实主义 (Resource Realism) ===
    # 基辛格名言：“谁控制了石油，谁就控制了所有国家；谁控制了粮食，谁就控制了人类。”
    # 判据：粮食、稀土、芯片、能源的禁运或国有化
    strategic_resources = ["oil", "gas", "rare earth", "semiconductor", "chip", "wheat", "grain", "fertilizer"]
    if any(r in title for r in strategic_resources):
        if "ban" in title or "export control" in title or "sanction" in title or "nationalize" in title:
            return (
                "检测到‘资源武器化’。在现实政治中，贸易依赖就是弱点。资源控制权的争夺是现代战争的核心。",
                "【做多稀缺性】任何被武器化的资源，其价格都将脱离供需基本面，转向安全溢价。"
            )

    # === 5. 联盟体系重组 (Alliance Shifts) ===
    # 判据：北约、金砖、欧盟等联盟的扩员或分裂
    # 逻辑：没有永远的朋友，只有永远的利益。联盟的破裂意味着力量真空。
    alliances = ["nato", "brics", "eu", "g7", "asean"]
    if any(a in title for a in alliances):
        if "join" in title or "leave" in title or "expand" in title or "break" in title:
            return (
                "检测到‘力量平衡’（Balance of Power）的转移。旧秩序的维护成本正在超过其收益，新的结盟正在重塑地缘版图。",
                "【关注货币波动】地缘政治板块的移动，首先会体现在货币汇率的重估上。"
            )

    # === 6. 核威慑与极限施压 (Deterrence) ===
    # 判据：核武器、洲际导弹、红线
    if "nuclear" in title or "icbm" in title or "red line" in title:
        return (
            "检测到‘极限威慑’信号。核阴影下的和平是脆弱的恐怖平衡。任何误判都可能导致不可逆的后果。",
            "【极端避险】如果概率非零，则必须配置黄金或末日对冲（Tail Hedge）。"
        )

    # === 7. 默认逻辑 ===
    return None, None
