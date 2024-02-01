from dotenv import load_dotenv
from bedwars_api import HypixelAPI
import os
import logging
import datetime
import json


load_dotenv()


logging.basicConfig(filename="stats.log", level=logging.DEBUG, filemode="w")
logging.debug(f"\n\nbwnicks simple_stats.py starting at {datetime.datetime.now()}\n\n")

api = HypixelAPI(os.environ.get("HYPIXEL_API_KEY"))

logging.debug(f"Class {api.__class__.__name__}: api initialized with api_key {api.api_key}")


while True:
    prompt = input("Is (n)ick, (f)kdr, or (q)uit: ")

    if prompt == "n":
        print(api.nick(input("Player IGN: ")))
    elif prompt == "f":
        print(api.fkdr(input("Player IGN: ")))
    elif prompt == "q":
        break
    elif prompt == "d":
        print(json.dumps(api.data(input("Player IGN: ")), indent=2))
    else:
        print("Invalid input.")
