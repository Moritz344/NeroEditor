import requests
import rich
from mc_server_status.handling_requests import *
from mc_server_status.format_data import get_data
from mc_server_status.logging_handler import *
from termcolor import colored
import sys

# LAST CHANGE: ascii art und json format

run = True


class Main(object):
    def __init__(self):
        self.base_url = "https://api.mcstatus.io/v2"
        

    def update(self):
        try:
            server_name: input = input(str(colored("Server: ","blue",attrs=["blink"])))
            players_on,players_max,players_list_on,status,version,motd,mods_list, port,eula_blocked,host,plugins_list = get_server_info(self.base_url,server_name)
            get_data(players_on,players_max,players_list_on,status,version,motd,mods_list, port,eula_blocked,host,plugins_list)
        except Exception as e:
            print("DEBUG:",e)
            log.error("[bold red blink]No results![/]",extra={"markup": True})
        except KeyboardInterrupt:
            log.info("[bold green blink]Goodbye![/]",extra={"markup": True})
            sys.exit(0)


def cli_entry_point():
    app = Main()
    while run:
        app.update()
if __name__ == "__main__":
    cli_entry_point()

