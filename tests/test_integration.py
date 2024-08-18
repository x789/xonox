# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2024 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import unittest
import docker
import os
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready, wait_for_logs
import xml.etree.ElementTree as ET

class XonoxContainer(DockerContainer):
    def __init__(self, image):
        super(XonoxContainer, self).__init__(image)
        self.with_exposed_ports(80)


    @wait_container_is_ready()
    def wait_for_app(self):
        wait_for_logs(self, "Serving Flask app 'xonox.server'")
        self.base_url = f"http://{self.get_container_host_ip()}:{self.get_exposed_port(80)}"


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = docker.from_env()
        cls.image_tag = "xonox_integration_test"
        cls.image, *_ = cls.client.images.build(path=os.getcwd(), tag=cls.image_tag)


    @classmethod
    def tearDownClass(cls):
        cls.client.images.remove(cls.image.id, force=True)


    def test_integration(self):
        with XonoxContainer(self.image_tag) as ctr:
            ctr.wait_for_app()
            xonox_client = XonoxClient(ctr.base_url)
            iradio300_client = IRadio300Client(ctr.base_url, "aff2")
            noxon2_client = Noxon2Client(ctr.base_url, "aff4")

            local_stations = [ {"name": "abc", "description": "first", "streamUrl": "http://abc/mp3-stream"},
                         {"name": "def", "description": "second", "streamUrl": "http://def/stream"},
                         {"name": "xyz", "description": "last", "streamUrl": "http://xyz.example.com/"}
            ]

            # Verify prerequisites
            assert len(xonox_client.get_station_list()) == 0
            assert xonox_client.get_settings() == {}

            # Enable global presets
            settings = {"useGlobalPresetList": True}
            xonox_client.write_settings(settings)
            assert xonox_client.get_settings() == settings

            # Add local stations
            for station in local_stations:
                xonox_client.add_station(station)

            # Get the remote station list
            remote_stations = xonox_client.get_station_list()

            # Check if the remote list contains all local stations
            assert self.__remove_ids(remote_stations) == local_stations

            # Receive station list (iRadio 300)
            playback_list = iradio300_client.get_station_list()
            default_data = {"type": "Station", "format": "Public", "location": "n/a", "bandwidth": "128", "content-type": "MP3", "reliability": "1", "bookmark-url": f"{ctr.base_url}//noOp", "logo-url": f"{ctr.base_url}//noOp"}
            expected_data = []
            for index, value in enumerate(local_stations):
                expected_data.append({**value, **default_data, "id": str(index)})
            assert playback_list == expected_data

            # "Play" second station (iRadio 300)
            playback_data = iradio300_client.get_station_data(1)
            assert playback_data["id"] == "1"
            assert playback_data["name"] == local_stations[1]["name"]
            assert playback_data["streamUrl"] == local_stations[1]["streamUrl"]
            assert playback_data["description"] == local_stations[1]["description"]

            # Get non-existing preset #1 (iRadio 300)
            item = iradio300_client.get_preset(1)
            assert item["type"] == "Message"
            assert item["message"] == "Preset not found"

            # Create a preset for second station at index 1. (iRadio 300)
            item = iradio300_client.set_preset(1)
            assert item["type"] == "Message"
            assert item["message"] == "Preset set"

            # Fetch the preset (iRadio 300)
            preset = iradio300_client.get_preset(1)
            assert preset == {**local_stations[1], **default_data, "id": "1"}
            

            # Receive station list (Noxon2)
            playback_list = noxon2_client.get_station_list()
            default_data = {"type": "Station", "format": "Public", "location": "n/a", "bandwidth": "128", "content-type": "MP3", "reliability": "1", "bookmark-url": f"{ctr.base_url}//noOp", "logo-url": f"{ctr.base_url}//noOp"}
            expected_data = []
            for index, value in enumerate(local_stations):
                expected_data.append({**value, **default_data, "id": str(index)})
            assert playback_list == expected_data

            # "Play" third station (Noxon2)
            playback_data = noxon2_client.get_station_data(2)
            assert playback_data["id"] == "2"
            assert playback_data["name"] == local_stations[2]["name"]
            assert playback_data["streamUrl"] == local_stations[2]["streamUrl"]
            assert playback_data["description"] == local_stations[2]["description"]

            # Get non-existing preset #2 (Noxon2)
            item = noxon2_client.get_preset(2)
            assert item["type"] == "Message"
            assert item["message"] == "Preset not found"

            # Create a preset for second station at index 2. (Noxon2)
            item = noxon2_client.set_preset(2)
            assert item["type"] == "Message"
            assert item["message"] == "Preset set"

            # Fetch the preset (Noxon2)
            preset = noxon2_client.get_preset(2)
            assert preset == {**local_stations[2], **default_data, "id": "2"}

            # Delete a station
            id_of_second_station = [s["id"] for s in remote_stations if s["name"] == local_stations[1]["name"]][0]
            xonox_client.delete_station(id_of_second_station)

            # Check if second station is missing from remote list
            remote_stations = xonox_client.get_station_list()
            assert self.__remove_ids(remote_stations) == [local_stations[0], local_stations[-1]]
            

    def __remove_keys(self, d, keys_to_ignore):
        return {k: v for k, v in d.items() if k not in keys_to_ignore}


    def __remove_ids(self, source):
        return [self.__remove_keys(d, ["id"]) for d in source]

