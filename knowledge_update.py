from datetime import datetime
import os
from config import config
import hashlib 
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
# 检查文件是否以向量化
def check_md5(md5_str: str): 
    if not os.path.exists(config.md5_pass):
        open(config.md5_pass,"w", encoding='utf-8').close()
        return False
    else: 
        for line in open(config.md5_pass, "r", encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False

# 保存md5
def save_md5(md5_str: str):
    with open(config.md5_pass, "a", encoding='utf-8') as f:
        f.write(md5_str + '\n')

# 将传入的文件生成md5字符串
def get_string_md5(file_content: str, encoding='utf-8'):
    str_bytes = file_content.encode(encoding=encoding)
    md5_hex = hashlib.md5(str_bytes).hexdigest()
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self): 
        os.makedirs(config.persist_directory, exist_ok=True)
        # chroma数据库实例
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(
                model="text-embedding-v2",  # ✅ 阿里当前主力 embedding 模型（免费额度充足）
                dashscope_api_key="sk-64e6fed87d164550b35bf7d04bfbb97e",  # 在 https://dashscope.console.aliyun.com/ 获取
            ),
            persist_directory=config.persist_directory
        )
        # 字符串分割实例
        self.spliter = RecursiveCharacterTextSplitter(
            separators=["\n\n","\n"," ",".",",","\u200B",],
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    async def upload_str(self, content: str, filename: str): 
        md5_hex = get_string_md5(content)
        if check_md5(md5_hex): 
            # print(f"文件：{filename}已上传，请勿重复加载")
            return 
        
        if len(content) > 1000: 
            knowledge_chunks: list[str] = self.spliter.split_text(content)
        else: 
            knowledge_chunks = [content]

        metadata = {
            "source": filename,
            "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operate": "user"
        }
        await self.chroma.aadd_texts(knowledge_chunks, metadatas=[metadata for _ in knowledge_chunks])
        save_md5(md5_hex)
        print(f"成功上传文件：{filename}")


if __name__ == "__main__": 
    knowledge_service = KnowledgeBaseService()