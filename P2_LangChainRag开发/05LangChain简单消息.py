from langchain_qwq import ChatQwen

qwen = ChatQwen(base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", model="qwen3.7-flash", enable_thinking=False)

messages = [
    ("system", "只回复必要的信息"),
    ("human", "生成一首7言绝句。"),
    ("ai", "春水碧于天，画船听雨眠。垆边人似月，皓腕凝霜雪。"),
    ("human", "这不是7言绝句吧？"),
    ("ai", """
    抱歉，刚才引用了韦庄《菩萨蛮》的词句。以下是正确的七言绝句：
    
    **《静夜思》**
    李白
    床前明月光，疑是地上霜。
    举头望明月，低头思故乡。
    """),
    ("human", "这也不是七言绝句吧？说一下七言绝句的格式"),
    ("ai", """
    七言绝句格式：每首四句，每句七个字。
    平仄、押韵需符合格律规范（通常二、四句押平声韵）。
    """),
    ("human", "那你刚生成的是七言绝句吗？先回答我，然后重新生成")
]

res = qwen.stream(input=messages)

for chunk in res:
    print(chunk.content, end="", flush=True)