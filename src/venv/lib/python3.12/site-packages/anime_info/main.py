import requests
import rich
import random
from rich import print,pretty
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from termcolor import cprint,colored
import sys
import subprocess
import time


subprocess.run(["clear"])

    
def anime_recommendation(anime_id):

        # recommendation of the day!

        response = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations")

        if response.status_code == 200:
            data = response.json()
            rec = data["data"][0]["entry"]["title"]
            cprint(f"Recommendation of the day is: {rec} {anime_id}","magenta",attrs=["bold"])
        else:
            print("No anime recommendation for today.")

try:
    anime_recommendation(random.randint(0,5000))
except Exception as e:
    print("No anime recommendation for today.")

def main():
    global anime_name,base_url,anime_info
    print()
    # search with anime name
    try:
        anime_name = input(str(colored("Search Anime: ","blue",attrs=["blink"])))
    except KeyboardInterrupt:
        print()
        cprint("Goodbye!","red")
        sys.exit(0)
    except Exception as e:
        print("idk",e)

    base_url = "https://api.jikan.moe/v4"
    anime_info = requests.get(f"{base_url}/anime?q={anime_name}")

    
class App(object):
    def __init__(self,title,desc,genres,figuren,anime_id,num_char,score,rank,Popularity,broadcast,base_url,status,episode):
        
        self.title = title
        self.desc = desc
        self.genres = genres
        self.figuren = ','.join(figuren)
        self.anime_id = anime_id
        self.num_chars = num_char
        self.base_url = base_url

        self.score = score
        self.rank = rank
        self.popularity = Popularity
        self.broadcast = broadcast
        self.episode = episode
        self.status = status
        
        self.show_anime_data()

    def show_anime_data(self):

        table = Table(title=f"{self.title} Table",box=box.ASCII,highlight=True,title_style="bold white",show_lines=False,show_footer=False,row_styles=["#98971a","#d79921"],collapse_padding=True,header_style="bold #d79921",)

        

        anime_data = {
                "Title": f"{self.title}",
                "Genre": f"{self.genres}",
                "Popularity": f"{self.popularity}",
                "Rank": f"{self.rank}",
                "Episodes": f"{self.episode}",
                "Broadcast": f"{self.broadcast}",
                "Status": f"{self.status}",
        }
        
            
        table.add_column("Title",justify="left",style="cyan",no_wrap=True)
        table.add_column("Genres",style="magenta")

        table.add_column("Score",style="#b16286")
        table.add_column("Rank",style="#8ec07c")
        table.add_column("Popularity",style="#fabd2f")
        table.add_column("Episodes",style="#b16286")
        table.add_column("Broadcast",style="#b16286")
        table.add_column("Status",style="#b16286")

        table.add_column("Characters",justify="left",style="cyan")
        
        table.add_row(f"{self.title}",f"{self.genres} ",f"{self.score}",f"{self.rank}",f"{self.popularity}",f"{self.episode}",f"{self.broadcast}",f"{self.status}",f"{self.figuren}")

        subprocess.run(["clear"])
        console = Console()
        console.print(table)
        
        console.log(anime_data,log_locals=False)



        cprint("Scroll up!","green",attrs=["bold","blink"])




        

def anime_log(anime_id,full_data) -> None:
    console = Console()
    tasks = [f"found {n} " for n in full_data]

    with console.status("[bold green] Working on gathering data ...") as status:
        while tasks:
            task = tasks.pop(0)
            time.sleep(0.3)
            console.log(f"{task}")
        

def check_status_code() -> None:

    while True:
        try:
            main()
            if anime_info.status_code == 200:
                search_data = anime_info.json()
                


                if search_data["data"]:
                    anime_id = search_data["data"][0]["mal_id"]
                    anime_title = search_data["data"][0]["title"]
                


                # anime details wie genre,title,beschreibung ...
                detail_response = requests.get(f"{base_url}/anime/{anime_id}")
                if detail_response.status_code == 200:
                    data = detail_response.json()

                    title = data["data"]["title"]
                    desc = data["data"]["synopsis"]
                    score = data["data"]["score"]
                    rank = data["data"]["rank"]
                    popularity = data["data"]["popularity"]
                    broadcast = data["data"]["broadcast"]["day"]
                    status = data["data"]["status"]
                    episodes = data["data"]["episodes"]
                    genres = ""+",".join([genre['name'] for genre in data['data']['genres']])





                # anime characters
                char_response = requests.get(f"{base_url}/anime/{anime_id}/characters")
                if char_response.status_code == 200:
                    char_data = char_response.json()

                    figuren = []
                    num_char = 0
                    for i,char in enumerate(char_data['data']):
                        if i < 30:
                            figuren.append(f"{char['character']['name']}")
                        num_char = i
                    
                    full_data = [
                            f"anime id: {anime_id}",
                            f"characters: {num_char}",
                            f"title: {title}",
                            f"genres: {genres}",
                            f"description",
                            f"rank: {rank}",
                            f"score: {score}",
                            f"broadcast: {broadcast}",
                            f"popularity: {popularity}",
                            f"status {status}",
                            f"episodes {episodes}",

                    ]
                    anime_log(anime_id,full_data)
                    App(title,desc,genres,figuren,anime_id,num_char,score,rank,popularity,broadcast,base_url,status,episodes)

            else:
                print("Error:",response.status_code)
        except Exception as e:
            print("No anime with this name or id found!",e)

check_status_code()

def cli_entry_point():
    check_status_code()


if __name__ == "__main__":
    cli_entry_point()
