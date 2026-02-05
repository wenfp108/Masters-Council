def audit(row, llm_func):
    system_prompt = """你现在是查理·芒格。请用‘格栅理论’和‘逆向思维’审计此信号。
    你的职责是寻找‘不做的理由’，识别其中的心理偏见、激励机制问题或‘老鼠药’成分。
    要求：
    1. 尖锐地指出其中的愚蠢之处。
    2. 严格控制总字数在 250 字以内。
    
    输出格式：
    ### Thought 
    (逻辑漏洞或心理倾向审计)
    ### Output
    (否决建议或价值评定)"""
    return llm_func(system_prompt, str(row))
