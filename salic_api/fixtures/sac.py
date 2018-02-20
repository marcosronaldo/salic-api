from datetime import datetime

from salic_api.models import Area, Arquivo, Projeto, PreProjeto, Segmento, Enquadramento, Mecanismo, Situacao, Interessado, \
    Captacao, CertidoesNegativas, Verificacao, PlanoDivulgacao, Produto, PlanoDistribuicao, PlanilhaAprovacao, \
    PlanilhaItens, PlanilhaEtapa, PlanilhaUnidade

#
# Global constants
#
CPF = '1234'


def areas_example():
    return [
        Area(Codigo='1', Descricao='Artes Cênicas'),
        Area(Codigo='2', Descricao='Audiovisual'),
        Area(Codigo='3', Descricao='Música'),
    ]


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


def tbarquivo_example():
    return [Arquivo(
        idArquivo=1,
        nmArquivo='1',
    )]


def tbplanilhaaprovacao_example():
    return [PlanilhaAprovacao(
        idPlanilhaAprovacao=1,
        idPlanilhaItem=1,
        qtItem=1,
    )]


def tbPlanilhaItens_example():
    return [PlanilhaItens(
        idPlanilhaItens=1,
        Descricao='Figurino',
    )]


def tbPlanilhaEtapa_example():
    return [PlanilhaEtapa(
        idPlanilhaEtapa=1,
        Descricao='Planilha Etapa',
    )]


def tbPlanilhaUnidade_example():
    return [PlanilhaUnidade(
        idUnidade=1,
        Descricao='Planilha Unidade',
    )]