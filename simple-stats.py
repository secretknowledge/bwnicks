from dotenv import load_dotenv
from bedwars_api import HypixelAPI
import os


load_dotenv()


api = HypixelAPI(os.environ.get("API_KEY"))

while True:
    prompt = input("Is (n)ick, (f)kdr, or (q)uit: ")

    if prompt == "n":
        print(api.nick(input("Player IGN: ")))
    elif prompt == "f":
        print(api.fkdr(input("Player IGN: ")))
    elif prompt == "q":
        break
    else:
        print("Invalid input.")