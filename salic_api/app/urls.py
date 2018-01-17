from flask import redirect
from flask_cors import CORS
from flask_restful import Api

from ..resources.api_doc.SwaggerDef import SwaggerDef
from ..resources.fornecedor.fornecedor_detail import FornecedorDetail
from ..resources.fornecedor.fornecedor_list import FornecedorList
from ..resources.fornecedor.produto import Produto
from ..resources.incentivador.doacao import Doacao
from ..resources.incentivador.incentivador_detail import IncentivadorDetail
from ..resources.incentivador.incentivador_list import IncentivadorList
from ..resources.preprojeto.pre_projeto_detail import PreProjetoDetail
from ..resources.preprojeto.pre_projeto_list import PreProjetoList
from ..resources.projeto.area import Area
from ..resources.projeto.captacao import Captacao
from ..resources.projeto.projeto_detail import ProjetoDetail
from ..resources.projeto.projeto_list import ProjetoList
from ..resources.projeto.segmento import Segmento
from ..resources.proponente.proponente_detail import ProponenteDetail
from ..resources.proponente.proponente_list import ProponenteList
from ..resources.test_resource import TestResource


def make_urls(app=None):
    if app is None:
        from flask import current_app as app

    api = Api(app)
    #cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    base_version = app.config['BASE_VERSION']

    api.add_resource(TestResource, '/test', '/test/')

    api.add_resource(ProjetoDetail, '/%s/projetos/<string:PRONAC>/' %
                     (base_version))
    api.add_resource(ProjetoList, '/%s/projetos/' % (base_version))

    api.add_resource(ProponenteList, '/%s/proponentes/' % (base_version))
    api.add_resource(ProponenteDetail,
                     '/%s/proponentes/<string:proponente_id>/' % (base_version))

    api.add_resource(
        Captacao, '/%s/projetos/<string:PRONAC>/captacoes/' % (base_version))

    url = '/%s/projetos/areas' % base_version
    api.add_resource(Area, url, url + '/')
    api.add_resource(Segmento, '/%s/projetos/segmentos/' % (base_version))

    api.add_resource(PreProjetoList, '/%s/propostas/' % (base_version))
    api.add_resource(PreProjetoDetail, '/%s/propostas/<string:id>/' %
                     (base_version))

    api.add_resource(IncentivadorList, '/%s/incentivadores/' % (base_version))
    api.add_resource(IncentivadorDetail,
                     '/%s/incentivadores/<string:incentivador_id>/' % (
                         base_version))
    api.add_resource(
        Doacao,
        '/%s/incentivadores/<string:incentivador_id>/doacoes/' % (base_version))

    api.add_resource(FornecedorList, '/%s/fornecedores/' % (base_version))
    api.add_resource(FornecedorDetail,
                     '/%s/fornecedores/<string:fornecedor_id>/' % (
                         base_version))
    api.add_resource(
        Produto,
        '/%s/fornecedores/<string:fornecedor_id>/produtos/' % (base_version))

    api.add_resource(SwaggerDef, '/%s/swagger-def/' % (base_version))

    @app.route('/')
    def documentation():
        return redirect("/doc", code=302)
