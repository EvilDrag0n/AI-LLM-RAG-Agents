from langchain_community.document_loaders import JSONLoader

# 需要依赖于 jq 库。安装依赖 pip install jq -i https://pypi.tuna.tsinghua.edu.cn/simple

json_loader = JSONLoader(
    file_path="./data/stu.json",
    # jq_schema=".",          # . 表示json根，即整个json
    # jq_schema=".name",      # .key 表示获取根下某个key的值
    # jq_schema=".hobby[]",          # .[] 表示获取整个数组
    # jq_schema=".hobby[1]",        #[xx] 表示获取数组第几个元素
    jq_schema=".family[].name",   #[].key 表示获取数组中所有对象的key的值
    text_content=False #读取的内容是否为字符串，默认为True
)

document = json_loader.load()
print(document)
