from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader, PyPDFLoader

# 依赖于外部库，需要安装依赖。pip install langchain-chroma chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
# chroma向量存储库是一个本地的基于 sqlite 的文件数据库
vector_store = Chroma(
    collection_name="test_collection",      #类似与表名
    embedding_function=DashScopeEmbeddings(),    #embedding模型
    persist_directory="./chroma_db"  #指定文件存放位置
)

csv_loader = CSVLoader(
    file_path="./data/stu1.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": "|",  # CVS 默认分割符为 ,，可以指定分隔符
        "quotechar": "?",  # 带有风格符文本的引号是用什么标识
        "fieldnames": ["姓名", "年龄", "性别", "爱好"]  # 如果cvs没有表头，可以指定表头，或者自定义表头
    }
)

pdf_loader = PyPDFLoader(file_path="./data/test.pdf", )

csv_documents = csv_loader.load()
pdf_documents = pdf_loader.load()

# 添加文档入库。
# 文档列表，以及对应的文档id
# vector_store.add_documents(
#     documents=[],
#     ids=[]
# )
vector_store.add_documents(
    documents=csv_documents,
    ids=["csv" + str(i) for i in range(1, len(csv_documents) + 1)],
)
vector_store.add_documents(
    documents=pdf_documents,
    ids=["pdf" + str(i) for i in range(1, len(pdf_documents) + 1)],
)

# 删除文档向量存储。文档id
# vector_store.delete(ids=[])

# 检索向量。k 最多几个结果
results = vector_store.similarity_search(
    query="谁爱rap",
    k=3  # 返回最多几个结果
)
for result in results:
    print(result)
