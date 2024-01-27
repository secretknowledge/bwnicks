from bedwars_api import HypixelAPI
from bedwars_api import LogParser
import logging
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(filename="stats.log", level=logging.DEBUG, filemode="w")
logging.debug(f"\n\nbwnicks complex_stats.py starting at {datetime.datetime.now()}\n\n")

log = LogParser()
api = HypixelAPI(os.environ.get("HYPIXEL_API_KEY"))

log.scan()

if len(log.people) != 0:
    for player in log.people:
        print(f"Player: {player}")
        print(f"FKDR: {api.fkdr(player)}")
        print(f"Level: {api.level(player)}")
        print(f"Nick: {api.nick(player)}")
        print()
else:
    print("No players found.")
