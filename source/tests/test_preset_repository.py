from src.xonox.preset_repository import PresetRepository
from src.xonox.preset import Preset
from unittest import TestCase

class PresetRepositoryTestCase(TestCase):
    def test_get_unknown_device_from_empty(self):
        sut = PresetRepository(None)

        with self.assertRaises(KeyError):
            preset = sut.get('ff0000', 4)

    def test_get_unknown_index_from_empty(self):
        device_id = 'ff0000'
        preset = Preset(device_id, 3, 15)
        sut = PresetRepository(None)
        sut.add(preset)

        with self.assertRaises(KeyError):
            preset = sut.get(device_id, 2)

    def test_add_to_empty(self):
        device_id = 'aaff3300ff00bbccddeeff4433'
        preset_index = 3
        station_id = 46
        preset = Preset(device_id, preset_index, station_id)
        sut = PresetRepository(None)

        sut.add(preset)

        actual = sut.get(device_id, preset_index)
        assert actual is not None
        assert actual.device_id == device_id
        assert actual.index == preset_index
        assert actual.station_id == station_id

    def test_add_to_nonempty(self):
        device_id = 'aaff3300ff00bbccddeeff4433'
        preset_index = 3
        station_id = 46
        sut = PresetRepository(None)
        sut.add(Preset('af3f58972486a9724664deedd', 9, 97426))
        preset = Preset(device_id, preset_index, station_id)

        sut.add(preset)

        actual = sut.get(device_id, preset_index)
        assert actual is not None
        assert actual.device_id == device_id
        assert actual.index == preset_index
        assert actual.station_id == station_id