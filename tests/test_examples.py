import copy
import json


class TestCoreUrls:
    valid_core_urls = [
        '/test',
        '/v1/projetos/areas',
        '/v1/projetos/segmentos',
    ]

    def check_endpoint(self, client, url, expected):
        data = client.get(url).get_data(as_text=True)
        data = json.loads(data)
        expected = copy.deepcopy(expected)
        assert sorted(data) == sorted(expected)
        assert data['_links'] == expected['_links']
        assert data == expected

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
        url = '/v1/projetos/20001234'
        expected = PROJETO_RESPONSE
        self.check_endpoint(client, url, expected)


    def test_projetos_list(self, client):
        data = client.get('/v1/projetos/').get_data(as_text=True)
        data = json.loads(data)
        expected = copy.deepcopy(PROJETO_RESPONSE)
        del expected['_embedded']

        expected = {
            'count': 1,
            '_embedded': {
                'projetos': [
                    expected,
                ]
            },
            '_links': {
                'self': 'v1/projetos/?limit=100&offset=0',
                'first': 'v1/projetos/?limit=100&offset=0',
                'last': 'v1/projetos/?limit=100&offset=0',
                'next': 'v1/projetos/?limit=100&offset=0',
            },
            'total': 1,
        }
        assert sorted(data) == sorted(expected)
        project_data, = data['_embedded']['projetos']
        project_expected, = expected['_embedded']['projetos']
        assert project_data == project_expected
        assert data == expected

    def test_incentivadores_detail(self, client):
        url = '/v1/incentivadores/30313233343536373839616263646566e0797636'
        expected = INCENTIVADOR_RESPONSE
        self.check_endpoint(client, url, expected)

    def test_fornecedores_detail(self, client):
        url = '/v1/fornecedores/30313233343536373839616263646566e0797636'
        expected = FORNECEDOR_RESPONSE
        self.check_endpoint(client, url, expected)

    def test_preprojetos_detail(self, client):
        url = '/v1/propostas/1'
        expected = PREPROJETO_RESPONSE
        self.check_endpoint(client, url, expected)

    def test_preprojetos_list(self, client):
        url = '/v1/propostas/'
        expected = copy.deepcopy(PREPROJETO_RESPONSE)

        expected = {
            'count': 1,
                '_embedded': {
                    'propostas': [
                        expected,
                    ]
                },
                '_links': {
                    'self': 'v1/propostas/propostas/?limit=100&offset=0',
                    'first': 'v1/propostas/propostas/?limit=100&offset=0',
                    'last': 'v1/propostas/propostas/?limit=100&offset=0',
                    'next': 'v1/propostas/propostas/?limit=100&offset=0',
                },
                'total': 1,
        }
        self.check_endpoint(client, url, expected)

    def test_proponentes_detail(self, client):
        url = '/v1/proponentes/30313233343536373839616263646566e0797636'
        expected = PROPONENTE_RESPONSE
        self.check_endpoint(client, url, expected)

    def test_proponentes_list(self, client):
        data = client.get('/v1/proponentes/').get_data(as_text=True)
        data = json.loads(data)
        expected = copy.deepcopy(PROPONENTE_RESPONSE)

        expected = {
            'count': 1,
            '_embedded': {
                'proponentes': [
                    expected,
                ]
            },
            '_links': {
                'self': 'v1/proponentes/proponentes/?limit=100&offset=0',
                'first': 'v1/proponentes/proponentes/?limit=100&offset=0',
                'last': 'v1/proponentes/proponentes/?limit=100&offset=0',
                'next': 'v1/proponentes/proponentes/?limit=100&offset=0',
            },
            'total': 1,
        }
        assert sorted(data) == sorted(expected)
        proponente_data, = data['_embedded']['proponentes']
        proponente_expected, = expected['_embedded']['proponentes']
        assert proponente_data == proponente_expected
        assert data == expected

    def test_projeto_captacoes(self, client):
        url = '/v1/projetos/20001234/captacoes'
        expected = CAPTACOES_RESPONSE
        self.check_detail_endpoint(client, url, expected)


