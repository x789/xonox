# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import json
from pathlib import Path
from os import path
from . import Station

class StationRepository:
    def __init__(self, configDirectory):
        self.__data = []
        self.__next_station_id = 0
        if configDirectory is None:
            configDirectory = Path.home()
        self.__configPath = path.join(configDirectory, 'xonox.conf')
        self.__load_data_from_file()

    def add(self, station):
        self.__update_next_station_id(station)
        self.__ensure_station_id_set(station)
        self.__data.append(station)
        self.__write_data_to_file()

    def get(self, id):
        for x in self.__data:
            if x.id == id:
                return x
        raise KeyError()

    def get_all(self):
        return self.__data.copy()

    def remove(self, id):
        for x in self.__data:
            if x.id == id:
                self.__data.remove(x)
                self.__write_data_to_file()
                return
        raise KeyError()

    def __ensure_station_id_set(self, station):
        if station.id is None:
            station.id = self.__next_station_id
            self.__next_station_id = self.__next_station_id + 1

    def __update_next_station_id(self, station):
        if station.id is not None and station.id >= self.__next_station_id:
            self.__next_station_id = station.id + 1

    def __load_data_from_file(self):
        try:
            with open(self.__configPath, 'r') as file:
                config = json.load(file)
                self.__read_stations_from_config(config)
                self.__read_next_station_id_from_config(config)
        except FileNotFoundError:
            pass

    def __read_stations_from_config(self, config):
        if 'stations' in config:
            stations = config['stations']
            for station in stations:
                self.add(Station(station['name'], station['description'], station['stream']))

    def __read_next_station_id_from_config(self, config):
        if 'nextStationId' in config:
            try:
                self.__next_station_id = int(config['nextStationId'])
            except ValueError:
                self.__next_station_id = len(self.__data)

    def __write_data_to_file(self):
        if len(self.__data) > 0:
            config = { 'stations': self.__data }
            with open(self.__configPath, 'w+') as file:
                json.dump(config, file, default=lambda o: o.__dict__, sort_keys=False, indent=2)
