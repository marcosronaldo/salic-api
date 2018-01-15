import unittest

from flask import url_for


class TestCoreUrls:
    valid_core_urls = ['/api/v1/']

    def test_core_url_examples(self, client):
        for url in self.valid_core_urls:
            client.get(url_for(url)).status_code == 200


# class TestFlaskApiUsingRequests(unittest.TestCase):
#     def test_hello_world(self):
#         response = requests.get('http://localhost:5000')
#         self.assertEqual(response.json(), {'hello': 'world'})


class TestFlaskApi(unittest.TestCase):
    # def setUp(self):
    #     self.app = flaskapi.app.test_client()
    #
    # def test_hello_world(self):
    #     response = self.app.get('/')
    pass
