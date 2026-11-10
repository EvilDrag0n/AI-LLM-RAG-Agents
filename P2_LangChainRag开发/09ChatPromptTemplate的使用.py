from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_qwq import ChatQwen

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

prompt_text = chat_prompt_template.invoke(input={"history":history_data})
# print(type(prompt_text))
# print("")
# print(prompt_text.to_string())
# print("")
# print(prompt_text.to_messages())
# print("")
# print(prompt_text.to_json())

llm = ChatQwen(model="qwen3.7-flash", base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
response = llm.invoke(prompt_text.to_messages())
print(response.content)