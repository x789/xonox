# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from . import Preset, PresetRepository

class PresetService:
    def __init__(self, config):
        self.__config = config
        self.__repository = PresetRepository(config)
    
    def add_preset(self, device_id, preset_index, station_id):
        '''Adds or overwrites a preset. If the global preset list is active, 'device_id' is ignored.'''
        group_id = self.__determine_group_id(device_id)
        preset = Preset(group_id, preset_index, station_id)
        self.__repository.add(preset)

    def get_preset(self, device_id, preset_index):
        '''Gets a preset. If the global preset list is active, 'device_id' is ignored.'''
        group_id = self.__determine_group_id(device_id)
        return self.__repository.get(group_id, preset_index)

    def get_all_presets(self):
        '''Gets all presets.'''
        return self.__repository.get_all()

    def __determine_group_id(self, device_id):
        if 'settings' not in self.__config or 'useGlobalPresetList' not in self.__config['settings'] or self.__config['settings']['useGlobalPresetList']:
            return 'global'
        else:
            return device_id