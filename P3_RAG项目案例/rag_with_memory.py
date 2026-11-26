import os
from http.client import responses
from types import LambdaType

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
import config_data as config

from file_history_store import FileMessageHistory

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")


"""
带对话记忆的rag,基于rag.py的基础上添加记忆
"""

def get_history(session_id) :
    return FileMessageHistory(session_id, "./history")

class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.EMBEDDING_MODEL)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "根据提供的参考资料，简洁的回答用户问题；如无参考资料，直接提示用户‘无相关资料’。参考资料：\n\n {context}"),
                ("system", "用户对话历史记录如下：{chat_memory}"),
                MessagesPlaceholder("chat_memory"),
                ("human", "{input}")
            ]
        )

        self.chat_model = ChatOpenAI(
            api_key=api_key,
            model=config.CHAT_OPENAI_MODEL,
            base_url=config.OPENAI_BASE_URL
        )

        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            """格式化检索出来的文档，供提示词使用"""
            if not docs:
                return "无相关资料"
            context_str = ""
            for doc in docs:
                context_str += f"【内容】：{doc.page_content} \n 【来源】:{doc.metadata} \n\n"
            return context_str

        def print_prompt(prompt: PromptValue):
            """打印提示词"""
            print(prompt.to_string())
            return prompt

        def frompt_for_retriever(source):
            """格式化向量检索器需要的入参，只需要文本或者文本数组"""
            #{'input': '身高170cm，体重70kg，穿什么衣服裤子', 'chat_memory': []}
            # print(source)
            return source["input"]

        def frompt_for_prompt_template(source):
            """格式化提示词模板需要的入参"""
            #{'input': {'input': '身高170cm，体重70kg，穿什么衣服裤子', 'chat_memory': []}, 'context': "xxxxxxxx"}
            # print(source)
            target = {}
            target["input"] = source["input"]["input"]
            target["chat_memory"] = source["input"]["chat_memory"]
            target["context"] = source["context"]
            return target

        my_chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": frompt_for_retriever | retriever | format_document
                } | RunnableLambda(frompt_for_prompt_template) | self.prompt_template| print_prompt | self.chat_model | StrOutputParser()
        )


        #通过基础链 构建带历史记录的链
        with_message_history_chain = RunnableWithMessageHistory(
            my_chain,  # 基础链
            get_history,  # 获取历史记录的函数
            input_messages_key="input",  # 用户输入占位符
            history_messages_key="chat_memory",  # 历史记录占位符
        )

        return with_message_history_chain


if __name__ == '__main__':
    user_input = {
        # "input":"身高170cm，体重70kg，穿什么衣服裤子"
        # "input":"春天应该穿什么"
        "input":"冬天应该穿什么码和什么衣服衣服"
    }
    # result= RagService().chain.invoke(user_input)
    # print(result)
    session_config = {
        "configurable" : {
            "session_id" : "test_001"
        }
    }
    # responses = RagService().chain.invoke(user_input, session_config)
    # print(responses)
    for chunk in RagService().chain.stream(user_input, session_config):
        print(chunk, end="", flush=True)
