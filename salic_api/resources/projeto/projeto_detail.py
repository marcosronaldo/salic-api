from salic_api.resources.resource_base import InvalidResult
from . import utils
from .models import (
    ProjetoQuery, CertidoesNegativasModelObject,
    DivulgacaoModelObject, DescolamentoModelObject,
    DistribuicaoModelObject, ReadequacaoModelObject,
    CaptacaoQuery
)
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import ListResource
from ..sanitization import sanitize
from ..serialization import listify_queryset
from ...app.security import encrypt

DISTRIBUICOES_KEY_MAP = {
    'area': 'area',
    'segmento': 'segmento',
    'produto': 'produto',
    'posicao_logo': 'posicao_logo',
    'QtdeOutros': 'qtd_outros',
    'QtdeProponente': 'qtd_proponente',
    'QtdeProduzida': 'qtd_produzida',
    'QtdePatrocinador': 'qtd_patrocinador',
    'QtdeVendaNormal': 'qtd_venda_normal',
    'QtdeVendaPromocional': 'qtd_venda_promocional',
    'PrecoUnitarioNormal': 'preco_unitario_normal',
    'PrecoUnitarioPromocional': 'preco_unitario_promocional',
    'Localizacao': 'localizacao',
}

DESLOCAMENTOS_KEY_MAP = {
    'PaisOrigem': 'pais_origem',
    'PaisDestino': 'pais_destino',
    'UFOrigem': 'uf_origem',
    'UFDestino': 'uf_destino',
    'MunicipioOrigem': 'municipio_origem',
    'MunicipioDestino': 'municipio_destino',
    'Qtde': 'quantidade',
}

DOCUMENTOS_KEY_MAP = {
    'Descricao': 'classificacao',
    'Data': 'data',
    'NoArquivo': 'nome',
}


