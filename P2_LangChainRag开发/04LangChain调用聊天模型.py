from langchain_qwq import ChatQwen
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

qwen = ChatQwen(base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", model="qwen3.7-flash", enable_thinking=False)

system_message = SystemMessage("只输出必要内容")
human_message = HumanMessage("给我写一首唐诗")
messages = [system_message, human_message]
res = qwen.stream(input=messages)
for chunk in res:
    print(chunk.content, end="", flush=True)