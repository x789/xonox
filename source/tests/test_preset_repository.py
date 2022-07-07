from pyfakefs.fake_filesystem_unittest import TestCase
from src.xonox.preset_repository import PresetRepository
from src.xonox.preset import Preset

class PresetRepositoryTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_init_without_presets(self):
        sut = PresetRepository(None)

        stations = sut.get_all()

        assert len(stations) == 0

    def test_persistence(self):
        preset1 = Preset('000000001', 1, 1101)
        preset2 = Preset('000000001', 2, 1102)
        preset3 = Preset('000000001', 3, 1103)
        preset4 = Preset('000000001', 4, 1104)
        first = PresetRepository(None)
        first.add(preset1)
        first.add(preset2)
        first.add(preset3)
        first.add(preset4)
        
        sut = PresetRepository(None)

        assert len(sut.get_all()) == 4
        actual = sut.get(preset1.device_id, preset1.index)
        assert actual is not None
        assert actual.device_id == preset1.device_id
        assert actual.index == preset1.index
        assert actual.station_id == preset1.station_id
        actual = sut.get(preset2.device_id, preset2.index)
        assert actual is not None
        assert actual.device_id == preset2.device_id
        assert actual.index == preset2.index
        assert actual.station_id == preset2.station_id
        actual = sut.get(preset3.device_id, preset3.index)
        assert actual is not None
        assert actual.device_id == preset3.device_id
        assert actual.index == preset3.index
        assert actual.station_id == preset3.station_id
        actual = sut.get(preset4.device_id, preset4.index)
        assert actual is not None
        assert actual.device_id == preset4.device_id
        assert actual.index == preset4.index
        assert actual.station_id == preset4.station_id

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

        assert len(sut.get_all()) == 1
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

        assert len(sut.get_all()) == 2
        actual = sut.get(device_id, preset_index)
        assert actual is not None
        assert actual.device_id == device_id
        assert actual.index == preset_index
        assert actual.station_id == station_id