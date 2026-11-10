from openai import OpenAI

client = OpenAI(
    base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# response = client.chat.completions.create(
#     model="qwen3.7-flash",
#     messages=[
#         {"role": "system", "content": "你是一个个人生活助理，不说废话，简单回答"},
#         {"role": "assistant", "content": "我是一个生活助理，能帮人处理各种生活问题"},
#         {"role": "user", "content": "青椒炒蛋应该怎么做"}
#     ],
#     stream=True
# )

response = client.chat.completions.create(
    model="qwen3.7-flash",
    messages=[{"role": "system", "content": "你是一个AI助手，简洁回答问题"},
              {"role": "user", "content": "我现在有10块钱"},
              {"role": "assistant", "content": "好的"},
              {"role": "user", "content": "买1颗需要3块钱"},
              {"role": "assistant", "content": "好"},
              {"role": "user",
               "content": "朋友又给了我2块，我一共可以买几颗糖"},
              ],
    stream=True
)

for chunk in response:
    if not chunk.choices:
        print("")
        print(chunk.usage)
        continue
    delta = chunk.choices[0].delta
    if delta.content is not None:
        print(delta.content, end="", flush=True)
