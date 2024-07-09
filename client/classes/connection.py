from datetime import datetime
from sqlite3 import Timestamp
from pydantic import BaseModel
from classes.heartbeat_message import *


class Connection(BaseModel):
    name: str
    port: int
    timestamp: datetime

    def __init__(self, name: str, port: int) -> None:
        super().__init__(name=name, port=port, timestamp=datetime.now())

    def __hash__(self) -> int:
        return self.port
    
    def __eq__(self, other: object) -> bool:
        return self.port == other.port
    
    def update_time(self) -> None:
        self.timestamp = datetime.now()


