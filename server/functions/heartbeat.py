from operator import truediv
from classes.heartbeat_message import *
from classes.connection import *
import datetime

def handle_heartbeat(online_users: set[Connection] ,heartbeat: Heartbeat_Message) -> None:
   connection = Connection(heartbeat=heartbeat)
   online_users.add(connection)

def handle_validate_online_users(online_users: set[Connection]) -> None:
   for connection in online_users:
      if connection.timestamp < datetime.datetime.now() - datetime.timedelta(seconds=3):
        online_users.remove(connection)

def handle_list_online_users(online_users: set[Connection]) -> set[Heartbeat_Message]:
   heartbeat_set = set()
   for connection in online_users:
      heartbeat_set.add(Heartbeat_Message(name=connection.heartbeat.name, port=connection.heartbeat.port))
   return heartbeat_set