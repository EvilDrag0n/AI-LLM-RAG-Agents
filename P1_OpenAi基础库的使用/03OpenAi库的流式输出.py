from openai import OpenAI

# 1.获取client对象
client = OpenAI(
    base_url="https://llm-11gkvboh901iojl2.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 2. 调用模型

response = client.chat.completions.create(
    model="qwen3.7-flash",
    messages=[
        {"role": "system", "content": "你是一个个人生活助理，不说废话，简单回答"},
        {"role": "assistant", "content": "我是一个生活助理，能帮人处理各种生活问题"},
        {"role": "user", "content": "青椒炒蛋应该怎么做"}
    ],
    stream=True
)

# 3. 处理结果
for chunk in response:
    # 如果 choices 为空，跳过该数据块（通常是末尾的用量统计块）
    if not chunk.choices:
        # 可选：在这里可以读取 chunk.usage 来获取本次请求的 Token 消耗
        print("")
        print("+++++++++++++ 本次token用量 ++++++++++++++")
        print(chunk.usage)
        continue
    delta = chunk.choices[0].delta
    if delta.content is not None:
        print(delta.content, end="", flush=True)
