# AI 大模型、RAG 与智能体开发

本项目记录使用 Python 学习大模型应用开发的示例，目前涵盖 OpenAI 兼容接口和 LangChain 的基础用法。代码按主题和编号组织，适合逐个运行和阅读；目前仓库主要包含基础示例，尚未实现完整的 RAG 或智能体应用。

## 项目内容

| 目录 | 内容 |
| --- | --- |
| `P1_OpenAi基础库的使用/` | API 密钥、聊天接口、流式输出和手动传入对话历史。 |
| `P2_LangChainRag开发/` | 余弦相似度、通义模型与嵌入、消息、提示词模板、链、输出解析器、自定义函数、内存会话历史和自定义文件会话历史。 |

## 运行示例

安装 Python，并根据要运行的脚本安装所需依赖。示例使用的包包括 `openai`、`numpy`、`python-dotenv`、`langchain-core`、`langchain-community`、`langchain-openai`、`langchain-qwq` 和 `dashscope`；项目目前没有锁定依赖版本，不同版本的接口可能存在差异。

部分示例需要阿里云或 DeepSeek 的 API 密钥和可用的模型服务。请按照所运行脚本及对应 SDK 的要求配置环境变量；DeepSeek 示例通过项目根目录的 `.env` 读取 `DEEPSEEK_API_KEY`：

```dotenv
DEEPSEEK_API_KEY=替换为自己的密钥
```

`.env` 已加入 `.gitignore`，不要提交真实密钥。部分示例中的服务地址和模型名称需要根据自己的服务配置调整，调用远程模型可能产生费用。

在项目根目录选择一个脚本运行，例如：

```powershell
python "P2_LangChainRag开发/01余弦相似度.py"
```

各示例相互独立，请根据文件编号及内容选择学习顺序。

`P2_LangChainRag开发/14自定义File长期会话记忆.py` 演示自定义文件会话历史，将消息以 UTF-8 JSON 保存到当前工作目录下的 `history/<session_id>` 文件，中文直接显示。目录会自动创建；当前实现每次写入会覆盖为本轮消息，完整历史的追加逻辑仍待完善。示例当前仅启用询问宠物总数的调用，可自行取消前两轮调用的注释以写入示例信息。
