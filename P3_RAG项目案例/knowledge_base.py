"""
知识库
"""

import os
from datetime import datetime
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def check_md5(str_md5: str):
    """检查MD5是否已保存"""
    # 校验md5字符串
    if str_md5 is None:
        return False

    """检查传入的MD5字符串是否已经保存"""
    if not os.path.exists(config.MD5_PATH):
        # 文件不存在，创建文件，并把md5存入文件
        open(config.MD5_PATH, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.MD5_PATH, 'r', encoding="utf-8").readlines():
            line = line.strip()  # 去除头尾空格和换行
            if line == str_md5:
                return True
    return False


def save_md5(str_md5: str):
    """保存MD5值"""
    if str_md5 is None:
        pass
    """将传入的MD5字符串记录到文件中保存"""
    # a:apend 追加
    with open(config.MD5_PATH, 'a', encoding="utf-8") as f:
        f.write(str_md5 + "\n")


def get_str_md5(input_str: str, encoding='utf-8') -> str:
    """将传入的字符串转换为MD5"""
    str_bytes = input_str.encode(encoding=encoding)

    # 创建MD5对象
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)  # 传入需要转换的字符串字节组更新内容
    return md5_obj.hexdigest()  # 获取16进制的md5字符串


class KnowledgeBaseService(object):
    def __init__(self):
        #确保数据文件已存在
        os.makedirs(config.CHROMA_DB_PATH, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.CHROMA_COLLECTION_NAME, #数据库表表名
            embedding_function=DashScopeEmbeddings(model=config.EMBEDDING_MODEL),
            persist_directory=config.CHROMA_DB_PATH,    #数据库文件路径
        )      # 向量存储实例
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SPLIT_SIZE,     #分割后的文本最大长度
            chunk_overlap=config.CHUNK_OVERLAP,     #连续文本段之间重复字符数
            separators=config.CHUNK_SPLIT_SEPARATORS,   #自然段落划分的符号
            length_function=len                         #使用python自带的len函数统计长度
        )     # 文本分割器对象

    def upload_by_str(self, data:str, filename):
        """将传入的字符串进行向量化，并存入向量数据库中"""
        #先校验文本知识库是否已存在
        result={
            "isSuccess":False,
            "msg":"【失败】存入知识库四百"
        }

        md5 = get_str_md5(data)

        if check_md5(md5):
            result["msg"] = "【跳过】知识库已存在该内容"
            return result

        text_chunks = []
        if len(data) >= config.MAX_SPLIT_CHAR_NUMBER:
            text_chunks = self.spliter.split_text(data)
        else:
            text_chunks.append(data)

        #文档元数据
        metadata = {
                "source": filename,
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator":"你猜"
            }

        #存入向量库
        self.chroma.add_texts(
            text_chunks,
            metadatas=[metadata for _ in text_chunks]
        )

        #保存MD5
        save_md5(md5)
        result["msg"] = "【成功】内容以存入知识库"
        result["isSuccess"] = True
        return result


if __name__ == '__main__':
    md5 = "ccf6b6bde000ae39d305f27485f654ff"
    # str1 = get_str_md5("config.MD5_PATH")
    # str2 = get_str_md5("config.MD5_PATH")
    # str3 = get_str_md5("config.MD6_PATH")
    # print(str1)
    # print(str2)
    # print(str3)

    # print(check_md5(md5))

    # save_md5(md5)

    service = KnowledgeBaseService()
    print(service.upload_by_str(data="config.MD5_PATH", filename="test.txt"))