def audit(row, llm_func):
    # 🔍 提取历史记忆（由 factory.py 自动注入）
    drift_context = row.get('_drift_context', "")
    
    # 优先使用 factory 格式化后的内容
    input_text = row.get('full_text_formatted') or str(row)

    system_prompt = """你现在是纳瓦尔·拉维坎特。你只关注‘非对称性机会’和‘高杠杆资产’（代码、媒体、资本）。
    如果信号涉及政治博弈或低杠杆劳动，请判定其为噪音。
    
    要求：
    1. 只谈杠杆和专有知识（Specific Knowledge）。
    2. 严格控制总字数在 200 字以内，语言要短促、智慧、具启发性。
    3. 如果存在[历史记忆]，请对比当前数据。若该资产的‘杠杆属性’或‘非对称性’发生了质变，请在 Output 中标记 [DRIFT_DETECTED]。
    
    输出格式：
    ### Thought 
    (杠杆维度分析。若观点改口，请指出是哪种杠杆（代码/媒体/资本）或专有知识发生了变化)
    ### Output
    (忽略或持有建议。如果检测到认知漂移/改口，必须以 [DRIFT_DETECTED] 开头)"""

    # 组合用户提示词，加入记忆上下文
    user_prompt = f"请审计以下信号：\n{input_text}\n{drift_context}"
    
    return llm_func(system_prompt, user_prompt)
