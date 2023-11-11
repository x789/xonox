# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import json
from pathlib import Path
from os import path
from . import Station

class StationRepository:
    def __init__(self, config):
        self.__data = []
        self.__next_station_id = 0
        self.__config = config
        self.__read_data_from_config()

    def add(self, station):
        self.__add(station)
        self.__write_data_to_config()
        self.__save_config()

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
                self.__write_data_to_config()
                self.__save_config()
                return
        raise KeyError()

    def __add(self, station):        
        self.__update_next_station_id(station)
        self.__ensure_station_id_set(station)
        self.__data.append(station)

    def __ensure_station_id_set(self, station):
        if station.id is None:
            station.id = self.__next_station_id
            self.__next_station_id = self.__next_station_id + 1

    def __update_next_station_id(self, station):
        if station.id is not None and station.id >= self.__next_station_id:
            self.__next_station_id = station.id + 1

    def __read_data_from_config(self):
        self.__read_stations_from_config()
        self.__read_next_station_id_from_config()

    def __read_stations_from_config(self):
        if 'stations' in self.__config:
            stations = self.__config['stations']
            for station in stations:
                self.__add(Station(station['name'], station['description'], station['stream']))

    def __read_next_station_id_from_config(self):
        if 'nextStationId' in self.__config:
            try:
                self.__next_station_id = int(self.__config['nextStationId'])
            except ValueError:
                self.__next_station_id = len(self.__data)

    def __write_data_to_config(self):
        self.__config['stations'] = self.__data
        self.__config['nextStationId'] = self.__next_station_id

    def __save_config(self):
        self.__config.save()
