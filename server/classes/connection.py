from datetime import datetime
from sqlite3 import Timestamp
from pydantic import BaseModel
from classes.heartbeat_message import Heartbeat_Message


class Connection(BaseModel):
    heartbeat: Heartbeat_Message
    timestamp: datetime =  datetime.now()

    def __hash__(self) -> int:
        return self.heartbeat.port
    
    def __eq__(self, other: object) -> bool:
        return self.heartbeat.port == other.heartbeat.port
    
    def update_time(self) -> None:
        self.timestamp = datetime.now()




