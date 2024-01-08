# API Key = 3ae7e469-f78e-474e-9d0c-1ee6c4378127
import requests
import json
import pickle
import datetime
from types import SimpleNamespace
import logging

logging.basicConfig(filename="stats.log", level=logging.DEBUG)


class LogParser:
    def __init__(self, log_file="~/.minecraft/logs/blclient/minecraft/latest.log"):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        self.log_file = log_file
        logging.debug(f"Class {self.__class__.__name__}: self.log_file = {self.log_file}")
        self.people = []

    def parse(self):
        logging.debug(f"Class {self.__class__.__name__}: parse() called")

        with open(self.log_file, "r") as f:
            for line in f:
                keyword = "[Client thread/INFO]: [CHAT] ONLINE: "
                if keyword in line:
                    logging.debug(f"Found line in {self.log_file}: {line}")
                    data = line.split(keyword)[1]
                    people = data.split(", ")
                    logging.debug(f"Class {self.__class__.__name__}: people = {people}")

                    for person in people:
                        self.people.append(person)


class Data:
    def __init__(self, dictionary):
        """
        :param dictionary:
        :type dictionary: dict
        Get a dictionary containing data, convert it to json, load it into a data tree.
        """
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        self.tree = json.loads(json.dumps(dictionary), object_hook=lambda d: SimpleNamespace(**d))
        logging.debug(f"Class {self.__class__.__name__}: self.tree initialized")
        self.timestamp = datetime.datetime.now().timestamp()
        logging.debug(f"Class {self.__class__.__name__}: self.timestamp = {self.timestamp}")


class Cache:
    def __init__(self, filename, api_key):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        self.data = {}
        self.filename = filename
        self.api_key = api_key
        logging.debug(f"Class {self.__class__.__name__}: Init finished")
        self.load()
        self.refresh(reload=False)  # No extra file loading
        logging.debug(f"Class {self.__class__.__name__}: Refresh finished")

    def __getitem__(self, key):
        logging.debug(f"Class {self.__class__.__name__}: __getitem__ called with key {key}")
        return self.data[key]

    def __setitem__(self, key, value):
        logging.debug(f"Class {self.__class__.__name__}: __setitem__ called with key {key}")
        self.data[key] = value
        self.save()

    def __delitem__(self, key):
        logging.debug(f"Class {self.__class__.__name__}: __delitem__ called with key {key}")
        del self.data[key]
        self.save()

    def __contains__(self, key):
        logging.debug(f"Class {self.__class__.__name__}: __contains__ called with key {key}")
        return key in self.data

    def __len__(self):
        logging.debug(f"Class {self.__class__.__name__}: __len__ called")
        return len(self.data)

    def __iter__(self):
        logging.debug(f"Class {self.__class__.__name__}: __iter__ called")
        return iter(self.data)

    def save(self):
        logging.debug(f"Class {self.__class__.__name__}: save() called")
        with open("cache.bin", "wb") as f:
            f.write(pickle.dumps(self.data))
            logging.debug(f"Class {self.__class__.__name__}: cache saved")

    def load(self):
        logging.debug(f"Class {self.__class__.__name__}: load() called")
        with open("cache.bin", "rb") as f:
            self.data = pickle.loads(f.read())
            logging.debug(f"Class {self.__class__.__name__}: cache loaded")

    def clear(self):
        logging.debug(f"Class {self.__class__.__name__}: clear() called")
        self.data = {}
        self.save()
        logging.debug(f"Class {self.__class__.__name__}: clear finished")

    def reload(self):
        logging.debug(f"Class {self.__class__.__name__}: reload() called")
        self.save()
        self.load()
        logging.debug(f"Class {self.__class__.__name__}: reload finished")

    def refresh(self, reload=True):
        logging.debug(f"Class {self.__class__.__name__}: refresh() called")
        if reload:
            logging.debug(f"Class {self.__class__.__name__}: refreshing cache")
            self.reload()

        for key, value in self.data.items():
            if value.timestamp - datetime.datetime.now().timestamp() >= 1800:
                logging.debug(f"Class {self.__class__.__name__} found old data: refreshing {key}")
                data = requests.get(
                    url="https://api.hypixel.net/player",
                    params={"key": self.api_key,
                            "name": key},
                ).json()

                if data["player"] is None:  # Banned player
                    logging.debug(f"Class {self.__class__.__name__}: Player {key} is banned")
                    self.__delitem__(key)
                else:
                    logging.debug(f"Class {self.__class__.__name__}: Player {key} is not banned")
                    logging.debug(f"Class {self.__class__.__name__}: Player data: {key} data updated")
                    self.__setitem__(key, Data(data))
            else:
                logging.debug(f"Class {self.__class__.__name__}: Player {key} is up to date")
                continue


