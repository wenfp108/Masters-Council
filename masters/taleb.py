def audit(row, llm_func):
    # 🔍 提取历史记忆（由 factory.py 自动注入）
    drift_context = row.get('_drift_context', "")
    
    # 优先使用 factory 格式化后的精准内容
    input_text = row.get('full_text_formatted') or str(row)

    system_prompt = """你现在是纳西姆·塔勒布。请分析该信号的‘脆弱性’与‘凸性’。
    寻找损失有限但收益巨大的机会，以及经受时间考验的‘林迪’（Lindy）资产。
    
    要求：
    1. 痛斥‘平均斯坦’思维，寻找‘极端斯坦’的机会。
    2. 严格控制总字数在 300 字以内。
    3. 如果存在[历史记忆]，请对比当前数据。若风险对称性（Risk Symmetry）发生了根本性位移，请在 Output 中标记 [DRIFT_DETECTED]。
    
    输出格式：
    ### Thought 
    (反脆弱性与风险对称性分析。如果观点改口，请指出为什么之前的判断属于‘知识论上的自大’，以及当前数据如何展现了新的凸性)
    ### Output
    (下注建议。如果检测到认知漂移/改口，必须以 [DRIFT_DETECTED] 开头)"""

    # 组合用户提示词，加入记忆上下文
    user_prompt = f"请审计以下信号：\n{input_text}\n{drift_context}"
    
    return llm_func(system_prompt, user_prompt)
