# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

class StationRepository:
    def __init__(self):
        self.__data = []

    def add(self, station):
        station.id = len(self.__data)
        self.__data.append(station)

    def get(self, id):
        return self.__data[id]

    def get_all(self):
        return self.__data.copy()

    def remove(self, id):
        self.__data.pop(id)
