import uvicorn
from fastapi import FastAPI
import yaml
from functions.heartbeat import *
from classes.heartbeat_message import *
from fastapi_utils.tasks import repeat_every
from classes.heartbeat_message import Heartbeat_Message
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from config.config import config_file

# Global variable that mantain client's connections
online_users = set[Connection]() 
app = FastAPI()


# heartbeat api
@app.post(config_file["server"]["api"]["heartbeat"], status_code = HTTP_204_NO_CONTENT)
async def heartbeat(heartbeat: Heartbeat_Message) -> None:
    handle_heartbeat(online_users, heartbeat)

# list online users api
@app.get(config_file["server"]["api"]["list"], status_code = HTTP_200_OK)
async def list_online_users() -> set[Heartbeat_Message]:
    return handle_list_online_users(online_users)

# delete old online records every 3 seconds
@app.on_event('startup')
@repeat_every(seconds=3)
async def validate_online_users():
    handle_validate_online_users(online_users)

if __name__ == "__main__":
    uvicorn.run(app, host=config_file["server"]["ip"], port=config_file["server"]["port"])  # Specify the desired port here