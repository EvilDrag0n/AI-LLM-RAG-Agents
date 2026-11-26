import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict

# def get_history(session_id) :
#     return FileMessageHistory(session_id, "./history")

#自定义文件消息历史
class FileMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, file_path):
        self.session_id = session_id
        self.file_path = file_path
        self.message_path = os.path.join(self.file_path, self.session_id)
        os.makedirs(os.path.dirname(self.message_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # 新消息追加历史消息
        all_messages = self.messages
        all_messages.extend(messages)

        dict_messages = messages_to_dict(all_messages)

        # 写入文件
        with open(self.message_path, 'w', encoding='utf-8') as f:
            json.dump(dict_messages, f, ensure_ascii=False, indent=2)

    #从文件中读取历史消息
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.message_path, 'r', encoding='utf-8') as f:
                dict_messages = json.load(f)
                return messages_from_dict(dict_messages)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.message_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
