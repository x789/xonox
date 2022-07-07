# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import json
from pathlib import Path
from os import path
from . import Preset

class PresetRepository:
    def __init__(self, config_directory):
        self.__data = dict()
        if config_directory is None:
            config_directory = Path.home()
        self.__configPath = path.join(config_directory, 'xonox-presets.conf')
        self.__load_data_from_file()

    def add(self, preset):
        if preset.device_id not in self.__data.keys():
            self.__data[preset.device_id] = dict()        
        self.__data[preset.device_id][preset.index] = preset
        self.__write_data_to_file()


    def get(self, device_id, preset_index):
        return self.__data[device_id][preset_index]

    def get_all(self):
        all = []
        for v in self.__data.values():
            for preset in v.values():
                all.append(preset)
        return all

    def __load_data_from_file(self):
        try:
            with open(self.__configPath, 'r') as file:
                config = json.load(file)
                self.__read_presets_from_config(config)
        except FileNotFoundError:
            pass

    def __read_presets_from_config(self, config):
        if 'presets' in config:
            presets = config['presets']
            for preset in presets:
                self.add(Preset(preset['device_id'], preset['index'], preset['station_id']))

    def __write_data_to_file(self):
        if len(self.__data) > 0:
            config = { 'presets': self.get_all() }
            with open(self.__configPath, 'w+') as file:
                json.dump(config, file, default=lambda o: o.__dict__, sort_keys=False, indent=2)
