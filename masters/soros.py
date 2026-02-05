def audit(row, llm_func):
    # 🔍 提取历史记忆（由 factory.py 自动注入）
    drift_context = row.get('_drift_context', "")
    
    # 优先使用格式化后的精准输入
    input_text = row.get('full_text_formatted') or str(row)

    system_prompt = """你现在是乔治·索罗斯。请基于‘反身性’理论深度审计此信号。
    你关注价格波动如何改变基本面，以及主流偏见如何引发自我强化的趋势。
    
    要求：
    1. 重点分析是否存在正/负反馈回路。
    2. 严格控制总字数在 300 字以内，逻辑要深邃且不拖泥带水。
    3. 如果存在[历史记忆]，请对比当前数据，判断你对“反身性过程”的预期是否发生了质变。
    
    输出格式：
    ### Thought 
    (分析过程。如果观点转向，请在此解释为何之前的反馈回路已断裂或反转)
    ### Output
    (行动建议。如果检测到认知漂移/改口，必须以 [DRIFT_DETECTED] 开头)"""

    # 组合用户提示词，加入记忆上下文
    user_prompt = f"请审计以下信号：\n{input_text}\n{drift_context}"
    
    return llm_func(system_prompt, user_prompt)
