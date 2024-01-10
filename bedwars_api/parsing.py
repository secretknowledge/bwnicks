import logging


class LogParser:
    def __init__(self, log_file="~/.minecraft/logs/blclient/minecraft/latest.log"):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        self.log_file = log_file
        logging.debug(f"Class {self.__class__.__name__}: self.log_file = {self.log_file}")
        self.people = []

    def parse(self, line):
        logging.debug(f"Class {self.__class__.__name__}: parse() called")

        keyword = "[Client thread/INFO]: [CHAT] ONLINE: "
        if keyword in line:
            logging.debug(f"Found line in {self.log_file}: {line}")
            data = line.split(keyword)[1]
            people = data.split(", ")
            logging.debug(f"Class {self.__class__.__name__}: people = {people}")

            for person in people:
                self.people.append(person)

    def scan(self):
        with open(self.log_file, "r") as f:
            for line in f.read():
                self.parse(line)