class HypixelException(Exception):
    def __init__(self, message):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        super().__init__(message)
        logging.debug(f"HypixelException raised: {message}")


class HypixelAPI:
    def __init__(self, api_key):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        self.api_key = api_key
        logging.debug(f"Class {self.__class__.__name__}: self.api_key = {self.api_key}")
        self.cache = Cache("cache.log", self.api_key)
        logging.debug(f"Class {self.__class__.__name__}: self.cache initialized")
        self.cache.load()
        logging.debug(f"Class {self.__class__.__name__}: self.cache loaded")

    def player(self, player_name):
        logging.debug(f"Class {self.__class__.__name__}: player() called")
        if player_name not in self.cache.__dict__["data"].keys():
            data = requests.get(
                url="https://api.hypixel.net/player",
                params={"key": self.api_key,
                        "name": player_name},
            ).json()

            if data["player"] is None:
                logging.debug(f"Class {self.__class__.__name__} for player {player_name}: no data available")
                raise HypixelException("Player is not available via Hypixel API.")
            else:
                logging.debug(f"Class {self.__class__.__name__} for player {player_name}: data available")
                self.cache.__setitem__(player_name, Data(data))
                logging.debug(f"Class {self.__class__.__name__} for player {player_name}: data added to cache")

        return self.cache.__getitem__(player_name)

    def nick(self, player_name):
        logging.debug(f"Class {self.__class__.__name__}: nick() called")
        try:
            self.player(player_name)
            logging.debug(f"Class {self.__class__.__name__}: found player {player_name} in cache")
            return False

        except HypixelException:
            logging.debug(f"Class {self.__class__.__name__}: player {player_name} not in cache")
            return True

    def fkdr(self, player_name):
        logging.debug(f"Class {self.__class__.__name__}: fkdr() called")
        player_data = self.player(player_name)
        logging.debug(f"Class {self.__class__.__name__}: player_data for player {player_name} is found")
        fkdr = int(player_data.tree.player.stats.Bedwars.final_kills_bedwars) / int(
            player_data.tree.player.stats.Bedwars.final_deaths_bedwars)
        logging.debug(f"Class {self.__class__.__name__}: fkdr for player {player_name} = {fkdr}")

        return round(fkdr, 2)


"""
TODO:

- Add error message when API is rate limited / disabled / out of requests.
- Optimise caching format for performance and so it doesn't take up too much space.
- Create custom class alike to SimpleNamespace that is more memory efficient and more optimised toward our data.
- Other random optimisation.
- Add more custom error handling.
- Reorganise code and split into separate files.
- Fix latest.log parsing to not be a memory leak.
- Make thread safe.
- Make asynchronous.
- User Interface
    - Add a option for refreshing player data every 30 minutes seconds or leaving it to be removed after a week.
    - Periodically refresh player data
    - Periodically scan latest.log file for new data
    - Add options to clear logs, disable logs, remove old log data, and change loging level.
    - Add option to clear cache and disable cache.
    - Loading animations
"""
