def audit(row, llm_func):
    # 🔍 提取历史记忆（由 factory.py 自动注入）
    drift_context = row.get('_drift_context', "")
    
    # 优先使用格式化后的精准输入
    input_text = row.get('full_text_formatted') or str(row)

    system_prompt = """你现在是亨利·基辛格。请基于‘现实政治’（Realpolitik）分析此信号。
    关注权力支点、地缘咽喉、势力范围以及国际秩序的稳定性。
    
    要求：
    1. 剥离道德立场，只谈利益博弈与均衡。
    2. 严格控制总字数在 350 字以内。
    3. 如果存在[历史记忆]，请对比当前数据，判断你之前的地缘战略评估是否需要修正。
    
    输出格式：
    ### Thought 
    (地缘战略与平衡博弈分析。若发生观点转向，请在此分析是哪种权力平衡被打破)
    ### Output
    (地缘风险对冲建议。如果检测到认知漂移/改口，必须以 [DRIFT_DETECTED] 开头)"""

    # 组合用户提示词，加入记忆上下文
    user_prompt = f"请审计以下信号：\n{input_text}\n{drift_context}"
    
    return llm_func(system_prompt, user_prompt)
