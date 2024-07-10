from operator import truediv
from classes.heartbeat_message import *
from classes.connection import *
import datetime
from logs.logging import log_to_event_viewer_decorator

@log_to_event_viewer_decorator
def handle_heartbeat(online_users: set[Connection] ,heartbeat: Heartbeat_Message) -> None:
   connection = Connection(heartbeat=heartbeat)
   if connection not in online_users:
      online_users.add(connection)
   else:
      for user in online_users:
         if user == connection:
            user.update_time()
   

def handle_validate_online_users(online_users: set[Connection]) -> None:
   for connection in online_users:
      if connection.timestamp < datetime.datetime.now() - datetime.timedelta(seconds=3):
        online_users.remove(connection)

def handle_list_online_users(online_users: set[Connection]) -> set[Heartbeat_Message]:
   heartbeat_set = set()
   # return set([message(name=connection.heartbeat.name, port=connection.heartbeat.port) for message in online_users]) another 1 liner option
   for connection in online_users:
      heartbeat_set.add(Heartbeat_Message(name=connection.heartbeat.name, port=connection.heartbeat.port))
   return heartbeat_set