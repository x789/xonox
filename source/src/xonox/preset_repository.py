# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from . import Preset

class PresetRepository:
    def __init__(self, config_directory):
        self.__data = dict()

    def add(self, preset):
        if preset.device_id not in self.__data.keys():
            self.__data[preset.device_id] = dict()
        
        self.__data[preset.device_id][preset.index] = preset


    def get(self, device_id, preset_index):
        return self.__data[device_id][preset_index]