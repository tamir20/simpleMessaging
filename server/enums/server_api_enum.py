from enum import Enum

class Server_API_Enum(str, Enum):
    LIST = 'list'
    HEARTBEAT = 'heartbeat'