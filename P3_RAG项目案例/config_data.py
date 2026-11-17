MD5_PATH = "./file_md5.txt"  # MD5文件路径

#chroma
CHROMA_COLLECTION_NAME = "test_rag"  # 数据库表名
EMBEDDING_MODEL = "text-embedding-v4"  # embedding模型
CHROMA_DB_PATH = "./chroma_db"  # 数据库文件

#spliter
CHUNK_SPLIT_SIZE=300
CHUNK_OVERLAP=50
CHUNK_SPLIT_SEPARATORS=[".", "!", "?", "\n\n", "\n", "。", "？", "！", "", " "]
MAX_SPLIT_CHAR_NUMBER = 1000  #超过这个长度才分割