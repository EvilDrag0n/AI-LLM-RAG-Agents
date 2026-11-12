from langchain_community.document_loaders import PyPDFLoader

# PyPDFLoader 依赖于 pypdf 包。需要先安装依赖包 pip install pypdf -i https://pypi.tuna.tsinghua.edu.cn/simple
pdf_loader = PyPDFLoader(
    file_path="./data/test.pdf",
    mode="page",  # 读取模式，single 整个文件一次性读取 page 按页读取。默认为 page
    password=None  # PDF 文件密码
)

pdf_documents = pdf_loader.load()
for document in pdf_documents:
    print(document)