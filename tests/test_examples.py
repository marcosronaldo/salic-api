import unittest
import json

from flask import url_for


class TestCoreUrls:
    valid_core_urls = ['/test', '/v1/projetos/areas']

    def test_core_url_examples(self, client):
        for url in self.valid_core_urls:
            assert client.get(url).status_code == 200, url

    def test_number_of_areas(self, client):
        data = client.get('/v1/projetos/areas').get_data(as_text=True)
        assert json.loads(data) == {
            '_embedded': {
                'areas': [
                    {'_links': {'self': 'v1/projetos/?area=1'},
                     'codigo': '1',
                     'nome': 'Artes Cênicas'},
                    {'_links': {'self': 'v1/projetos/?area=2'},
                     'codigo': '2',
                     'nome': 'Audiovisual'},
                    {'_links': {'self': 'v1/projetos/?area=3'},
                     'codigo': '3',
                     'nome': 'Música'},
                ],
            },
            '_links': {'self': 'v1/projetos/areas/'},
        }


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
