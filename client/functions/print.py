import requests
from functions.json_parser import convert_json_to_user_set
from labels.labels import GENERAL_HELP, USER_LIST_DIVIDER, USER_LIST_TITLE, WELCOME_MESSAGE


def print_user_list() -> None:
    response = requests.get('http://127.0.0.1:12000/list')
    user_set = convert_json_to_user_set(response.text)

    print(USER_LIST_TITLE)
    print(USER_LIST_DIVIDER)

    for user in user_set:
        print(f"{user.name:10} {user.port}")

def print_welcome_messsage(name: str) -> None:
    print(WELCOME_MESSAGE + name)
    print(GENERAL_HELP)