class ProjetoDetail(ListResource):
    resource_path = 'projeto'
    query_class = ProjetoQuery

    def build_links(self, args={}):
        pronac = args['pronac']

        self.links = links = {}
        url_id = encrypt(args['proponente_id'])

        links['self'] = self.url('/projetos/' + pronac)
        links['proponente'] = self.url('/proponentes/%s' % url_id)
        links['incentivadores'] = self.url('/incentivadores/?pronac=' + pronac)
        links['fornecedores'] = self.url('/fornecedores/?pronac=' + pronac)

        self.captacoes_links = []
        for captacao in args['captacoes']:
            url = '/incentivadores/%s' % encrypt(captacao['cgccpf'])
            self.captacoes_links.append({
                'projeto': self.url('/projetos/%s' % pronac),
                'incentivador': self.url(url),
            })

        self.produtos_links = []
        for produto in args['produtos']:
            cgccpf_id = encrypt(produto['cgccpf'])
            self.produtos_links.append({
                'projeto': self.url('projetos/%s' % pronac),
                'fornecedor': self.url('/fornecedores/%s' % cgccpf_id),
            })

    def hal_builder(self, data, args=None):
        hal_data = data
        hal_data['_links'] = dict(self.links)
        hal_data['_embedded'] = {
            'captacoes': [], 'relacao_bens_captal': [],
            'marcas_anexadas': [], 'deslocamento': [],
            'divulgacao': [], 'relatorio_fisco': [],
            'certidoes_negativas': [], 'relacao_pagamentos': [],
            'readequacoes': [], 'documentos_anexados': [],
            'distribuicao': [], 'prorrogacao': []
        }

        for index in range(len(data['captacoes'])):
            data['captacoes'][index]['_links'] = self.captacoes_links[index]

        for index in range(len(data['relacao_pagamentos'])):
            data['relacao_pagamentos'][index]['_links'] = \
                self.produtos_links[index]

        for emb_field in hal_data['_embedded']:
            hal_data['_embedded'][emb_field] = data[emb_field]
            del data[emb_field]

        return hal_data

    def fetch_result(self, PRONAC):
        result, n_records = ProjetoQuery().all(limit=1, offset=0, PRONAC=PRONAC)
        if n_records == 0:
            raise InvalidResult({
                'message': 'No project with PRONAC %s' % PRONAC,
                'message_code': 11
            }, 404)
        return result

    def check_pronac(self, PRONAC):
        try:
            int(PRONAC)
        except ValueError:
            result = {
                'message': 'PRONAC must be an integer',
                'message_code': 10
            }
            raise InvalidResult(result, status_code=405)

    def finalize_result(self, result, PRONAC):
        # Sanitizing text values
        sanitize_fields = (
            'acessibilidade', 'objetivos', 'justificativa', 'etapa',
            'ficha_tecnica', 'impacto_ambiental', 'especificacao_tecnica',
            'estrategia_execucao', 'providencia', 'democratizacao', 'sinopse',
            'resumo',
        )
        for field in sanitize_fields:
            result[field] = sanitize(result[field], truncated=False)

        self.build_links(args={
            'PRONAC': PRONAC,
            'proponente_id': result['cgccpf'],
            'captacoes': result['captacoes'],
            'produtos': result['relacao_pagamentos'],
        })

        self.clean_cgcpf(result)

    def fetch_related(self, projeto, PRONAC):
        id_PRONAC = projeto.pop('IdPRONAC')

        # Certidões
        certidoes_negativas = CertidoesNegativasModelObject().all(PRONAC)
        projeto['certidoes_negativas'] = listify_queryset(certidoes_negativas)

        # Documentos anexados
        documentos = ProjetoQuery().attached_documents(id_PRONAC)
        projeto['documentos_anexados'] = self.cleaned_documentos(documentos)

        # Marcas anexadas
        marcas = ProjetoQuery().attached_brands(id_PRONAC)
        projeto['marcas_anexadas'] = marcas = listify_queryset(marcas)
        for marca in marcas:
            marca['link'] = utils.build_brand_link(marca)

        # Divulgação
        divulgacao = DivulgacaoModelObject().all(id_PRONAC)
        projeto['divulgacao'] = listify_queryset(divulgacao)

        # Deslocamentos
        deslocamentos = DescolamentoModelObject().all(id_PRONAC)
        projeto['deslocamento'] = self.cleaned_deslocamentos(deslocamentos)

        # Distribuições
        distribuicoes = DistribuicaoModelObject().all(id_PRONAC)
        projeto['distribuicao'] = self.cleaned_distribuicoes(distribuicoes)

        # Readequações
        readequacoes = ReadequacaoModelObject().all(id_PRONAC)
        projeto['readequacoes'] = self.cleaned_readequacoes(readequacoes)

        # Prorrogação
        prorrogacao = ProjetoQuery().postpone_request(id_PRONAC)
        projeto['prorrogacao'] = listify_queryset(prorrogacao)

        # Relação de pagamentos
        pagamentos = ProjetoQuery().payments_listing(idPronac=id_PRONAC)
        projeto['relacao_pagamentos'] = listify_queryset(pagamentos)

        # Relatório fisco
        relatorio_fisco = ProjetoQuery().taxing_report(id_PRONAC)
        projeto['relatorio_fisco'] = listify_queryset(relatorio_fisco)

        # Relação de bens de capital
        capital_goods = ProjetoQuery().goods_capital_listing(id_PRONAC)
        projeto['relacao_bens_captal'] = listify_queryset(capital_goods)

        # Captações
        captacoes = CaptacaoQuery().all(PRONAC=PRONAC)
        projeto['captacoes'] = listify_queryset(captacoes)

    # FIXME: @current_app.cache.cached(timeout=current_app.config['GLOBAL_CACHE_TIMEOUT'])
    def get(self, PRONAC):
        return super().get(PRONAC=PRONAC)

    def cleaned_deslocamentos(self, deslocamentos):
        deslocamentos = listify_queryset(deslocamentos)
        return list(map(map_keys(DESLOCAMENTOS_KEY_MAP), deslocamentos))

    def cleaned_documentos(self, documentos):
        result = []
        for doc in listify_queryset(documentos):
            link = utils.build_file_link(doc)
            if link == '':
                continue
            clean = {'link': link}
            clean.update(map_keys(DOCUMENTOS_KEY_MAP, doc))
            result.append(clean)
        return result

    def cleaned_readequacoes(self, readequacoes):
        readequacoes = listify_queryset(readequacoes)
        fields = (
            'descricao_justificativa',
            'descricao_avaliacao',
            'descricao_solicitacao',
        )
        for item in readequacoes:
            for field in fields:
                item[field] = sanitize(item[field], truncated=False)
        return readequacoes

    def cleaned_distribuicoes(self, distribuicoes):
        def clean(data):
            res = map_keys(DISTRIBUICOES_KEY_MAP, data)
            n_venda = res['qtd_venda_normal']
            n_promo = res['qtd_venda_promocional']
            preco = res['preco_unitario_normal']
            preco_promo = res['preco_unitario_promocional']
            res['receita_normal'] = n_venda * preco
            res['receita_promocional'] = n_promo * preco
            res['receita_prevista'] = n_venda * preco + n_promo * preco_promo
            return res

        distribuicoes = listify_queryset(distribuicoes)
        return list(map(clean, distribuicoes))

    def clean_cgcpf(self, result):
        result['cgccpf'] = result['cgccpf'] or '00000000000000'
        result["cgccpf"] = remove_blanks(str(result["cgccpf"]))
        result['cgccpf'] = cgccpf_mask(result['cgccpf'])

        for captacao in result['captacoes']:
            captacao['cgccpf'] = cgccpf_mask(captacao['cgccpf'])

        for produto in result['relacao_pagamentos']:
            produto['cgccpf'] = cgccpf_mask(produto['cgccpf'])


def map_keys(key_map, data=None):
    """
    Create a new dictionary using all keys from the given key_map mapping.

    >>> map_keys({1: 'one', 2: 'two'}, {1: 1, 2: 4, 3: 9})
    {'one': 1, 'two': 2}

    This function is curried and can be called with a single argument.
    """
    if data is None:
        return lambda data: map_keys(key_map, data)
    return {new: data[orig] for orig, new in key_map.items()}
