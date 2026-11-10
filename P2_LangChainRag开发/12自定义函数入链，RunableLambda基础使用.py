import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableLambda

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"
# 第一次提示词模板
first_template = PromptTemplate.from_template("我的邻居姓{lastName}, 刚生了一个{gender},查看《诗经》或者《楚辞》帮她取一个名字。严格以JSON格式输出，key为name,value为姓名，不要输出额外内容")
# 第二次提示词模板
second_template = PromptTemplate.from_template("解析这个名字，名字来源为诗经》或者《楚辞》：{name}的含义")

# 解析器
str_parser = StrOutputParser()

# 自定义函数
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# 大模型
llm = ChatOpenAI(api_key=api_key, base_url=base_url, model="deepseek-flash", temperature=0.5)

# 组链
# # 1.自定义函数组链
# chain = first_template | llm | my_func | second_template | llm | str_parser

# 2. 函数直接组链
chain = first_template | llm | (lambda ai_msg: {"name": ai_msg.content}) | second_template | llm | str_parser

# 调用链
for chunk in chain.stream({"lastName":"李", "gender":"女"}) :
    print(chunk, end="", flush=True)