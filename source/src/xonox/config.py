# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import json
from pathlib import Path
from os import path

class Config:
    def __init__(self, config_directory):
        self.__data = dict()
        if config_directory is None:
            config_directory = Path.home()
        self.__config_path = path.join(config_directory, 'xonox.conf')
        self.__load_data_from_file()

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __contains__(self, key):
        return self.__data.__contains__(key)

    def save(self):
        with open(self.__config_path, 'w+') as file:
            json.dump(self.__data, file, default=lambda o: o.__dict__, sort_keys=False, indent=2)

    def __load_data_from_file(self):
        try:
            with open(self.__config_path, 'r') as file:
                self.__data = json.load(file)
        except FileNotFoundError:
            pass