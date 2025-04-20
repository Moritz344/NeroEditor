import logging
import rich
from rich.logging import RichHandler
from rich.console import Console

console = Console()
# console.clear() 

FORMAT = ""

logging.basicConfig(
        level="NOTSET",format=FORMAT,datefmt="[%X]",handlers=[RichHandler()]
)



log = logging.getLogger("rich")
#log.info("running mcscan ... ")


