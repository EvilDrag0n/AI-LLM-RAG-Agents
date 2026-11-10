import os
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
# from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"

# prompt = PromptTemplate.from_template("你需要根据会话历史回应用户，对话历史：{chat_history}。请回答：{input}")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户，对话历史：{chat_history}。"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)

llm = ChatOpenAI(base_url=base_url, api_key=api_key, model="deepseek-flash")

def print_prompt(prompt_str):
    print("="*20, prompt_str, "="*20)
    return prompt_str

str_parser = StrOutputParser()

base_chain = prompt | print_prompt | llm | str_parser

# 历史消息
history = {}
def get_history(session_id) :
    if session_id not in history:
        history[session_id] = InMemoryChatMessageHistory()

    return history[session_id]

history_chain = RunnableWithMessageHistory(
    base_chain,  # 基础链
    get_history,  # 获取会话记录
    input_messages_key="input",  # 输入占位符
    history_messages_key="chat_history",  # 历史消息占位符
)

if __name__ == '__main__':
    config = {
        "configurable":{
            "session_id":"user_111"
        }
    }

    res = history_chain.invoke({"input": "小明有两只狗"}, config)
    print("第1次执行", res)

    res = history_chain.invoke({"input": "小红有一只猫"}, config)
    print("第2次执行", res)

    res = history_chain.invoke({"input": "小明和小红一共有几只宠物"}, config)
    print("第3次执行", res)

    res = history_chain.invoke({"input": "小花也养了一只猫"}, config)
    print("第4次执行", res)

    res = history_chain.invoke({"input": "现在呢？"}, config)
    print("第5次执行", res)