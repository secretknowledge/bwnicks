from bedwars_api.exceptions import *
from bedwars_api.data import *
from bedwars_api.parsing import *


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
            logging.debug(f"Class {self.__class__.__name__}: Received response from API for player {player_name}")

            if data["success"] is False:
                logging.debug(f"Class {self.__class__.__name__}: API request for player {player_name} failed")
                if data["cause"] == "You have already looked up this name recently" or data["cause"] == "Key throttle":
                    raise TooManyRequestsException
                else:
                    raise InvalidRequestException

            elif data["player"] is None:
                logging.debug(f"Class {self.__class__.__name__} for player {player_name}: no data available")
                raise PlayerNotFoundException
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

        except PlayerNotFoundException:
            logging.debug(f"Class {self.__class__.__name__}: player {player_name} not in cache")
            return True

    def fkdr(self, player_name):
        logging.debug(f"Class {self.__class__.__name__}: fkdr() called")
        player_data = self.player(player_name)
        logging.debug(f"Class {self.__class__.__name__}: player_data for player {player_name} is found")
        try:
            fkdr = int(player_data.tree.player.stats.Bedwars.final_kills_bedwars) / int(
                player_data.tree.player.stats.Bedwars.final_deaths_bedwars)
        except ZeroDivisionError:
            logging.debug(f"Class {self.__class__.__name__}: fkdr: division by zero for player {player_name}")
            fkdr = 0
        except AttributeError:
            logging.debug(f"Class {self.__class__.__name__}: fkdr: attribute error for player {player_name}")
            fkdr = 0

        logging.debug(f"Class {self.__class__.__name__}: fkdr for player {player_name} = {fkdr}")

        return round(fkdr, 2)

# graciecooper2018
