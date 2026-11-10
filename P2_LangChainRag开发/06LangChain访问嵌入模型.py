from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings()

# print(embeddings.embed_query("你是谁"))
print(embeddings.embed_documents(["你是谁啊", "你猜", "我是小美"]))