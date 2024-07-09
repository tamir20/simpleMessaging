import uvicorn
from fastapi import FastAPI
from functions.heartbeat import *
from classes.heartbeat_message import *
from fastapi_utils.tasks import repeat_every
from classes.heartbeat_message import Heartbeat_Message
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

# Global variable that mantain client's connections
online_users = set[Connection]() 
app = FastAPI()


@app.post("/heartbeat", status_code = HTTP_204_NO_CONTENT)
async def heartbeat(heartbeat: Heartbeat_Message) -> None:
    handle_heartbeat(online_users, heartbeat)

@app.get("/list", status_code = HTTP_200_OK)
async def list_online_users() -> set[Heartbeat_Message]:
    return handle_list_online_users(online_users)

@app.on_event('startup')
@repeat_every(seconds=3)  # Adjust the interval as needed
async def validate_online_users():
    handle_validate_online_users(online_users)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=12000)  # Specify the desired port here