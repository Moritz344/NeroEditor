import requests
import json
from mc_server_status.logging_handler import *

def get_server_info(base,server) -> str:
    response = requests.get(f"{base}/status/java/{server}")
    if response.status_code == 200:
        data = response.json()
        host = data["host"]
        players_on = data["players"]["online"]
        players_max: max = data["players"]["max"]
        version = data["version"]["name_clean"]

        player_list_on: list = []
        mods_list: list = []
        plugins_list: list = []

        status: bool = data["online"]
        motd = data["motd"]["clean"]

        mods = data["mods"]
        plugins = data["plugins"]

        port: int = data["port"]
        eula_blocked = data["eula_blocked"]

        max_number: int = 12

        
        # O.O
        if players_on < 100:
            for index in range(0,players_on):
                if index < max_number:
                    try:
                        name = data["players"]["list"][index]["name_clean"]
                        player_list_on.append(name)
                    except Exception:
                        player_list_on = []
                else:
                    continue

        for index in range(0,len(mods )):
            try:
                mod_name = data["mods"][index]["name"]
                mods_list.append(mod_name)
            except Exception as e:
                mods_list = []
                print("There was an error while loading the mods.",e)

        for index in range(0,len(plugins)):
            try:
                plugin_name = data["plugins"][index]["name"]
                plugins_list.append(plugin_name)
            except Exception as e:
                plugins_list = []
                print("There was an error while loading the plugins.",e)


        return players_on,players_max,player_list_on,status,version,motd,mods_list,port,eula_blocked,host,plugins_list

