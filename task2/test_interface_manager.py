import json
import unittest
from logging import Logger
from typing import Dict
from unittest.mock import patch

import httpretty

from interface_manager import protocol, InterfaceManager


class TestApp(unittest.TestCase):

    @patch('configparser.ConfigParser')
    @patch('logging.Logger')
    def setUp(self, logger: Logger, conf: Dict):
        self.url = 'http://test.sk/interfaces'
        self.interface_manager = InterfaceManager(self.url, logger, {}, conf)
        self.logger = logger
        self.conf = conf

    def test_protocol(self):
        self.assertEqual(protocol(False), 'http')
        self.assertEqual(protocol(True), 'https')

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_get_all_interfaces_exception(self):
        httpretty.register_uri(httpretty.GET, self.url, status=400)
        self.assertRaises(SystemExit, self.interface_manager._get_all_interfaces)
        self.logger.exception.assert_called_with("Error: it is not possible to get data from the specified URL.")

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_get_all_interfaces_content(self):
        self.test_interface_str = '''[
                   {
                       "cisco-ethernet:ethernet": {},
                       "cisco-pw:pw-neighbor": {
                           "load-balance": {}
                       },
                       "description": "FE000",
                       "enabled": false,
                       "ietf-ip:ipv4": {},
                       "ietf-ip:ipv6": {
                           "ietf-ipv6-unicast-routing:ipv6-router-advertisements": {}
                       },
                       "link-up-down-trap-enable": "enabled",
                       "name": "FastEthernet0/0/0",
                       "type": "ianaift:ethernetCsmacd"
                   }]'''
        httpretty.register_uri(httpretty.GET, self.url, body=self.test_interface_str)
        response = self.interface_manager._get_all_interfaces()
        self.assertTrue(len(response) == 1)
        self.assertEqual(response[0].name, "FastEthernet0/0/0")

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_analyze_return(self):
        with open('test_data/test_logg_data.json') as ld, open('test_data/dataclass_data.json') as dd:
            self.logg_data = json.loads(ld.read())
            self.dataclass_data = dd.read()
        httpretty.register_uri(httpretty.GET, self.url, body=self.dataclass_data)
        analyze = self.interface_manager.analyze()
        self.assertTrue(len(analyze), len(self.logg_data))
        self.assertTrue(analyze, "enabled_interfaces")
        self.assertEqual(analyze.keys(), self.logg_data.keys())


if __name__ == '__main__':
    unittest.main()
