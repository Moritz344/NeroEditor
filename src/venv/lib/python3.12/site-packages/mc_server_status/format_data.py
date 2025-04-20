import rich
from rich.panel import Panel
from rich.console import Console
from termcolor import cprint,colored
from rich.box import *
from rich.markdown import Markdown
from mc_server_status.logging_handler import *
from mc_server_status.ascii_art import *
from rich.prompt import Prompt
import questionary
import json

# TODO: ascii art

print(ascii_1)
cprint("[+] Fetch data from your favourite minecraft server. 🧙‍♂️","yellow")
print()


def get_data(players_on,players_max,players_list_on,status,version,motd,mods_list,port,eula_blocked,host,plugins_list):
    console = Console()

    players_list_on = ",".join(players_list_on)
    
    status_color = "[bold green]"
    mods_color = "[white]"
    plugins_color = "[white]"
    eula_color = "[white]"
    

    if status:
        status = "Online"
        status_color = "[bold green]"
    else:
        status = "Offline"
        status_color = "[bold red]"

    if mods_list :
        mods_color = "[green]"
    else:
        mods_color = "[#3c3836]"

    if plugins_list:
        plugins_color = "[green]"
    else:
        plugins_color = "[#3c3836]"

    if eula_blocked:
        eula_color = "[green]"
    else:
        eula_color = "[red]"

    motd = motd.split()
    motd = "  ".join(motd)
    

    mods_list= ",".join(mods_list)

    plugins_list = ",".join(plugins_list)

    if mods_list == "":
        mods_list = "N/A"
    if not eula_blocked:
        eula_blocked = "No"
    else:
        eula_blocked = "Yes"

    if plugins_list == "":
        plugins_list = "N/A"

    json_format = {"Status": f"{status}","Host": f"{host}","Port": f"{port}","MOTD": f"{motd}","Version": f"{version}","Players": f"{players_on/players_max}","Mods": f"{mods_list}","Plugins": f"{plugins_list}","EULA Blocked": f"{eula_blocked}","Player list": f"{players_list_on }"}

    answers = questionary.form(
            select = questionary.select("How would you like to display the data?",choices=["Markdown 🧙‍♂️","Panel 📦","JSON 🧙‍♂️"],)

    ).ask()

    selected_item = answers["select"]
    if selected_item == "Markdown 🧙‍♂️":
        MARKDOWN = f"""
        # MARKDOWN FORMAT

        Status:        {status}
        Host:          {host}
        Port:          {port}
        MOTD:          {motd}
        Version:       {version}
        Players:       {players_on}/{players_max}

        Mods:          {mods_list}
        Plugins:       {plugins_list}
        EULA Blcocked: {eula_blocked}
        Player List:   {players_list_on}

        
        """
        console.clear()
        md = Markdown(MARKDOWN)
        console.print(md)
    elif selected_item == "JSON 🧙‍♂️":
        console.clear()
        print(json.dumps(json_format,sort_keys=False,indent=4))
    elif selected_item == "Panel 📦":
        panel = Panel(
                f"[bold yellow]Status:           [/]{status_color}{status}[/]"
                "\n"
                f"[bold yellow]Host:             [/][#458588]{host}[/]"
                "\n"
                f"[bold yellow]Port:             [/][#d65d0e]{port}[/]"
                "\n"
                f"[bold yellow]MOTD:             [/][#ebdbb2]{motd}[/]"
                "\n"
                f"[bold yellow]Version:          [/][#689d6a]{version}[/]"
                "\n"
                f"[bold yellow]Players:          [/][#a89984]{players_on}/{players_max}[/]"
                "\n"
                f"[bold yellow]Mods:             [/]{mods_color}{mods_list}[/]"
                "\n"
                f"[bold yellow]Plugins:          [/]{plugins_color}{plugins_list}[/]"
                "\n"
                f"[bold yellow]EULA Blocked:     [/]{eula_color}{eula_blocked}[/]"
                "\n"
                f"[bold yellow]Player list:      [/]{players_list_on}",

                title="Panel",
                title_align="right",
                border_style="white",
        )


        console.clear()
        console.print(panel)

