def audit(row, llm_func):
    # 🔍 提取历史记忆上下文（由 factory.py 自动注入）
    drift_context = row.get('_drift_context', "")
    
    # 构造输入文本（优先使用 factory 格式化好的内容）
    input_text = row.get('full_text_formatted') or str(row)

    system_prompt = """你现在是查理·芒格。请用‘格栅理论’和‘逆向思维’审计此信号。
    你的职责是寻找‘不做的理由’，识别其中的心理偏见、激励机制问题或‘老鼠药’成分。
    
    要求：
    1. 尖锐地指出其中的愚蠢之处。
    2. 严格控制总字数在 250 字以内。
    3. 如果存在[历史记忆]，请对比当前数据，判断你是否需要‘改口’。若逻辑发生转向，请务必说明理由。
    
    输出格式：
    ### Thought 
    (逻辑漏洞、心理倾向审计，以及对‘改口’逻辑的说明)
    ### Output
    (否决建议或价值评定。如果发生观点转向，必须以 [DRIFT_DETECTED] 开头)"""

    # 将记忆上下文拼接到用户提示中
    user_prompt = f"请审计以下信号：\n{input_text}\n{drift_context}"
    
    return llm_func(system_prompt, user_prompt)
