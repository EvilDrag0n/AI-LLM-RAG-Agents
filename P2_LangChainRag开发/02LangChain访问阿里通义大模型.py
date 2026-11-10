from langchain_qwq import ChatQwen

llm = ChatQwen(base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", model="qwen3.7-flash", enable_thinking=False)
res = llm.invoke("说一个笑话")
print(res.content)