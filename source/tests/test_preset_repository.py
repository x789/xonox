from src.xonox.preset_repository import PresetRepository
from src.xonox.preset import Preset
from unittest import TestCase

class PresetRepositoryTestCase(TestCase):
    def test_init_without_config(self):
        device_id = 'ff0000'
        preset_index = 5
        sut = PresetRepository(None)

        preset = sut.get(device_id, preset_index)

        assert preset is not None
        assert preset.device_id == device_id
        assert preset.index == preset_index
        assert preset.station_id == 0