# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import json
from pathlib import Path
from os import path
from xonox.station import Station

class StationRepository:
    def __init__(self):
        self.__data = []
        self.__configPath = path.join(Path.home(), 'xonox.conf')
        self.__load_data_from_file()

    def add(self, station):
        station.id = len(self.__data)
        self.__data.append(station)
        self.__write_data_to_file()

    def get(self, id):
        return self.__data[id]

    def get_all(self):
        return self.__data.copy()

    def remove(self, id):
        self.__data.pop(id)
        self.__write_data_to_file()

    def __load_data_from_file(self):
        try:
            with open(self.__configPath, 'r') as file:
                config = json.load(file)
                if ('stations' in config):
                    stations = config['stations']
                    for station in stations:
                        self.add(Station(station['name'], station['description'], station['stream']))
        except FileNotFoundError:
            pass

    def __write_data_to_file(self):
        if len(self.__data) > 0:
            config = { 'stations': self.__data }
            with open(self.__configPath, 'w+') as file:
                json.dump(config, file, default=lambda o: o.__dict__, sort_keys=False, indent=2)
