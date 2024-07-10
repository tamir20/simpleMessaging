import requests
from enums.server_api_enum import Server_API_Enum
from functions.json_parser import convert_json_to_user_set
from functions.url_generator import get_server_url_api
from labels.labels import GENERAL_HELP, USER_LIST_DIVIDER, USER_LIST_TITLE, WELCOME_MESSAGE


def print_user_list() -> None:
    response = requests.get(get_server_url_api(Server_API_Enum.LIST))
    user_set = convert_json_to_user_set(response.text)

    print(USER_LIST_TITLE)
    print(USER_LIST_DIVIDER)

    for user in user_set:
        print(f"{user.name:10} {user.port}")

def print_welcome_messsage(name: str) -> None:
    print(WELCOME_MESSAGE + name)
    print(GENERAL_HELP)