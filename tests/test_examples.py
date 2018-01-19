import json


class TestCoreUrls:
    valid_core_urls = [
        '/test',
        '/v1/projetos/areas',
        '/v1/projetos/segmentos',
    ]

    def test_core_url_examples(self, client):
        for url in self.valid_core_urls:
            assert client.get(url).status_code == 200, url

    def test_projetos_areas(self, client):
        data = client.get('/v1/projetos/areas').get_data(as_text=True)
        assert json.loads(data) == {
            '_embedded': {
                'areas': [
                    {
                        '_links': {'self': 'v1/projetos/?area=1'},
                        'codigo': '1',
                        'nome': 'Artes Cênicas'
                    },
                    {
                        '_links': {'self': 'v1/projetos/?area=2'},
                        'codigo': '2',
                        'nome': 'Audiovisual'
                    },
                    {
                        '_links': {'self': 'v1/projetos/?area=3'},
                        'codigo': '3',
                        'nome': 'Música'
                    },
                ],
            },
            '_links': {'self': 'v1/projetos/areas/'},
        }

    def test_projetos_detail(self, client):
        data = client.get('/v1/projetos/123').get_data(as_text=True)
        assert json.loads(data) == {

        }
