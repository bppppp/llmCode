from langchain_chroma import Chroma
from config import config
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreService(object):
    def __init__(self): 
        self.embedding = DashScopeEmbeddings(
            model="text-embedding-v2",  # ✅ 阿里当前主力 embedding 模型（免费额度充足）
            dashscope_api_key="sk-64e6fed87d164550b35bf7d04bfbb97e",  # 在 https://dashscope.console.aliyun.com/ 获取
        )
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory)
        
    def get_retriever(self): 
        # 返回向量存储器
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})
    
if __name__ == "__main__":
    retriever = VectorStoreService().get_retriever()
    res = retriever.invoke("我的name是什么")
    print(res)