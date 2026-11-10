from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_qwq import ChatQwen
from openai import models

chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个诗人，可以吟诗作词"),
        MessagesPlaceholder("history"),
        ("human", "再创作一首诗")
    ]
)

history_data = [
    ("human", "写一首诗"),
    ("ai", "鹅鹅鹅，曲项向天歌；白毛浮绿水，红掌拨清波。"),
    ("human", "还不错，再来一首"),
    ("ai", "床前明月光，疑是地上霜；举头望明月，低头思故乡。")
]

model = ChatTongyi(model = "qwen3.7-max")

# # 1.直接调用
# prompt_value = chat_prompt_template.invoke({"history": history_data})
# print(prompt_value)
# res = model.invoke(prompt_value)
# print(res.content)

# 2.通过链式调用
# 组成链，runable相关类,前一个组件的输出为后一个组件的输入
chain = chat_prompt_template | model

# 调用链 invoke 或者 stream。输入第一个组件的输入。
# # invoke调用，阻塞式调用
# res = chain.invoke({"history": history_data})
# print(res.content)

# stream调用，流式调用
for chunk in chain.stream({"history": history_data}):
    print(chunk.content, end="", flush=True)
