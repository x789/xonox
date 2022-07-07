from pyfakefs.fake_filesystem_unittest import TestCase
from src.xonox.station_repository import StationRepository
from src.xonox.station import Station
from os import path

class StationRepositoryTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_init_without_config(self):
        sut = StationRepository(None)

        stations = sut.get_all()

        assert len(stations) == 0

    def test_get_unknown(self):
        station = Station('foo', 'bar', 'http://example.stream')
        sut = StationRepository(None)
        sut.add(station)
        
        with self.assertRaises(KeyError):
            sut.get(29725)

    def test_get_unknown_when_empty(self):
        sut = StationRepository(None)
        
        with self.assertRaises(KeyError):
            sut.get(0)

    def test_delete(self):
        station = Station('foo', 'bar', 'http://example.stream')
        sut = StationRepository(None)
        sut.add(station)

        sut.remove(0)

        assert len(sut.get_all()) == 0

    def test_delete_unknown(self):
        station = Station('foo', 'bar', 'http://example.stream')
        sut = StationRepository(None)
        sut.add(station)

        with self.assertRaises(KeyError):
            sut.remove(-10)

    def test_add_new_to_empty(self):
        station = Station('foo', 'bar', 'http://example.stream')
        sut = StationRepository(None)

        sut.add(station)

        assert len(sut.get_all()) == 1
        assert sut.get(0) is not None
        assert sut.get(0).id == 0

    def test_add_new_to_nonempty(self):
        sut = StationRepository(None)
        sut.add(Station('1', 'one', 'http://example.stream/1'))

        sut.add(Station('2', 'two', 'http://example.stream/2'))

        assert len(sut.get_all()) == 2
        assert sut.get(0) is not None
        assert sut.get(1) is not None
        assert sut.get(0).id == 0
        assert sut.get(0).name is '1'
        assert sut.get(0).description is 'one'
        assert sut.get(0).stream is 'http://example.stream/1'
        assert sut.get(1).id == 1
        assert sut.get(1).name is '2'
        assert sut.get(1).description is 'two'
        assert sut.get(1).stream is 'http://example.stream/2'

    def test_add_old_to_empty(self):
        station = Station('foo', 'bar', 'http://example.stream', 3597)
        sut = StationRepository(None)

        sut.add(station)

        assert len(sut.get_all()) == 1
        assert sut.get(3597) is not None
    
    def test_add_old_after_new(self):
        sut = StationRepository(None)
        sut.add(Station('1', 'one', 'http://example.stream/1'))

        sut.add(Station('foo', 'bar', 'http://example.stream', 1337))

        assert len(sut.get_all()) == 2
        assert sut.get(0) is not None
        assert sut.get(1337) is not None
        assert sut.get(0).id == 0
        assert sut.get(0).name is '1'
        assert sut.get(0).description is 'one'
        assert sut.get(0).stream is 'http://example.stream/1'
        assert sut.get(1337).id == 1337
        assert sut.get(1337).name is 'foo'
        assert sut.get(1337).description is 'bar'
        assert sut.get(1337).stream is 'http://example.stream'

    def test_add_new_after_old(self):
        sut = StationRepository(None)
        sut.add(Station('foo', 'bar', 'http://example.stream', 1337))

        sut.add(Station('1', 'one', 'http://example.stream/1'))

        assert len(sut.get_all()) == 2
        assert sut.get(1337) is not None
        assert sut.get(1338) is not None
        assert sut.get(1337).id == 1337
        assert sut.get(1337).name is 'foo'
        assert sut.get(1337).description is 'bar'
        assert sut.get(1337).stream is 'http://example.stream'
        assert sut.get(1338).id == 1338
        assert sut.get(1338).name is '1'
        assert sut.get(1338).description is 'one'
        assert sut.get(1338).stream is 'http://example.stream/1'

    def test_issue_3(self):
        """Tests the fix for issue #3. See https://github.com/x789/xonox/issues/3 for details."""
        sut = StationRepository(None)
        sut.add(Station('Station A', 'AAA', 'http://example.stream/A'))
        sut.add(Station('Station B', 'BBB', 'http://example.stream/B'))
        sut.add(Station('Station C', 'CCC', 'http://example.stream/C'))
        sut.remove(1)
        
        sut.add(Station('Station D', 'DDD', 'http://example.stream/D'))

        assert len(sut.get_all()) == 3
        assert sut.get(0) is not None
        assert sut.get(2) is not None
        assert sut.get(3) is not None

    def test_add_colliding_ids(self):
        """
        IDs are unique. Before v0.0.6 collisions could occur but there is no automatic solution for that issue. This test is primarily for documentation purpose.
        See https://github.com/x789/xonox/issues/3 for details.
        """
        sut = StationRepository(None)
        sut.add(Station('foo', 'bar', 'http://example.stream', 15))

        sut.add(Station('1', 'one', 'http://example.stream/1', 15))

        assert len(sut.get_all()) == 2
        s = sut.get(15)
        assert s is not None
        assert s.id == 15
        assert s.name is 'foo'
        assert s.description is 'bar'
        assert s.stream is 'http://example.stream'

    def test_persistence_of_id_counter(self):
        old_repository = StationRepository(None)
        old_repository.add(Station('foo', 'bar', 'http://example.stream', 15))
        old_repository.remove(15)
        sut = StationRepository(None)
        expected = Station('Radio Tralalala', 'Finest Tralala Music', 'http://metamorphosator.com/stream')

        sut.add(expected)

        assert sut.get(16) is not None
        actual = sut.get(16)
        assert actual.id == expected.id
        assert actual.name == expected.name
        assert actual.description == expected.description
        assert actual.stream == expected.stream
