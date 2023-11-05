# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from pyfakefs.fake_filesystem_unittest import TestCase
from src.xonox import Config

class ConfigTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_persistence(self):
        this = Config(None)
        this['foo'] = 'bar'
        this['metamorphosator-id'] = 1337
        this.save()

        that = Config(None)

        assert 'foo' in that
        assert 'metamorphosator-id' in that
        assert that['foo'] == 'bar'
        assert that['metamorphosator-id'] == 1337