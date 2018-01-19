from flask import current_app

from salic_api.resources.resource_base import InvalidResult
from . import utils
from .models import (
    ProjetoModelObject, CertidoesNegativasModelObject,
    DivulgacaoModelObject, DescolamentoModelObject,
    DistribuicaoModelObject, ReadequacaoModelObject,
    CaptacaoQuery
)
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import ListResource
from ..sanitization import sanitize
from ..serialization import listify_queryset
from ...app.security import encrypt
from ...utils.log import Log


class ProjetoDetail(ListResource):
    resource_path = 'projeto'
    query_class = ProjetoModelObject

    def build_links(self, args={}):

        self.links["self"] += args['PRONAC']

        url_id = encrypt(args['proponente_id'])
        proponente_link = current_app.config['API_ROOT_URL'] + \
                          'proponentes/%s' % url_id

        incentivadores_link = current_app.config['API_ROOT_URL'] + \
                              'incentivadores/?PRONAC=' + args['PRONAC']
        fornecedores_link = current_app.config['API_ROOT_URL'] + \
                            'fornecedores/?PRONAC=' + args['PRONAC']

        self.links["proponente"] = proponente_link
        self.links["incentivadores"] = incentivadores_link
        self.links["fornecedores"] = fornecedores_link

        self.captacoes_links = []

        for captacao in args['captacoes']:
            captacao_links = {}
            captacao_links['projeto'] = current_app.config['API_ROOT_URL'] + \
                                        'projetos/%s' % args['PRONAC']
            url_id = encrypt(captacao['cgccpf'])
            captacao_links['incentivador'] = current_app.config[
                                                 'API_ROOT_URL'] + \
                                             'incentivadores/%s' % url_id

            self.captacoes_links.append(captacao_links)

        self.produtos_links = []

        for produto in args['produtos']:
            produto_links = {}
            # TODO - Alterar a API para tratar de agentes sem cgccpf, agentes extrangeiros
            if produto['cgccpf'] == None:
                produto['cgccpf'] = '00000000000000'
            fornecedor_id = encrypt(produto['cgccpf'])
            produto_links['projeto'] = current_app.config['API_ROOT_URL'] + \
                                       'projetos/%s' % args['PRONAC']
            produto_links['fornecedor'] = current_app.config['API_ROOT_URL'] + \
                                          'fornecedores/%s' % fornecedor_id

            self.produtos_links.append(produto_links)

    def __init__(self):
        super().__init__()
        self.links = {'self': self.url('projetos/')}

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

    def check_pronac(self, PRONAC):
        try:
            int(PRONAC)
        except ValueError:
            result = {
                'message': 'PRONAC must be an integer',
                'message_code': 10
            }
            raise InvalidResult(result, status_code=405)

    def fetch_result(self, PRONAC):
        result, n_records = ProjetoModelObject() \
            .all(limit=1, offset=0, PRONAC=PRONAC)
        if n_records == 0:
            raise InvalidResult({
                'message': 'No project with PRONAC %s' % PRONAC,
                'message_code': 11
            }, 404)
        return result

    def fetch_related(self, result, PRONAC):
        pass

    # FIXME: @current_app.cache.cached(timeout=current_app.config['GLOBAL_CACHE_TIMEOUT'])
    def get(self, PRONAC):
        try:
            return self._get_worker(PRONAC)
        except InvalidResult as ex:
            return ex.render(self)

    def _get_worker(self, PRONAC):
        self.check_pronac(PRONAC)
        result = self.fetch_result(PRONAC)
        projeto = listify_queryset(result)[0]
        Log.debug('IdPRONAC = %s' % str(projeto['IdPRONAC']))

        try:
            certidoes_negativas = CertidoesNegativasModelObject().all(projeto['PRONAC'])
        except Exception as e:
            Log.error(
                'Database error trying to fetch \"certidoes_negativas data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        projeto['certidoes_negativas'] = listify_queryset(certidoes_negativas)
        try:
            documentos_anexados = ProjetoModelObject() \
                .attached_documents(projeto['IdPRONAC'])
        except Exception as e:
            Log.error(
                'Database error trying to fetch \"documentos_anexados data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        documentos_anexados = listify_queryset(documentos_anexados)
        projeto['documentos_anexados'] = self.cleaned_documentos(
            documentos_anexados)

        try:
            marcas_anexadas = ProjetoModelObject(
            ).attached_brands(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"marcas_anexadas data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
                'more': 'something is broken'
            }
            return self.render(result, status_code=503)

        marcas_anexadas = listify_queryset(marcas_anexadas)

        for marca in marcas_anexadas:
            marca['link'] = utils.build_brand_link(marca)

        projeto['marcas_anexadas'] = marcas_anexadas

        try:
            divulgacao = DivulgacaoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"divulgacao data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
                'more': 'something is broken'
            }
            return self.render(result, status_code=503)

        projeto['divulgacao'] = listify_queryset(divulgacao)

        try:
            deslocamentos = DescolamentoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"deslocamentos data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        deslocamentos = listify_queryset(deslocamentos)
        projeto['deslocamento'] = self.cleaned_deslocamentos(deslocamentos)

        try:
            distribuicoes = DistribuicaoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"distribuicoes data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        distribuicoes = listify_queryset(distribuicoes)
        projeto['distribuicao'] = self.cleaned_distribuicoes(distribuicoes)

        try:
            readequacoes = ReadequacaoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"readequacoes data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        readequacoes = listify_queryset(readequacoes)
        projeto['readequacoes'] = self.cleaned_readequacoes(readequacoes)

        try:
            prorrogacao = ProjetoModelObject().postpone_request(
                projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"prorrogacao data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        prorrogacao = listify_queryset(prorrogacao)
        projeto['prorrogacao'] = prorrogacao

        try:
            relacao_pagamentos = ProjetoModelObject().payments_listing(
                idPronac=projeto['IdPRONAC'])
        except Exception as e:
            Log.error(
                'Database error trying to fetch \"relacao pagamentos data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        relacao_pagamentos = listify_queryset(relacao_pagamentos)
        projeto['relacao_pagamentos'] = relacao_pagamentos

        try:
            relatorio_fisco = ProjetoModelObject(
            ).taxing_report(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"relatorio fisco data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        relatorio_fisco = listify_queryset(relatorio_fisco)
        projeto['relatorio_fisco'] = relatorio_fisco

        try:
            relacao_bens_captal = ProjetoModelObject(
            ).goods_capital_listing(projeto['IdPRONAC'])
        except Exception as e:
            Log.error(
                'Database error trying to fetch \"relacao bens captal pagamentos data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        relacao_bens_captal = listify_queryset(relacao_bens_captal)
        projeto['relacao_bens_captal'] = relacao_bens_captal

        try:
            captacoes = CaptacaoQuery().all(PRONAC=PRONAC)
        except Exception as e:
            Log.error('Database error trying to fetch \"captacoes data\"')
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        captacoes = listify_queryset(captacoes)
        projeto['captacoes'] = captacoes

        # Sanitizing text values
        sanitize_fields = (
            'acessibilidade', 'objetivos', 'justificativa', 'etapa',
            'ficha_tecnica', 'impacto_ambiental', 'especificacao_tecnica',
            'estrategia_execucao', 'providencia', 'democratizacao', 'sinopse',
            'resumo',
        )
        for field in sanitize_fields:
            projeto[field] = sanitize(projeto[field], truncated=False)

        # Removing IdPRONAC
        del projeto['IdPRONAC']

        self.build_links(args={
            'PRONAC': projeto['PRONAC'], 'proponente_id': projeto['cgccpf'],
            'captacoes': projeto['captacoes'], 'produtos': relacao_pagamentos
        })

        self.clean_cgcpf(projeto)
        return self.render(projeto)

    def cleaned_documentos(self, documentos_anexados):
        cleaned = []
        for documento in documentos_anexados:
            link = utils.build_file_link(documento)
            if link == '':
                continue
            sanitized_doc = {}
            sanitized_doc['link'] = link
            sanitized_doc['classificacao'] = documento['Descricao']
            sanitized_doc['data'] = documento['Data']
            sanitized_doc['nome'] = documento['NoArquivo']
            cleaned.append(sanitized_doc)

        return cleaned

    def cleaned_deslocamentos(self, deslocamentos):
        clean = []
        for deslocamento in deslocamentos:
            clean_elem = {}
            clean_elem['pais_origem'] = deslocamento['PaisOrigem']
            clean_elem['pais_destino'] = deslocamento['PaisDestino']
            clean_elem['uf_origem'] = deslocamento['UFOrigem']
            clean_elem['uf_destino'] = deslocamento['UFDestino']
            clean_elem['municipio_origem'] = deslocamento['MunicipioOrigem']
            clean_elem['municipio_destino'] = deslocamento['MunicipioDestino']
            clean_elem['quantidade'] = deslocamento['Qtde']
            clean.append(clean_elem)
        return clean

    def cleaned_readequacoes(self, readequacoes):
        for readequacao in readequacoes:
            readequacao['descricao_justificativa'] = sanitize(
                readequacao['descricao_justificativa'], truncated=False)
            readequacao['descricao_avaliacao'] = sanitize(
                readequacao['descricao_avaliacao'], truncated=False)
            readequacao['descricao_solicitacao'] = sanitize(
                readequacao['descricao_solicitacao'], truncated=False)
        return readequacoes

    def cleaned_distribuicoes(self, distribuicoes):
        distribuicoes_satitized = []
        key_map = {
            'area': 'area',
            'segmento': 'segmento',
            'produto': 'produto',
            'posicao_logo': 'posicao_logo',
            'qtd_outros': 'QtdeOutros',
            'qtd_proponente': 'QtdeProponente',
            'qtd_produzida': 'QtdeProduzida',
            'qtd_patrocinador': 'QtdePatrocinador',
            'qtd_venda_normal': 'QtdeVendaNormal',
            'qtd_venda_promocional': 'QtdeVendaPromocional',
            'preco_unitario_normal': 'PrecoUnitarioNormal',
            'preco_unitario_promocional': 'PrecoUnitarioPromocional',
            'localizacao': 'Localizacao',
        }

        for distribuicao in distribuicoes:
            clean = {
                k: distribuicao[key_map[v]] for k, v in key_map.items()
            }
            qtd_venda = clean['qtd_venda_normal']
            qtd_promo = clean['qtd_venda_promocional']
            preco = clean['preco_unitario_normal']
            preco_promo = clean['preco_unitario_promocional']

            clean['receita_normal'] = qtd_venda * preco
            clean['receita_pro'] = qtd_promo * preco
            clean['receita_prevista'] = qtd_venda * preco + \
                                        qtd_promo * preco_promo
            distribuicoes_satitized.append(clean)
        return distribuicoes_satitized

    def clean_cgcpf(self, projeto):
        projeto["cgccpf"] = remove_blanks(str(projeto["cgccpf"]))
        projeto['cgccpf'] = cgccpf_mask(projeto['cgccpf'])

        for captacao in projeto['captacoes']:
            captacao['cgccpf'] = cgccpf_mask(captacao['cgccpf'])
        for produto in projeto['relacao_pagamentos']:
            produto['cgccpf'] = cgccpf_mask(produto['cgccpf'])
