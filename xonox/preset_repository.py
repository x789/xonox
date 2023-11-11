# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from . import Preset

class PresetRepository:
    def __init__(self, config):
        self.__data = dict()
        self.__config = config
        self.__read_presets_from_config()

    def add(self, preset):
        self.__add(preset)
        self.__write_data_to_config()
        self.__save_config()

    def get(self, group_id, preset_index):
        return self.__data[group_id][preset_index]

    def get_all(self):
        all = []
        for v in self.__data.values():
            for preset in v.values():
                all.append(preset)
        return all

    def __add(self, preset):        
        if preset.group_id not in self.__data.keys():
            self.__data[preset.group_id] = dict()        
        self.__data[preset.group_id][preset.index] = preset

    def __read_presets_from_config(self):
        if 'presets' in self.__config:
            presets = self.__config['presets']
            for preset in presets:
                self.__add(Preset(preset['group_id'], preset['index'], preset['station_id']))

    def __write_data_to_config(self):
        self.__config['presets'] = self.get_all()

    def __save_config(self):
        self.__config.save()
