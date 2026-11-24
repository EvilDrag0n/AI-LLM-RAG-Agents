from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    def __init__(self, embedding):
        """
        :param embedding:   嵌入模型
        """
        self.embedding = embedding

        self.vector_db = Chroma(
            collection_name=config.CHROMA_COLLECTION_NAME,  # 数据库表表名
            embedding_function=self.embedding,
            persist_directory=config.CHROMA_DB_PATH,  # 数据库文件路径
        )  # 向量存储实例

    def get_retriever(self):
        return self.vector_db.as_retriever(search_kwargs={"k": config.max_result})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings

    retriever = VectorStoreService(DashScopeEmbeddings(model=config.EMBEDDING_MODEL)).get_retriever()
    result = retriever.invoke("身高170cm，体重70kg，穿什么衣服裤子")
    for i in result:
        print(i)