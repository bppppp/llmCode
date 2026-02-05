from history_store import FileChatHistory
from save_vector import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from utils import test_chain

def print_prompt(prompt): 
    print(prompt.to_string())
    return prompt

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return FileChatHistory(
        session_id=session_id
    )

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService()
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你是一个资深前端工程师，你的技术栈是Vue3，擅长编写高质量、可维护的代码，语言简洁明了。\n参考资料为：{content}"),
            ("并且我提供用户的对话历史记录，如下："),
            MessagesPlaceholder(variable_name="chat_history"),  # 历史消息占位符
            ("user", "{input}")
        ])
        self.chat_model = ChatOpenAI(
            api_key="sk-bcd1a03d3f1a4a139e088e4f2c0edd50",
            base_url="https://api.deepseek.com/v1",
            model="deepseek-coder",
            temperature=0.3,
            max_tokens=2000,
            # streaming=True,
        )
        self.chain = self.__get_chain()

    def __get_chain(self): 
        retriever = self.vector_service.get_retriever()

        chain = (
            {
                "input": RunnablePassthrough(),
                "content": RunnableLambda(lambda value: value["input"]) | retriever | self.__format_documents
            } | RunnableLambda(self.__transform_prompt_template) | self.prompt_template | print_prompt| self.chat_model | StrOutputParser()
        )

        chain_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history,             # ← 必须传入 history 工厂函数
            input_messages_key="input",      # ← 用户输入字段名
            history_messages_key="chat_history",  # ← prompt 中 MessagesPlaceholder 的 variable_name
        )
        return chain_with_history

    def __transform_prompt_template(self, value):
        print(value)
        new_value = {
            "input": value["input"]["input"],
            "content": value["content"],
            "chat_history": value["input"]["chat_history"]
        }
        print(new_value)
        return new_value

    def __format_documents(self, docs: list[Document]): 
        if not docs: 
            return "无参考资料"
        formatted_str = ""
        for doc in docs: 
            formatted_str += f"文档内容：{doc.page_content}\n 文档元数据{doc.metadata}\n"
        return formatted_str
    
if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "022699",
        }
    }
    Rag = RagService().chain
    res = Rag.invoke({
        "input": "我的name是什么"
    }, config=session_config)
    print(res)