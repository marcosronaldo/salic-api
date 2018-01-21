from datetime import date

from .database.connector import get_session
from .resources.shared_models import Area, Projeto, PreProjeto, \
    PlanoDistribuicao, Produto, PlanoDivulgacao, Verificacao, Segmento, \
    Enquadramento, Mecanismo, Situacao, Interessado, Captacao, \
    CertidoesNegativas, Custos


#
# Populate a test db
#
def populate():
    """
    Populate database with some examples.
    """

    session = get_session('sqlite')

    # Create tables
    Projeto.metadata.create_all(session.bind)
    session.commit()

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
def projeto_exexample():
    return [Projeto(
        IdPRONAC=20001234,
        AnoProjeto='2000',
        Sequencial='1234',
        NomeProjeto='Test',
        Localizacao='Brazil',
        DtInicioExecucao=date(2000, 1, 1),
        DtFimExecucao=date(2000, 2, 1),
        UfProjeto='DF',
        SolicitadoReal='R$1.000.000',
        SolicitadoUfir='R$1.000.000',
        SolicitadoCusteioUfir='R$1.000.000',
        SolicitadoCusteioReal='R$1.000.000',
        SolicitadoCapitalUfir='R$1.000.000',
        SolicitadoCapitalReal='R$1.000.000',
        ResumoProjeto='abstract',
        ProvidenciaTomada='nenhuma',
        Segmento='1',
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
        DtInicioDeExecucao=date(2000, 1, 1),
        DtFinalDeExecucao=date(2000, 2, 1),
        dtAceite=date(2000, 1, 1),
        DtArquivamento=date(2000, 3, 1),
        Mecanismo='mecenato',
        Objetivos='cutural',
        Justificativa='Justificativa',
        Acessibilidade='Acessibilidade',
        DemocratizacaoDeAcesso='DemocratizacaoDeAcesso',
        EtapaDeTrabalho='EtapaDeTrabalho ',
        FichaTecnica='FichaTecnica ',
        ResumoDoProjeto='ResumoDoProjeto ',
        Sinopse='Sinopse ',
        ImpactoAmbiental='ImpactoAmbiental ',
        EspecificacaoTecnica='EspecificacaoTecnica ',
        EstrategiadeExecucao='EstrategiadeExecucao ',
    )]


def segmento_example():
    return [Segmento(Codigo='1', Descricao='Descricao')]


def enquadramento_example():
    return [Enquadramento(
        Enquadramento=1,
        AnoProjeto='2000',
        Sequencial='1234',
        IdPRONAC=20001234,
    )]


def mecanismo_example():
    return [Mecanismo(Descricao='Descricao')]


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
        DtRecibo=date(2000, 1, 1),
        CgcCpfMecena=CPF,
    )]


def certidoes_negativas_example():
    return [CertidoesNegativas(
        AnoProjeto='2000',
        Sequencial='1234',
        DtEmissao=date(2000, 1, 1),
        DtValidade=date(2000, 3, 1),
        CodigoCertidao=1,
        cdSituacaoCertidao=1,
        CgcCpf=CPF,
    )]


def verificacao_example():
    return [Verificacao(idTipo=1, Descricao='Descricao', stEstado=1)]


def plano_divulgacao_example():
    return [PlanoDivulgacao(
        idPeca=1,
        idVeiculo=1,
        stPlanoDivulgacao=1,
        idProjeto=1,
    )]


def produto_example():
    return [Produto(
        Descricao='Descricao',
        Area='Area',
        Sintese='Sintese',
        Idorgao=1,
        stEstado=1,
    )]


def plano_distribuicao_example():
    return [PlanoDistribuicao(
        idPlanoDistribuicao=1,
        idProjeto=1,
        idProduto=1,
        stPrincipal=1,
        Segmento='1',
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
        stPlanoDistribuicaoProduto=0,
    )]


def custos_example():
    return [Custos(
        idCustos=1,
        IdPRONAC=20001234,
        valor_proposta=1000,
        valor_solicitado=1000,
        valor_aprovado=1000,
        valor_aprovado_convenio=1000,
        custo_projeto=1000,
        outras_fontes=0,
    )]


#
# Registe all factories
#
FACTORIES = [
    areas_example, projeto_exexample, pre_projeto_example, segmento_example,
    enquadramento_example, mecanismo_example, situacao_example,
    interessado_example, captacao_example, certidoes_negativas_example,
    verificacao_example, plano_divulgacao_example, produto_example,
    plano_distribuicao_example, custos_example,
]
