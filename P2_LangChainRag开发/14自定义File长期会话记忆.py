import os, json
from typing import Sequence

from dotenv import load_dotenv
from langchain_core.messages import message_to_dict, messages_from_dict, messages_to_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

#自定义文件消息历史
class FileMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, file_path):
        self.session_id = session_id
        self.file_path = file_path
        self.message_path = os.path.join(self.file_path, self.session_id)
        os.makedirs(os.path.dirname(self.message_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # 新消息追加历史消息
        self.messages.extend(messages)

        dict_messages = messages_to_dict(messages)

        # 写入文件
        with open(self.message_path, 'w', encoding='utf-8') as f:
            json.dump(dict_messages, f, ensure_ascii=False, indent=2)

    #从文件中读取历史消息
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.message_path, 'r', encoding='utf-8') as f:
                dict_messages = json.load(f)
                return messages_from_dict(dict_messages)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.message_path, 'w', encoding='utf-8') as f:
            json.dump([], f)


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
def get_history(session_id) :
    return FileMessageHistory(session_id, "./history")

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

    # res = history_chain.invoke({"input": "小明有两只狗"}, config)
    # print("第1次执行", res)
    #
    # res = history_chain.invoke({"input": "小红有一只猫"}, config)
    # print("第2次执行", res)

    res = history_chain.invoke({"input": "小明和小红一共有几只宠物"}, config)
    print("第3次执行", res)

    # res = history_chain.invoke({"input": "小花也养了一只猫"}, config)
    # print("第4次执行", res)
    #
    # res = history_chain.invoke({"input": "现在呢？"}, config)
    # print("第5次执行", res)
