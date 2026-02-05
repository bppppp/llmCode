import asyncio
import json
import os
from knowledge_update import KnowledgeBaseService

folder_path = "./base_files"  # 文件夹路径
knowledgeBase = KnowledgeBaseService()
async def read_files():
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):  # 检查是否为JSON文件
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()  # 直接读取为字符串
                    await knowledgeBase.upload_str(content=content, filename=filename)
            except Exception as e:
                print(f"读取{filename}时出错: {e}")

if(__name__ == "__main__"):
    asyncio.run(read_files())