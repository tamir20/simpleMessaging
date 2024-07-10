import json
from classes.heartbeat_message import Heartbeat_Message
from classes.chat_message import Chat_Message

def convert_json_to_user_set(online_users_json_str: str) -> set[Heartbeat_Message]:
    online_users = set[Heartbeat_Message]()
    online_users_json = json.loads(online_users_json_str)
    for user in online_users_json:
        online_users.add(Heartbeat_Message(name=user['name'], port=user['port']))
    return online_users

