# coding=utf-8
from .fixtures import FACTORIES
from salic_api.fixtures.bdcorporativo import tbcomprovantepagamentoxplanilhaaprovacao_example, \
    tbcomprovantepagamento_example, arquivo_imagem_example, documento_example, documento_projeto_example, \
    tbItemCusto_example
from .agentes import nomes_example, agentes_example, internet_example, pais_example, uf_example, municipio_example, \
    tbDeslocamento_example
from .base import prorrogacao_example
from .fake import custos_example
from .fixtures import populate, make_tables, clear_tables, FACTORIES
from salic_api.fixtures import tbcomprovantepagamentoxplanilhaaprovacao_example, tbcomprovantepagamento_example, \
    arquivo_imagem_example, documento_example, documento_projeto_example, tbItemCusto_example
from .sac import areas_example, projeto_example, pre_projeto_example, segmento_example, enquadramento_example, \
    mecanismo_example, situacao_example, interessado_example, captacao_example, certidoes_negativas_example, \
    verificacao_example, plano_divulgacao_example, produto_example, plano_distribuicao_example, tbarquivo_example, \
    tbplanilhaaprovacao_example, tbPlanilhaEtapa_example, tbPlanilhaItens_example, tbPlanilhaUnidade_example, \
    readequacao_example, tipo_readequacao_example, tipo_encaminhamento_example

from .tabelas import usuarios_example

FACTORIES.extend([
    areas_example, projeto_example, pre_projeto_example, segmento_example,
    enquadramento_example, mecanismo_example, situacao_example,
    interessado_example, captacao_example, certidoes_negativas_example,
    verificacao_example, plano_divulgacao_example, produto_example,
    plano_distribuicao_example, custos_example,
    tbcomprovantepagamentoxplanilhaaprovacao_example,
    tbcomprovantepagamento_example, tbarquivo_example,
    tbplanilhaaprovacao_example, tbPlanilhaItens_example,
    nomes_example, agentes_example, internet_example,
    arquivo_imagem_example, documento_example, documento_projeto_example,
    pais_example, uf_example, municipio_example, tbDeslocamento_example,
    usuarios_example, prorrogacao_example, tbPlanilhaEtapa_example,
    tbPlanilhaUnidade_example, tbItemCusto_example,readequacao_example,
    tipo_encaminhamento_example, tipo_readequacao_example
])
