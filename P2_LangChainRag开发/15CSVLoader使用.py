from langchain_community.document_loaders import CSVLoader

csv_loader1 = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8"
)

# 一次性加载
documents = csv_loader1.load()
for document in documents:
    print(type(document), document)

# # 懒加载
# for document in csv_loader1.lazy_load() :
#     print(document)

# CSVLoader 的其他参数
csv_loader2 = CSVLoader(
    file_path="./data/stu1.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": "|",   #CVS 默认分割符为 ,，可以指定分隔符
        "quotechar": "?",   #带有风格符文本的引号是用什么标识
        "fieldnames":["姓名", "年龄", "性别","爱好"] #如果cvs没有表头，可以指定表头，或者自定义表头
    }
)

# # 懒加载
# for document in csv_loader2.lazy_load() :
#     print(document)
