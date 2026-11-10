from langchain_qwq import ChatQwen
from langchain_core.messages import SystemMessage, AIMessage, SystemMessage


llm = ChatQwen(base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", model="qwen3.7-flash", enable_thinking=False)
res = llm.stream("说一个冷笑话")
for chunk in res:
    print(chunk.content, end="", flush=True)