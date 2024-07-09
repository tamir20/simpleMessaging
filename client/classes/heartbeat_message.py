from pydantic import BaseModel

class Heartbeat_Message(BaseModel):
    name: str
    port: int

    def __hash__(self) -> int:
        return self.port
    
    def __eq__(self, other: object) -> bool:
        return self.port == other.heartbeat.port