from datetime import date

from .database.connector import get_session
from .resources.shared_models import Area, Projeto


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
    session.add(projeto_ex())
    for area in areas_ex():
        session.add(area)
    session.commit()


#
# Example objects
#
def areas_ex():
    return [
        Area(Codigo='1', Descricao='Artes Cênicas'),
        Area(Codigo='2', Descricao='Audiovisual'),
        Area(Codigo='3', Descricao='Música'),
    ]


def projeto_ex():
    return Projeto(
        IdPRONAC=123,
        AnoProjeto='2000',
        Sequencial='abc',
        NomeProjeto='Test project',
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
        CgcCpf='123.456.789-00',
        idProjeto=1,
        Mecanismo='1',
    )

# class PreProjeto(Base):
#     __tablename__ = 'PreProjeto'
#
#     idPreProjeto = Column(Integer, primary_key=True)
#     NomeProjeto = Column(String)
#     DtInicioDeExecucao = Column(Date)
#     DtFinalDeExecucao = Column(Date)
#     dtAceite = Column(Date)
#     DtArquivamento = Column(Date)
#     Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
#     mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])
#     Objetivos = Column(String)
#     Justificativa = Column(String)
#     Acessibilidade = Column(String)
#     DemocratizacaoDeAcesso = Column(String)
#     EtapaDeTrabalho = Column(String)
#     FichaTecnica = Column(String)
#     ResumoDoProjeto = Column(String)
#     Sinopse = Column(String)
#     ImpactoAmbiental = Column(String)
#     EspecificacaoTecnica = Column(String)
#     EstrategiadeExecucao = Column(String)
#
#     def __init__(self):
#         pass
#
#
# class Segmento(Base):
#     __tablename__ = 'Segmento'
#
#     Codigo = Column(String, primary_key=True)
#     Descricao = Column(String)
#
#     def __init__(self):
#         pass
#
#
# class Enquadramento(Base):
#     __tablename__ = 'Enquadramento'
#
#     IdEnquadramento = Column(Integer, primary_key=True)
#     Enquadramento = Column(Integer)
#     AnoProjeto = Column(String)
#     Sequencial = Column(String)
#     IdPRONAC = Column(Integer, ForeignKey('Projetos.IdPRONAC'))
#
#     def __init__(self):
#         pass
#
#
# class Mecanismo(Base):
#     __tablename__ = 'Mecanismo'
#
#     Codigo = Column(Integer, primary_key=True)
#     Descricao = Column(String)
#
#     def __init__(self):
#         pass
#
#
# class Situacao(Base):
#     __tablename__ = 'Situacao'
#
#     Codigo = Column(String, primary_key=True)
#     Descricao = Column(String)
#
#     def __init__(self):
#         pass
#
#
# class Area(Base):
#     __tablename__ = 'Area'
#
#     Codigo = Column(String, primary_key=True)
#     Descricao = Column(String)
#
#     def __init__(self):
#         pass
#
#
# class Interessado(Base):
#     __tablename__ = 'Interessado'
#
#     CgcCpf = Column(String, primary_key=True)
#     Nome = Column(String)
#     Responsavel = Column(String)
#     Uf = Column(String)
#     Cidade = Column(String)
#     tipoPessoa = Column(String)
#     captacao_related = relationship(
#         'Captacao',
#         primaryjoin='Interessado.CgcCpf==Captacao.CgcCpfMecena')
#     projeto_related = relationship(
#         'Projeto',
#         primaryjoin='Interessado.CgcCpf==Projeto.CgcCpf')
#
#     def __init__(self):
#         pass
#
#
# class Captacao(Base):
#     __tablename__ = 'Captacao'
#
#     Idcaptacao = Column(Integer, primary_key=True)
#     AnoProjeto = Column(String)
#     Sequencial = Column(String)
#     PRONAC = column_property(AnoProjeto + Sequencial)
#     CaptacaoReal = Column(String)
#     DtRecibo = Column(Date)
#     CgcCpfMecena = Column(String, ForeignKey('Interessado.CgcCpf'))
#     interessado_related = relationship('Interessado',
#                                        foreign_keys=[CgcCpfMecena])
#     # projeto_related = relationship('Projeto', primaryjoin='Captacao.PRONAC==Projeto.PRONAC')
#
#
# class CertidoesNegativas(Base):
#     __tablename__ = 'CertidoesNegativas'
#
#     idCertidoesNegativas = Column(Integer, primary_key=True)
#     AnoProjeto = Column(String)
#     Sequencial = Column(String)
#     PRONAC = column_property(AnoProjeto + Sequencial)
#     DtEmissao = Column(Date)
#     DtValidade = Column(Date)
#     CodigoCertidao = Column(Integer)
#     cdSituacaoCertidao = Column(Integer)
#     CgcCpf = Column(String)
#
#
# class Verificacao(Base):
#     __tablename__ = 'Verificacao'
#
#     idVerificacao = Column(Integer, primary_key=True)
#     idTipo = Column(Integer)
#     Descricao = Column(String)
#     stEstado = Column(Integer)
#
#
# class PlanoDivulgacao(Base):
#     __tablename__ = 'PlanoDeDivulgacao'
#
#     idPlanoDivulgacao = Column(Integer, primary_key=True)
#     idPeca = Column(Integer)
#     idVeiculo = Column(Integer)
#     stPlanoDivulgacao = Column(Integer)
#
#     idProjeto = Column(Integer, ForeignKey('Projetos.idProjeto'))
#     projeto_related = relationship('Projeto', foreign_keys=[idProjeto])
#
#
# class Produto(Base):
#     __tablename__ = 'Produto'
#
#     Codigo = Column(Integer, primary_key=True)
#     Descricao = Column(String)
#     Area = Column(String)
#     Sintese = Column(String)
#     Idorgao = Column(Integer)
#     stEstado = Column(Integer)
#
#
# class PlanoDistribuicao(Base):
#     __tablename__ = 'PlanoDistribuicaoProduto'
#
#     idPlanoDistribuicao = Column(Integer, primary_key=True)
#     idProjeto = Column(Integer, ForeignKey('Projetos.idProjeto'))
#     projeto_related = relationship('Projeto', foreign_keys=[idProjeto])
#     idProduto = Column(Integer, ForeignKey('Produto.Codigo'))
#     produto_related = relationship('Produto', foreign_keys=[idProduto])
#     stPrincipal = Column(Integer)
#     Segmento = Column(String, ForeignKey('Segmento.Codigo'))
#     segmento_related = relationship('Segmento', foreign_keys=[Segmento])
#     Area = Column(String, ForeignKey('Area.Codigo'))
#     area_related = relationship('Area', foreign_keys=[Area])
#     idPosicaoDaLogo = Column(Integer, ForeignKey('Verificacao.idVerificacao'))
#     vetificacao_related = relationship('Verificacao',
#                                        foreign_keys=[idPosicaoDaLogo])
#     PrecoUnitarioNormal = Column(String)
#     PrecoUnitarioPromocional = Column(String)
#     QtdeProduzida = Column(Integer)
#     QtdeProponente = Column(Integer)
#     QtdePatrocinador = Column(Integer)
#     QtdeOutros = Column(Integer)
#     QtdeVendaNormal = Column(Integer)
#     QtdeVendaPromocional = Column(Integer)
#     QtdeUnitarioNormal = Column(Integer)
#     QtdeUnitarioPromocional = Column(Integer)
#     stPlanoDistribuicaoProduto = Column(Integer)
