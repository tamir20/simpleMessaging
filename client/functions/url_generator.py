from config.config import config_file

def get_chat_url_api(api: str, port:int) -> str:
    return config_file["client"]["protocol"] + config_file["client"]["ip"] + ":" + str(port) + config_file["client"]["api"][api]

def get_server_url_api(api: str) -> str:
    return config_file["server"]["protocol"] + config_file["server"]["ip"] + ":" + str(config_file["server"]["port"]) + config_file["server"]["api"][api]