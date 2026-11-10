from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Tongyi

prompt_template = PromptTemplate.from_template("我的邻居姓{lastName}, 刚生了一个{gender},帮她取一个名字")

# 通过format 注入模板参数
template_text = prompt_template.format(lastName="王", gender="儿子")

# # print(template_text)
# llm = Tongyi(model="qwen-max")
# respon = llm.invoke(template_text)
# print(respon)


# 通过链调用
llm = Tongyi(model="qwen-max")
chain = prompt_template | llm
res = chain.invoke(input={"lastName": "王", "gender": "女儿"})
print(res)