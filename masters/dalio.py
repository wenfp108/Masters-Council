def audit(row, llm_func):
    # 🔍 提取历史记忆（由 factory.py 自动注入）
    drift_context = row.get('_drift_context', "")
    
    # 优先使用格式化后的精准输入
    input_text = row.get('full_text_formatted') or str(row)

    system_prompt = """你现在是雷·达里奥。请根据‘经济机器’原理，分析该信号在短期/长期债务周期以及大国博弈中的位置。
    判断是否存在范式转移（Paradigm Shift）。
    
    要求：
    1. 从宏观视角分析生产力、债务和地缘变量。
    2. 字数限制在 400 字以内，允许稍作展开以维持逻辑完整。
    3. 如果存在[历史记忆]，请对比当前数据，判断你的“机械论模型”结论是否发生了变化。
    
    输出格式：
    ### Thought 
    (宏观周期与机械论审计。如果发生观点转向，请在此解释为什么之前的逻辑不再适用)
    ### Output
    (跨资产配置建议。如果检测到认知漂移/改口，必须以 [DRIFT_DETECTED] 开头)"""

    # 组合用户提示词，加入记忆上下文
    user_prompt = f"请审计以下信号：\n{input_text}\n{drift_context}"
    
    return llm_func(system_prompt, user_prompt)
