class TestCsv:
    def test_incentivador_csv(self, client):
        url = '/v1/incentivadores/30313233343536373839616263646566e0797636'
        expected = INCENTIVADOR_CSV
        check_csv(client, url, expected)

    def test_proponente_csv(self, client):
    	url = '/v1/proponentes/30313233343536373839616263646566e0797636'
    	expected = PROPONENTE_CSV
    	check_csv(client, url, expected)

    def test_preprojeto_csv(self, client):
        url = '/v1/propostas/1'
        expected = PROPOSTA_CSV
        check_csv(client, url, expected)


def check_csv(client, url, expected):
    response = client.get(url + '?format=csv')
    result = response.get_data(as_text=True)
    print('RESULT')
    print(result)
    print(expected)
    assert result == expected


INCENTIVADOR_CSV = """cgccpf,nome,responsavel,tipo_pessoa,UF,municipio,total_doado
1234,Nome,Responsavel,juridica,Uf,Cidade,0.0
""".replace('\n', '\r\n')


PROPONENTE_CSV = """cgccpf,nome,responsavel,tipo_pessoa,UF,total_captado,municipio
1234,Nome,Responsavel,juridica,Uf,1000,Cidade
""".replace('\n', '\r\n')

PROPOSTA_CSV = (
    "impacto_ambiental,ficha_tecnica,data_termino,id,mecanismo,"
    "data_arquivamento,data_inicio,democratizacao,data_aceite,sinopse,nome,"
    "estrategia_execucao,especificacao_tecnica,acessibilidade,objetivos,etapa,"
    "resumo,justificativa\r\n"

    "ImpactoAmbiental,FichaTecnica,2000-02-01,1,Descricao,2000-03-01,2000-01-01,"
    "DemocratizacaoDeAcesso,2000-01-01,Sinopse,Test,EstrategiadeExecucao,"
    "EspecificacaoTecnica,Acessibilidade,cultural,"
    "EtapaDeTrabalho,ResumoDoProjeto,Justificativa\r\n")
