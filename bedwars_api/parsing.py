import logging
from file_read_backwards import FileReadBackwards


class LogParser:
    def __init__(self, log_file="/home/jonah/.minecraft/logs/blclient/minecraft/latest.log"):
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
                logging.debug(f"Class {self.__class__.__name__}: Found player with IGN {person}")
                self.people.append(person)

    def scan(self):
        with FileReadBackwards(self.log_file, encoding="utf-8") as f:
            for line in f:
                self.parse(line)


if __name__ == "__main__":
    parser = LogParser()
    parser.scan()
    print(f"Found {len(parser.people)} people: {parser.people}")
