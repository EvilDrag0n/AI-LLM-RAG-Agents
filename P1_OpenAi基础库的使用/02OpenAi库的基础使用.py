from openai import OpenAI
# 1.获取client对象
client = OpenAI(base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 2. 调用模型

repsonse = client.chat.completions.create(model="qwen3.7-flash",
                                        messages=[{"role": "system", "content": "你是一个个人生活助理，不说废话，简单回答"},
                                                  {"role": "assistant",
                                                   "content": "我是一个生活助理，能帮人处理各种生活问题"},
                                                  {"role": "user", "content": "青椒炒蛋应该怎么做"}])

# 3. 处理结果
print(repsonse.choices[0].message.content)