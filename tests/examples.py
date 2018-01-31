PROJETOS_AREAS = {
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
    'mecanismo': 'Mecenato',
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
    'mecanismo': 'Mecenato',
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
PRODUTOS_RESPONSE = {
    "count": 1,
    "_embedded": {
        "produtos": [
            {
                "id_planilha_aprovacao": 1,
                "justificativa": None,
                "data_pagamento": None,
                "nome": None,
                "cgccpf": "1234",
                "tipo_forma_pagamento": None,
                "data_aprovacao": None,
                "valor_pagamento": None,
                "_links": {
                    "projeto": "v1/projetos/148794",
                    "fornecedor": "v1/fornecedores/1"
                },
                "id_arquivo": 1,
                "nr_comprovante": None,
                "nome_fornecedor": "Name",
                "id_comprovante_pagamento": 1,
                "tipo_documento": None,
                "nr_documento_pagamento": None,
                "nm_arquivo": None,
                "PRONAC": "20001234"
            }
        ]
    },
    "total": 17,
    "_links": {
        "self": "v1/fornecedores/1/produtos/?limit=100&offset=0",
        "first": "v1/fornecedores/1/produtos/?limit=100&offset=0",
        "last": "v1/fornecedores/1/produtos/?limit=100&offset=0",
        "next": "v1/fornecedores/1/produtos/?limit=100&offset=0"
    }
}
