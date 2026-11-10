import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"
# 第一次提示词模板
first_template = PromptTemplate.from_template("我的邻居姓{lastName}, 刚生了一个{gender},帮她取一个名字。严格以JSON格式输出，key为name,value为姓名，不要输出额外内容")
# 第二次提示词模板
second_template = PromptTemplate.from_template("解析这个名字：{name}的含义")

# 解析器
json_parser = JsonOutputParser()
str_parser = StrOutputParser()

# 大模型
llm = ChatOpenAI(api_key=api_key, base_url=base_url, model="deepseek-flash")

# 构建链
chain = first_template | llm | json_parser | second_template | llm | str_parser

# 阻塞调用
# res = chain.invoke({"lastName": "张", "gender": "女"})
# print(res)

# 流式调用
for chunk in chain.stream({"lastName": "张", "gender": "女"}) :
    print(chunk, end="", flush=True)