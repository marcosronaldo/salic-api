from datetime import datetime

from salic_api.models import ComprovantePagamentoxPlanilhaAprovacao, ComprovantePagamento, ArquivoImagem, Documento, \
    DocumentoProjeto, ItemCusto


def tbcomprovantepagamentoxplanilhaaprovacao_example():
    return [ComprovantePagamentoxPlanilhaAprovacao(
        idPlanilhaAprovacao=1,
        idComprovantePagamento=1,
        nrOcorrencia=15,
        DtEmissao=datetime(2000, 1, 1),
        dsItemDeCusto='Descricao item',
        dsMarca='Descricao marca',
        dsFabricante='Descricao fabricante',
        tpDocumento=1,
        vlComprovado=2000.0,
    )]


def tbcomprovantepagamento_example():
    return [ComprovantePagamento(
        idComprovantePagamento=1,
        idFornecedor=1,
        idArquivo=1,
        tpFormaDePagamento='Dinheiro',
        nrComprovante='1',
        nrDocumentoDePagamento='1',
        vlComprovacao=3.1415,
        DtPagamento=datetime(2000, 2, 2),
        dtEmissao=datetime(2000, 1, 1),
        dsJustificativa='Descricao Justificativa',
    )]


def arquivo_imagem_example():
    return [ArquivoImagem(
        idArquivoImagem=1,
        idArquivo=1,
        imagem="This should be an image",
        dsDocumento="dsDocumento",
    )]


def documento_example():
    return [Documento(
        idDocumento=1,
        idArquivo=1,
    )]


def documento_projeto_example():
    return [DocumentoProjeto(
        idDocumentoProjeto=1,
        idDocumento=1,
        idTipoDocumento=1,
        idPronac=20001234,
    )]


def tbItemCusto_example():
    return [ItemCusto(
        idItem=1,
        idPlanilhaAprovacao=1,
    )]
