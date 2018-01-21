from . import utils
from .models import (
    ProjetoQuery, CertidoesNegativasQuery, DivulgacaoQuery, DescolamentoQuery,
    DistribuicaoQuery, ReadequacaoQuery, CaptacaoQuery
)
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import DetailResource, InvalidResult
from ..sanitization import sanitize
from ..serialization import listify_queryset
from ...app.security import encrypt

#
# Map values from SQL model to JSON result
#
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


class ProjetoDetail(DetailResource):
    resource_path = 'projeto'
    query_class = ProjetoQuery
    pronac = property(lambda self: self.args['PRONAC'])

    def hal_links(self, result):
        url_id = encrypt(result['cgccpf'])
        print(self.args)
        pronac = self.pronac
        return {
            'self': self.url('/projetos/' + pronac),
            'proponente': self.url('/proponentes/%s' % url_id),
            'incentivadores': self.url('/incentivadores/?pronac=' + pronac),
            'fornecedores': self.url('/fornecedores/?pronac=' + pronac),
        }

    def hal_embedded(self, data):
        fields = [
            'captacoes', 'certidoes_negativas', 'deslocamento', 'distribuicao',
            'divulgacao', 'documentos_anexados', 'marcas_anexadas',
            'prorrogacao', 'readequacoes', 'relacao_bens_captal',
            'relatorio_fisco', 'relacao_pagamentos']
        return {field: data.pop(field) for field in fields}

    def hal_embedded_links(self, data):
        return {
            # 'captacoes':
            #     self.links_captacoes(data['captacoes'], PRONAC),
            # 'relacao_pagamentos':
            #     self.links_produtos(data['relacao_pagamentos'], PRONAC),
        }

    def links_captacoes(self, captacoes, pronac):
        links = []
        for captacao in captacoes:
            url = '/incentivadores/%s' % encrypt(captacao['cgccpf'])
            links.append({
                'projeto': self.url('/projetos/%s' % pronac),
                'incentivador': self.url(url),
            })
        return links

    def links_produtos(self, produtos, pronac):
        links = []
        for produto in produtos:
            cgccpf_id = encrypt(produto['cgccpf'])
            links.append({
                'projeto': self.url('projetos/%s' % pronac),
                'fornecedor': self.url('/fornecedores/%s' % cgccpf_id),
            })
        return links

    def check_pronac(self, pronac):
        try:
            int(pronac)
        except ValueError:
            result = {
                'message': 'PRONAC must be an integer',
                'message_code': 10
            }
            raise InvalidResult(result, status_code=405)

    def prepare_result(self, result):
        result.pop('IdPRONAC')

        # Sanitizing text values
        sanitize_fields = (
            'acessibilidade', 'objetivos', 'justificativa', 'etapa',
            'ficha_tecnica', 'impacto_ambiental', 'especificacao_tecnica',
            'estrategia_execucao', 'providencia', 'democratizacao',
            'sinopse',
            'resumo',
        )
        for field in sanitize_fields:
            result[field] = sanitize(result[field], truncated=False)

        # Clean cgccpf
        result['cgccpf'] = result['cgccpf'] or '00000000000000'
        result["cgccpf"] = remove_blanks(str(result["cgccpf"]))
        result['cgccpf'] = cgccpf_mask(result['cgccpf'])

        for section in ['captacoes', 'relacao_pagamentos']:
            for item in result.get(section, ()):
                item['cgccpf'] = cgccpf_mask(item['cgccpf'])

    def insert_related(self, projeto):
        pronac = self.pronac

        # Certidões
        certidoes_negativas = CertidoesNegativasQuery().query(pronac)
        projeto['certidoes_negativas'] = listify_queryset(certidoes_negativas)

        # Documentos anexados
        documentos = ProjetoQuery().attached_documents(pronac)
        projeto['documentos_anexados'] = self.cleaned_documentos(documentos)

        # Marcas anexadas
        marcas = ProjetoQuery().attached_brands(pronac)
        projeto['marcas_anexadas'] = marcas = listify_queryset(marcas)
        for marca in marcas:
            marca['link'] = utils.build_brand_link(marca)

        # Divulgação
        divulgacao = DivulgacaoQuery().query(pronac)
        projeto['divulgacao'] = listify_queryset(divulgacao)

        # Deslocamentos
        deslocamentos = DescolamentoQuery().query(pronac)
        projeto['deslocamento'] = self.cleaned_deslocamentos(deslocamentos)

        # Distribuições
        distribuicoes = DistribuicaoQuery().query(pronac)
        projeto['distribuicao'] = self.cleaned_distribuicoes(distribuicoes)

        # Readequações
        readequacoes = ReadequacaoQuery().query(pronac)
        projeto['readequacoes'] = self.cleaned_readequacoes(readequacoes)

        # Prorrogação
        prorrogacao = ProjetoQuery().postpone_request(pronac)
        projeto['prorrogacao'] = listify_queryset(prorrogacao)

        # Relação de pagamentos
        pagamentos = ProjetoQuery().payments_listing(idPronac=pronac)
        projeto['relacao_pagamentos'] = listify_queryset(pagamentos)

        # Relatório fisco
        relatorio_fisco = ProjetoQuery().taxing_report(pronac)
        projeto['relatorio_fisco'] = listify_queryset(relatorio_fisco)

        # Relação de bens de capital
        capital_goods = ProjetoQuery().goods_capital_listing(pronac)
        projeto['relacao_bens_captal'] = listify_queryset(capital_goods)

        # Captações
        captacoes = CaptacaoQuery().query(PRONAC=pronac)
        projeto['captacoes'] = listify_queryset(captacoes)

    # FIXME: @current_app.cache.cached(timeout=current_app.config['GLOBAL_CACHE_TIMEOUT'])
    # def get(self, PRONAC):
    #     return super().get(PRONAC=PRONAC)

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
