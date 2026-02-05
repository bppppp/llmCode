import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.messages import messages_from_dict, message_to_dict
from langchain_core.messages import AIMessage, HumanMessage

class FileChatHistory(BaseChatMessageHistory): 
    def __init__(self, session_id):
        self.session_id = session_id
        self.storage_path = "./history_chat"
        print(self.storage_path, self.session_id)
        self.file_path = os.path.join(self.storage_path, self.session_id)
        print(self.file_path)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)


    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  # Existing messages
        all_messages.extend(messages)  # Add new messages

        serialized = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)
    
    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(
                os.path.join(self.storage_path, self.session_id),
                "r",
                encoding="utf-8",
            ) as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []


if __name__ == "__main__": 
    file_chat_history = FileChatHistory("022699.json")
    file_chat_history.add_messages(messages=[HumanMessage(content="直接输出符合需求的代码即可，除非我在需求中明确要求了，非则不需要对代码进行解释，也不需要给出运行案例。")])
