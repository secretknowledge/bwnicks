import datetime
import logging
import os
from types import SimpleNamespace
import requests
import pickle
import json
from bedwars_api.exceptions import *


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
        self.created_date = datetime.datetime.now().timestamp()
        logging.debug(f"Class {self.__class__.__name__}: self.created_date = {self.created_date}")


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
        logging.debug(f"Class {self.__class__.__name__}: working directory: {os.getcwd()}")

        if os.path.isfile("cache.bin"):
            logging.debug(f"Class {self.__class__.__name__}: cache file found")
            with open("cache.bin", "rb") as f:
                self.data = pickle.loads(f.read())
                logging.debug(f"Class {self.__class__.__name__}: cache loaded")
        else:
            logging.debug(f"Class {self.__class__.__name__}: cache file not found")
            self.save()

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
            logging.debug(f"Class {self.__class__.__name__}: key = {key} has age of {datetime.datetime.now().timestamp() - value.timestamp} seconds")
            if datetime.datetime.now().timestamp() - value.created_date <= (60 * 60 * 24 * 7):  # 7 days
                if datetime.datetime.now().timestamp() - value.timestamp >= (60 * 30):  # 30 minutes
                    logging.debug(f"Class {self.__class__.__name__} found old data: refreshing {key}")
                    data = requests.get(
                        url="https://api.hypixel.net/player",
                        params={"key": self.api_key,
                                "name": key},
                    ).json()
                    logging.debug(f"Class {self.__class__.__name__}: Polled data for player {key}")

                    if data["player"] is None:  # Banned player
                        logging.debug(f"Class {self.__class__.__name__}: Player {key} is banned")
                        self.__delitem__(key)
                    else:
                        logging.debug(f"Class {self.__class__.__name__}: Player {key} is not banned")
                        logging.debug(f"Class {self.__class__.__name__}: Player data: {key} data updated")
                        self.__setitem__(key, Data(data))
                elif datetime.datetime.now().timestamp() - value.timestamp <= (60 * 30):
                    logging.debug(f"Class {self.__class__.__name__}: Player {key} is up to date")
                    continue
                else:
                    raise APIException
            elif datetime.datetime.now().timestamp() - value.timestamp >= (60 * 3):
                logging.debug(f"Class {self.__class__.__name__}: Player {key} is too old")
                self.__delitem__(key)
            else:
                raise APIException
