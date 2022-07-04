# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

class Preset:
    def __init__(self, device_id, preset_index, station_id):
        self.device_id = device_id
        self.index = preset_index
        self.station_id = station_id
