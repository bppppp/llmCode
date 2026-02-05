import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
# import time

# 创建大预言模型链接
llm = ChatOpenAI(
    api_key="sk-bcd1a03d3f1a4a139e088e4f2c0edd50",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-coder",
    temperature=0.3,
    max_tokens=2000,
    # streaming=True,
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深前端工程师，你的技术栈是Vue3，擅长编写高质量、可维护的代码，语言简洁明了。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 历史消息占位符
    ("user", "{input}")
])
prompt.invoke
# 模拟对话历史
chat_history = [
    HumanMessage(content="直接输出符合需求的代码即可，除非我在需求中明确要求了，非则不需要对代码进行解释，也不需要给出运行案例。"),
]

# 输出为字符串
stringRes = StrOutputParser()
transform2string = RunnableLambda(lambda ai_msg: ai_msg.content)

# 创建链
chain = prompt | llm | transform2string

# 运行链
start_time = time.time()  # 开始时间
result = chain.invoke({"input": "用js实现冒泡排序", "chat_history": chat_history,})
end_time = time.time()
elapsed = end_time - start_time  # 耗时
print(result, end="", flush=True)
print(f"\n耗时: {elapsed:.6f} 秒")