PROJETO_RESPONSE = {
    # Embedded data
    '_embedded': {
        'relacao_bens_captal': [],
        'marcas_anexadas': [],
        'deslocamento': [],
        'divulgacao': [],
        'relatorio_fisco': [],
        'certidoes_negativas': [
            {
                'data_emissao': '2000-01-01',
                'data_validade': '2000-03-01',
                'descricao': None,
                'situacao': 'Não Pendente'
            }
        ],
        'relacao_pagamentos': [],
        'readequacoes': [],
        'documentos_anexados': [],
        'distribuicao': [],
        'prorrogacao': [],
        'captacoes': [
            {
                'PRONAC': '20001234',
                'cgccpf': '1234',
                'data_recibo': '2000-01-01',
                'nome_doador': 'Nome',
                'nome_projeto': 'Test',
                'valor': 'CaptacaoReal'
            }
        ],
    },

    # Links
    '_links': {
        'fornecedores': 'v1/fornecedores/?pronac=20001234',
        'incentivadores': 'v1/incentivadores/?pronac=20001234',
        'self': 'v1/projetos/20001234',
        'proponente': 'v1/proponentes/30313233343536373839616263646566e0797636',
    },

    # Campos do objeto
    'PRONAC': '20001234',
    'UF': 'DF',
    'acessibilidade': 'Acessibilidade',
    'ano_projeto': '2000',
    'area': 'Artes Cênicas',
    'cgccpf': '1234',
    'data_inicio': '2000-01-01',
    'data_termino': '2000-02-01',
    'democratizacao': 'DemocratizacaoDeAcesso',
    'enquadramento': 'Artigo 26',
    'especificacao_tecnica': 'EspecificacaoTecnica',
    'estrategia_execucao': 'EstrategiadeExecucao',
    'etapa': 'EtapaDeTrabalho',
    'ficha_tecnica': 'FichaTecnica',
    'impacto_ambiental': 'ImpactoAmbiental',
    'justificativa': 'Justificativa',
    'mecanismo': 'Descricao',
    'municipio': 'Cidade',
    'nome': 'Test',
    'objetivos': 'cultural',
    'outras_fontes': 0,
    'proponente': 'Nome',
    'providencia': 'nenhuma',
    'resumo': 'ResumoDoProjeto',
    'segmento': 'Descricao',
    'sinopse': 'Sinopse',
    'situacao': 'Descricao',
    'valor_aprovado': 1000,
    'valor_captado': 1000,
    'valor_projeto': 1000,
    'valor_proposta': 1000,
    'valor_solicitado': 1000,
}

INCENTIVADOR_RESPONSE = {
    'UF': 'Uf',
    '_links': {
        'self': 'v1/incentivadores/30313233343536373839616263646566e0797636',
        'doacoes': 'v1/incentivadores/30313233343536373839616263646566e0797636/doacoes',
    },
    'cgccpf': '1234',
    'municipio': 'Cidade',
    'nome': 'Nome',
    'responsavel': 'Responsavel',
    'tipo_pessoa': 'juridica',
    'total_doado': 0.0,
}

FORNECEDOR_RESPONSE = {
    "cgccpf": "1234",
    "_links": {
        "self": "v1/fornecedores/30313233343536373839616263646566e0797636",
        "produtos": "v1/fornecedores/30313233343536373839616263646566e0797636/produtos"
    },
    "email": "email",
    "nome": "Name"
}

PROPONENTE_RESPONSE = {
    'nome': 'Nome',
    'cgccpf': '1234',
    '_links': {
        'self': 'v1/proponentes/30313233343536373839616263646566e0797636',
        'projetos': 'v1/projetos/?proponente_id=30313233343536373839616263646566e0797636'
    },
    'tipo_pessoa': 'juridica',
    'responsavel': 'Responsavel',
    'UF': 'Uf',
    'total_captado': 1000,
    'municipio': 'Cidade',
}

PREPROJETO_RESPONSE = {
    'acessibilidade': 'Acessibilidade',
    'data_aceite': '2000-01-01',
    'data_arquivamento': '2000-03-01',
    'data_inicio': '2000-01-01',
    'data_termino': '2000-02-01',
    'democratizacao': 'DemocratizacaoDeAcesso',
    'especificacao_tecnica': 'EspecificacaoTecnica',
    'estrategia_execucao': 'EstrategiadeExecucao',
    'etapa': 'EtapaDeTrabalho',
    'ficha_tecnica': 'FichaTecnica',
    'id': 1,
    'impacto_ambiental': 'ImpactoAmbiental',
    'justificativa': 'Justificativa',
    'mecanismo': 'Descricao',
    'nome': 'Test',
    'objetivos': 'cultural',
    'resumo': 'ResumoDoProjeto',
    'sinopse': 'Sinopse',
    '_links': {
        'self': 'v1/propostas/1',
    },
}
CAPTACOES_RESPONSE = {
    '_embedded': {
        'captacoes': [
            {
                'PRONAC': '20001234',
                'cgccpf': '1234',
                'data_recibo': '2000-01-01',
                'nome_doador': 'Nome',
                'nome_projeto': 'Test',
                'valor': 'CaptacaoReal'
            }
        ]
    },
    '_links': {
        'first': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
        'last': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
        'self': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
        'next': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
    },
    'count': 1,
    'total': 1,
}
