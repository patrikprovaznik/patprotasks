import json
import unittest

from interface_api import app


class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        with open('../resource/task-1-interfaces.json') as f:
            data = json.loads(f.read())
            self.interfaces = data['ietf-interfaces:interfaces']['interface']
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.client.application.cache = {interface['name']: interface for interface in self.interfaces}

    def tearDown(self):
        self.ctx.pop()

    def test_get_all_interfaces(self):
        response = self.client.get('/get-all-interfaces')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json)
        self.assertEqual(response.json, self.interfaces)
        self.assertEqual(len(response.json), len(self.interfaces))

    def test_get_some_interface(self):
        response = self.client.get('/get-interface/FastEthernet0/0/2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json in self.interfaces)

    def test_get_interfaces(self):
        self.test_post_data = {
            "input": {
                "interfaces": [{
                    "name": "FastEthernet0/0/1",
                    "type": "ianaift:ethernetCsmacd"
                },
                    {
                        "name": None,
                        "type": "ianaift:ethernetCsmacd",
                        "enabled": False
                    }]
            }
        }
        response = self.client.post('/get-interfaces', json=self.test_post_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_interface(self):
        response_delete = self.client.delete('/delete-interface/FastEthernet0/0/3')
        response_all = self.client.get('/get-all-interfaces')
        self.assertEqual(response_delete.status_code, 200)
        self.assertTrue(response_delete.json not in self.interfaces)
        self.assertEqual(len(response_all.json), len(self.interfaces) - 1)


if __name__ == '__main__':
    unittest.main()
