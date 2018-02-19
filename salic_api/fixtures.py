import contextlib
from datetime import datetime

from .database.connector import get_session, get_engine
from .resources.shared_models import *


#
# Populate a test db
#
def make_tables(*, app=None, driver=None, session=None):
    """
    Create tables from schema.
    """
    if session is None:
        session = get_session(driver=driver, app=app)

    # Create tables
    Projeto.metadata.create_all(session.bind)
    session.commit()


def clear_tables():
    """
    Clear all data in tables for the current session.

    Works only with the "memory" connector used in tests.
    """
    meta = Projeto.metadata

    with contextlib.closing(get_engine('memory').connect()) as con:
        trans = con.begin()

        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def populate(*, session=None, app=None, driver=None):
    """
    Populate database with some examples.
    """

    if session is None:
        session = get_session(driver=driver, app=app)

    # Create entities
    for factory in FACTORIES:
        for obj in factory():
            session.add(obj)
    session.commit()


#
# Global constants
#
CPF = '1234'


#
# Example objects
#
def areas_example():
    return [
        Area(Codigo='1', Descricao='Artes Cênicas'),
        Area(Codigo='2', Descricao='Audiovisual'),
        Area(Codigo='3', Descricao='Música'),
    ]


# PRONAC = column_property(AnoProjeto + Sequencial)
def projeto_example():
    return [Projeto(
        IdPRONAC=20001234,
        AnoProjeto='2000',
        Sequencial='1234',
        NomeProjeto='Test',
        Localizacao='Brazil',
        DtInicioExecucao=datetime(2000, 1, 1),
        DtFimExecucao=datetime(2000, 2, 1),
        UfProjeto='DF',
        SolicitadoReal='R$1.000.000',
        SolicitadoUfir='R$1.000.000',
        SolicitadoCusteioUfir='R$1.000.000',
        SolicitadoCusteioReal='R$1.000.000',
        SolicitadoCapitalUfir='R$1.000.000',
        SolicitadoCapitalReal='R$1.000.000',
        ResumoProjeto='abstract',
        ProvidenciaTomada='nenhuma',
        Segmento='11',
        Situacao='1',
        Area='1',
        CgcCpf=CPF,
        idProjeto=1,
        Mecanismo='1',
    )]


def pre_projeto_example():
    return [PreProjeto(
        idPreProjeto=1,
        NomeProjeto='Test',
        DtInicioDeExecucao=datetime(2000, 1, 1),
        DtFinalDeExecucao=datetime(2000, 2, 1),
        dtAceite=datetime(2000, 1, 1),
        DtArquivamento=datetime(2000, 3, 1),
        Mecanismo=1,
        Objetivos='cultural',
        Justificativa='Justificativa',
        Acessibilidade='Acessibilidade',
        DemocratizacaoDeAcesso='DemocratizacaoDeAcesso',
        EtapaDeTrabalho='EtapaDeTrabalho',
        FichaTecnica='FichaTecnica',
        ResumoDoProjeto='ResumoDoProjeto',
        Sinopse='Sinopse',
        ImpactoAmbiental='ImpactoAmbiental',
        EspecificacaoTecnica='EspecificacaoTecnica',
        EstrategiadeExecucao='EstrategiadeExecucao',
    )]


def segmento_example():
    return [
        Segmento(Codigo='11', Descricao='Teatro', tpEnquadramento='2'),
        Segmento(Codigo='21', Descricao='Jogos Eletrônicos',
                 tpEnquadramento='1'),
    ]


def enquadramento_example():
    return [
        Enquadramento(
            Enquadramento=1,
            AnoProjeto='2000',
            Sequencial='1234',
            IdPRONAC=20001234,
        ),
    ]


def mecanismo_example():
    return [
        Mecanismo(Codigo='1', Descricao='Mecenato'),
        Mecanismo(Codigo='2', Descricao='FNC'),
    ]


def situacao_example():
    return [Situacao(Codigo='1', Descricao='Descricao')]


def interessado_example():
    return [Interessado(
        CgcCpf=CPF,
        Nome='Nome',
        Responsavel='Responsavel',
        Uf='Uf',
        Cidade='Cidade',
        tipoPessoa='2',  # Juridica
    )]


def captacao_example():
    return [Captacao(
        AnoProjeto='2000',
        Sequencial='1234',
        CaptacaoReal='CaptacaoReal',
        DtRecibo=datetime(2000, 1, 1),
        CgcCpfMecena=CPF,
    )]


def certidoes_negativas_example():
    return [CertidoesNegativas(
        AnoProjeto='2000',
        Sequencial='1234',
        DtEmissao=datetime(2000, 1, 1),
        DtValidade=datetime(2000, 3, 1),
        CodigoCertidao=1,
        cdSituacaoCertidao=1,
        CgcCpf=CPF,
    )]


def verificacao_example():
    return [Verificacao(idTipo=1, Descricao='Descricao', stEstado=True)]


def plano_divulgacao_example():
    return [PlanoDivulgacao(
        idPeca=1,
        idVeiculo=1,
        stPlanoDivulgacao=True,
        idProjeto=1,
    )]


def produto_example():
    return [Produto(
        Descricao='Um Produto',
        Area='Area',
        Sintese='Sintese',
        Idorgao=1,
        stEstado=True,
    )]