class RadioClientBase:
    def __init__(self, base_url, search_path, login_path, mac_address):
        self.base_url = base_url
        self.search_path = search_path
        self.login_path = login_path
        self.mac_address = mac_address
        

    def get_station_data(self, id):
        response = requests.get(f"{self.base_url}{self.search_path}?sSearchtype=3&Search={id}&mac={self.mac_address}&dlang=eng&fver=79&hw=10143&ven=Terratec")
        assert response.status_code == 200
        items = self.__noxon_item_list_to_python(response.text)
        assert len(items) == 1
        return items[0]
    
    
    def get_station_list(self):
        response = requests.get(f"{self.base_url}{self.login_path}?mac={self.mac_address}")
        assert response.status_code == 200
        return self.__noxon_item_list_to_python(response.text)
    

    def get_preset(self, index):
        response = requests.get(f"{self.base_url}/Favorites/GetPreset.aspx?mac={self.mac_address}&dlang=eng&fver=79&hw=10143&id={index}&itemid=")
        assert response.status_code == 200
        items = self.__noxon_item_list_to_python(response.text)
        assert len(items) == 1
        return items[0]
    

    def set_preset(self, index):
        response = requests.get(f"{self.base_url}/Favorites/AddPreset.aspx?mac={self.mac_address}&dlang=eng&fver=79&hw=10143&id={index}&itemid=")
        print(response.text)
        assert response.status_code == 200
        items = self.__noxon_item_list_to_python(response.text)
        assert len(items) == 1
        return items[0]


    def __noxon_item_list_to_python(self, response_body):
        root = ET.fromstring(response_body)
        items = root.findall("Item")
        result = []
        for item in items:
            if item.find("ItemType").text == "Message":
                result.append(self.__noxon_message_to_dict(item))
            else:
                result.append(self.__noxon_item_to_dict(item))
        return result


    def __noxon_message_to_dict(self, item):
        return {"type": "Message", "message": item.find("Message").text}


    def __noxon_item_to_dict(self, item):
        return {
            "id": item.find("StationId").text,
            "name": item.find("StationName").text,
            "streamUrl": item.find("StationUrl").text,
            "description": item.find("StationDesc").text,
            "type": item.find("ItemType").text,
            "format": item.find("StationFormat").text,
            "location": item.find("StationLocation").text,
            "bandwidth": item.find("StationBandWidth").text,
            "content-type": item.find("StationMime").text,
            "reliability": item.find("Relia").text,
            "bookmark-url": item.find("Bookmark").text,
            "logo-url": item.find("Logo").text
        }

class XonoxClient:
    def __init__(self, base_url):
        self.base_url = base_url


    def get_station_list(self):
        response = requests.get(f"{self.base_url}/station")
        assert response.status_code == 200
        return response.json()


    def add_station(self, station):
        response = requests.post(f"{self.base_url}/station", json=station)
        assert response.status_code == 201


    def delete_station(self, id):
        response = requests.delete(f"{self.base_url}/station/{id}")
        assert response.status_code == 204
    

    def get_settings(self):
        response = requests.get(f"{self.base_url}/settings")
        assert response.status_code == 200
        return response.json()
    

    def write_settings(self, settings):
        response = requests.post(f"{self.base_url}/settings", json=settings)
        assert response.status_code == 204


class Noxon2Client(RadioClientBase):
    def __init__(self, base_url, mac_address):
        super().__init__(base_url, "/setupapp/radio567/asp/BrowseXPA/Search.asp", "/setupapp/radio567/asp/BrowseXPA/LoginXML.asp", mac_address)


class IRadio300Client(RadioClientBase):
    def __init__(self, base_url, mac_address):
        super().__init__(base_url, "/setupapp/fs/asp/BrowseXML/Search.asp", "/setupapp/fs/asp/BrowseXML/loginXML.asp", mac_address)
