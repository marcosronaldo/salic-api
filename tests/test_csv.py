class TestCsv:
    def test_incentivador_csv(self, client):
        url = '/v1/incentivadores/30313233343536373839616263646566e0797636'
        response = client.get(url + '?format=csv')
        result = response.get_data(as_text=True)
        print('RESULT')
        print(result)
        print(INCENTIVADOR_CSV)
        assert result == INCENTIVADOR_CSV


INCENTIVADOR_CSV = """cgccpf,nome,responsavel,tipo_pessoa,UF,municipio,total_doado
1234,Nome,Responsavel,juridica,Uf,Cidade,0.0
""".replace('\n', '\r\n')
