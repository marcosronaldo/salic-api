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
        data = client.get('/v1/projetos/20001234').get_data(as_text=True)
        example = {
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
                        'cgccpf': '123.456.789-00',
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
                'proponente': 'v1/proponentes/3030303030303030303030303030303068da9e95bad279317b10bc1957fe',
            },

            # Campos do objeto
            'PRONAC': '20001234',
            'UF': 'DF',
            'acessibilidade': 'Acessibilidade',
            'ano_projeto': '2000',
            'area': 'Artes Cênicas',
            'cgccpf': '123.456.789-00',
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
            'objetivos': 'cutural',
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

        data = json.loads(data)
        assert sorted(data) == sorted(example)
        assert data['_links'] == example['_links']
        assert data['_embedded'] == example['_embedded']
        assert data == example
