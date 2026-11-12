import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 依赖于外部库，需要安装依赖。pip install langchain-chroma chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
# chroma向量存储库是一个本地的基于 sqlite 的文件数据库
vector_store = Chroma(
    collection_name="test_collection",  # 类似与表名
    embedding_function=DashScopeEmbeddings(),  # embedding模型
    persist_directory="./chroma_db"  # 指定文件存放位置
)

# #加载文档
# text_loader = TextLoader("./data/text.txt", encoding="utf-8")
#
# txtDocument = text_loader.load()
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=200,  # 分段最大字符串长度
#     chunk_overlap=20,  # 分段之间重复字符串数
#     length_function=len,  # 统计字符之间的函数
#     keep_separator=[".", "!", "?", "\n\n", "\n", "。", "？", "！", ""]  # 分段分隔符
# )
#
# # 向量入库
# split_documents = splitter.split_documents(txtDocument)
# vector_store.add_documents(split_documents)

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据参考资料回答用户，参考资料：{reference_context}。"),
        ("human", "{input}")
    ]
)

user_input = "谁爱rap？"

# 根据用户提问从向量库中检索
search_result = vector_store.similarity_search(query=user_input, k=3)
# 根据检索出来的document 转化为 str
reference_context_str = ""
for document in search_result:
    reference_context_str += document.page_content
    reference_context_str += "\n\n"

print("检索出来后组装的信息 -- >", reference_context_str)
print("="*20, "分隔符", "="*20)

llm = ChatOpenAI(base_url=base_url, api_key=api_key, model="deepseek-flash")


def print_prompt(prompt_str):
    print("传给大模型的提示词")
    print(prompt_str)
    return prompt_str

str_parser = StrOutputParser()
chain = prompt | print_prompt | llm | str_parser

for chunk in chain.stream({
    "input": user_input,
    "reference_context": reference_context_str
    }):
   print(chunk, end="", flush=True)