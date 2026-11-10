from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms import Tongyi

#示例模板
example_template = PromptTemplate.from_template("单词：{word}, 反义词：{antonym}")

# 示例的动态注入数据
examples_data=[
    {"word":"大", "antonym":"小"},
    {"word":"高", "antonym":"矮"},
    {"word":"胖", "antonym":"瘦"}
]

few_shot_prompt_template = FewShotPromptTemplate(
    example_prompt=example_template,  # 示例提示词模板
    examples=examples_data,  # 示例需要注入的变量数据
    prefix="示例如下：",  # 示例前的提示词模板前缀
    suffix="根据示例，输出{input_word}的反义词",  # 示例后的提示词模板后缀
    input_variables=["input_word"]  # 前缀或后缀需要注入的变量名
)

# 填充示例模板
prompt_text = few_shot_prompt_template.invoke(input={"input_word": "短"}).to_string()
print(prompt_text)
print("---------------------")

llm = Tongyi(models="qwen-max")
res = llm.invoke(prompt_text)
print(res)