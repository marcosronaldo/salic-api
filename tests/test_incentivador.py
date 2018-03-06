import pytest
import requests
import json


salic_url_base = "http://api.salic.cultura.gov.br/v1/"
api_url_base = "http://localhost:5000/v1/"


class TestIncentivador:
    def test_list_fields(self):
        salic, api = make_request('incentivadores')
        assert check_fields(salic, api)

    def test_incentivadores_list(self):
        salic, api = make_request('incentivadores')
        assert check_fields(salic, api, '_embedded')

    def test_incentivadores_links(self):
        salic, api = make_request('incentivadores')
        assert check_fields(salic, api, '_links')

    def test_specific_incentivador_fields(self):
        salic, api = make_request('incentivadores')


        assert check_fields(salic['_embedded']['incentivadores'][1],
                            api['_embedded']['incentivadores'][1])

def make_request(endpoint):
    result_salic = requests.get(salic_url_base + endpoint)
    salic_data = json.loads(result_salic.text)

    result_api = requests.get(api_url_base + endpoint)
    api_data = json.loads(result_api.text)

    return salic_data, api_data

def check_fields(salic_data, api_data, specific_field=None):
    if specific_field is not None:
        salic_data = salic_data.get(specific_field)
        api_data = api_data.get(specific_field)

    for key in salic_data.keys():
        if key not in api_data:
            return False
    
    return True