def plano_distribuicao_example():
    return [PlanoDistribuicao(
        idPlanoDistribuicao=1,
        idProjeto=1,
        idProduto=1,
        stPrincipal=True,
        Segmento='11',
        Area='1',
        idPosicaoDaLogo=1,
        PrecoUnitarioNormal='R$100',
        PrecoUnitarioPromocional='R$10',
        QtdeProduzida=0,
        QtdeProponente=0,
        QtdePatrocinador=0,
        QtdeOutros=0,
        QtdeVendaNormal=0,
        QtdeVendaPromocional=0,
        QtdeUnitarioNormal=0,
        QtdeUnitarioPromocional=0,
        stPlanoDistribuicaoProduto=False,
    )]


def custos_example():
    return [Custos(
        idCustos=1,
        IdPRONAC='20001234',
        idInteressado=CPF,
        valor_proposta=1000,
        valor_solicitado=1000,
        valor_aprovado=1000,
        valor_aprovado_convenio=1000,
        custo_projeto=1000,
        outras_fontes=0,
    )]


def tbcomprovantepagamentoxplanilhaaprovacao_example():
    return [tbComprovantePagamentoxPlanilhaAprovacao(
        idPlanilhaAprovacao=1,
        idComprovantePagamento=1,
        nrOcorrencia=15,
        DtEmissao = datetime(2000, 1, 1),
        dsItemDeCusto = 'Descricao item',
        dsMarca = 'Descricao marca',
        dsFabricante = 'Descricao fabricante',
        tpDocumento = 1,
        vlComprovado = 2000.0,
    )]


def tbcomprovantepagamento_example():
    return [tbComprovantePagamento(
        idComprovantePagamento=1,
        idFornecedor=1,
        idArquivo=1,
        tpFormaDePagamento='Dinheiro',
        nrComprovante='1',
        nrDocumentoDePagamento='1',
        vlComprovacao=3.1415,
        DtPagamento=datetime(2000, 2, 2),
        dtEmissao = datetime(2000, 1, 1),
        dsJustificativa = 'Descricao Justificativa',
    )]


def tbarquivo_example():
    return [tbArquivo(
        idArquivo=1,
        nmArquivo='1',
    )]


def tbplanilhaaprovacao_example():
    return [tbPlanilhaAprovacao(
        idPlanilhaAprovacao=1,
        idPlanilhaItem=1,
    )]


def tbPlanilhaItens_example():
    return [tbPlanilhaItens(
        idPlanilhaItens=1,
        Descricao='Figurino',
    )]


def nomes_example():
    return [Nomes(
        idNome=1,
        idAgente=1,
        Descricao='Name',
    )]


def agentes_example():
    return [Agentes(
        idAgente=1,
        CNPJCPF=CPF,
    )]


def internet_example():
    return [Internet(
        idInternet=1,
        idAgente=1,
        Descricao='email',
    )]


#
# Registe all factories
#
def arquivo_imagem_example():
    return [tbArquivoImagem(
        idArquivoImagem=1,
        idArquivo=1,
        imagem="This should be an image",
        dsDocumento="dsDocumento",
    )]


def documento_example():
    return [tbDocumento(
        idDocumento=1,
        idArquivo=1,
    )]


def documento_projeto_example():
    return[tbDocumentoProjeto(
        idDocumentoProjeto=1,
        idDocumento=1,
        idTipoDocumento=1,
        idPronac=20001234,
    )]


def pais_example():
    return [Pais(
        idPais=1,
        Descricao="Brasil",
    )]


def uf_example():
    return [uf(
        iduf=1,
        Descricao="Distrito Federal",
    )]


def municipio_example():
    return [Municipios(
        idMunicipioIBGE=1,
        Descricao="Cocais de Bambu",
    )]


def tbDeslocamento_example():
    return [tbDeslocamento(
        idDeslocamento=1,
        Qtde=2,
        idProjeto=1,
        idPaisOrigem=1,
        idUFOrigem=1,
        idMunicipioOrigem=1,
        idPaisDestino=1,
        idUFDestino=1,
        idMunicipioDestino=1,
    )]


def usuarios_example():
    return[Usuarios(
        usu_codigo=1,
        usu_nome='nome',
    )]


def prorrogacao_example():
    return[prorrogacao(
        idProrrogacao=1,
        Logon=1,
        DtPedido=datetime(2000, 1, 1),
        DtInicio=datetime(2000, 1, 1),
        DtFinal=datetime(2000, 3, 1),
        Observacao='Observacao',
        Atendimento='A',
        idPronac=20001234,
    )]


def tbPlanilhaEtapa_example():
    return[tbPlanilhaEtapa(
        idPlanilhaEtapa=1,
        Descricao='Planilha Etapa',
    )]


def tbPlanilhaUnidade_example():
    return[tbPlanilhaUnidade(
        idUnidade=1,
        Descricao='Planilha Unidade',
    )]


def tbItemCusto_example():
    return [tbItemCusto(
        idItem = 1,
        idPlanilhaAprovacao = 1,
    )]

FACTORIES = [
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
    tbPlanilhaUnidade_example, tbItemCusto_example,
]
