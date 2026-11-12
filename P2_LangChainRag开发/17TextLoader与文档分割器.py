from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_loader = TextLoader("./data/text.txt", encoding="utf-8")

txtDocument = text_loader.load()
# print(txtDocument)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,         #分段最大字符串长度
    chunk_overlap=20,       # 分段之间重复字符串数
    length_function=len,    # 统计字符之间的函数
    keep_separator=[".", "!", "?", "\n\n", "\n", "。", "？", "！", ""]     #分段分隔符
)

split_text = splitter.split_documents(txtDocument)
for text in split_text:
    print(text)