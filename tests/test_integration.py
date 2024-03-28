# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2024 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import unittest
import docker
import os
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready, wait_for_logs

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

    def test_add_station(self):
        with XonoxContainer(self.image_tag) as ctr:
            ctr.wait_for_app()
            endpoint = ctr.base_url + "/station"

            payload = {"name": "foo", "description": "bar", "streamUrl": "http://foo/bar"}
            response = requests.post(endpoint, json=payload)
            assert(response.status_code == 201)

            response = requests.get(endpoint)
            assert(response.status_code == 200)
            response_payload = response.json()
            assert(len(response_payload) == 1)
            assert(response_payload[0]["id"] == 0)
            assert(response_payload[0]["name"] == "foo")
            assert(response_payload[0]["description"] == "bar")            
            assert(response_payload[0]["streamUrl"] == "http://foo/bar")