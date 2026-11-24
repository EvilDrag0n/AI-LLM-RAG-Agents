import os
from itertools import chain

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnablePassthrough

from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
import config_data as config

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")


class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.EMBEDDING_MODEL)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "根据提供的参考资料，简洁的回答用户问题；如无参考资料，直接提示用户‘无相关资料’。参考资料：\n\n {context}"),
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
            if not docs:
                return "无相关资料"
            context_str = ""
            for doc in docs:
                context_str += f"【内容】：{doc.page_content} \n 【来源】:{doc.metadata} \n\n"
            return context_str

        def print_prompt(prompt: PromptValue):
            # print(prompt)
            return prompt

        my_chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": retriever | format_document
                } | self.prompt_template| print_prompt | self.chat_model | StrOutputParser()
        )

        return my_chain


if __name__ == '__main__':
    user_input = "身高170cm，体重70kg，穿什么衣服裤子"

    # result= RagService().chain.invoke(user_input)
    # print(result)

    for chunk in RagService().chain.stream(user_input):
        print(chunk, end="", flush=True)
