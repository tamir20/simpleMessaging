from pydantic import BaseModel

class Chat_Message(BaseModel):
    msg: str
    sender: str

    def print_chat(self) -> None:
        print(f'from {self.sender}: {self.msg}')