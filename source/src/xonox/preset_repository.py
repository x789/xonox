# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from . import Preset

class PresetRepository:
    def __init__(self, configDirectory):
        self.__data = []

    def get(self, device_id, preset_index):
        return Preset(device_id, preset_index, 0)