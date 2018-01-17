from sqlalchemy import Column, Date, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy.orm import relationship

Base = declarative_base()


class Projeto(Base):
    __tablename__ = 'Projetos'

    IdPRONAC = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    NomeProjeto = Column(String)
    Localizacao = Column(String)
    DtInicioExecucao = Column(Date)
    DtFimExecucao = Column(Date)
    UfProjeto = Column(String)
    SolicitadoReal = Column(String)
    SolicitadoUfir = Column(String)
    SolicitadoCusteioUfir = Column(String)
    SolicitadoCusteioReal = Column(String)
    SolicitadoCapitalUfir = Column(String)
    SolicitadoCapitalReal = Column(String)
    ResumoProjeto = Column(Text)
    ProvidenciaTomada = Column(String)
    Segmento = Column(String, ForeignKey("Segmento.Codigo"))
    Segmento_related = relationship("Segmento", foreign_keys=[Segmento])
    Situacao = Column(String, ForeignKey("Situacao.Codigo"))
    Situacao_related = relationship("Situacao", foreign_keys=[Situacao])
    Area = Column(String, ForeignKey("Area.Codigo"))
    Area_related = relationship("Area", foreign_keys=[Area])
    CgcCpf = Column(String, ForeignKey("Interessado.CgcCpf"))
    Interessado_related = relationship("Interessado",
                                       foreign_keys=[CgcCpf])
    idProjeto = Column(Integer, ForeignKey("PreProjeto.idPreProjeto"))
    preprojeto_related = relationship("PreProjeto",
                                      foreign_keys=[idProjeto])
    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
    mecanismo_related = relationship(
        "Mecanismo", foreign_keys=[Mecanismo])


class PreProjeto(Base):
    __tablename__ = 'PreProjeto'

    idPreProjeto = Column(Integer, primary_key=True)
    NomeProjeto = Column(String)
    DtInicioDeExecucao = Column(Date)
    DtFinalDeExecucao = Column(Date)
    dtAceite = Column(Date)
    DtArquivamento = Column(Date)
    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])
    Objetivos = Column(String)
    Justificativa = Column(String)
    Acessibilidade = Column(String)
    DemocratizacaoDeAcesso = Column(String)
    EtapaDeTrabalho = Column(String)
    FichaTecnica = Column(String)
    ResumoDoProjeto = Column(String)
    Sinopse = Column(String)
    ImpactoAmbiental = Column(String)
    EspecificacaoTecnica = Column(String)
    EstrategiadeExecucao = Column(String)


class Segmento(Base):
    __tablename__ = 'Segmento'

    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)

    def __init__(self):
        pass


class Enquadramento(Base):
    __tablename__ = 'Enquadramento'

    IdEnquadramento = Column(Integer, primary_key=True)
    Enquadramento = Column(Integer)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    IdPRONAC = Column(Integer, ForeignKey('Projetos.IdPRONAC'))


class Mecanismo(Base):
    __tablename__ = 'Mecanismo'

    Codigo = Column(Integer, primary_key=True)
    Descricao = Column(String)


class Situacao(Base):
    __tablename__ = 'Situacao'

    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)


class Area(Base):
    __tablename__ = 'Area'

    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)


class Interessado(Base):
    __tablename__ = 'Interessado'

    CgcCpf = Column(String, primary_key=True)
    Nome = Column(String)
    Responsavel = Column(String)
    Uf = Column(String)
    Cidade = Column(String)
    tipoPessoa = Column(String)
    captacao_related = relationship(
        'Captacao',
        primaryjoin='Interessado.CgcCpf==Captacao.CgcCpfMecena')
    projeto_related = relationship(
        'Projeto',
        primaryjoin='Interessado.CgcCpf==Projeto.CgcCpf')


class Captacao(Base):
    __tablename__ = 'Captacao'

    Idcaptacao = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    CaptacaoReal = Column(String)
    DtRecibo = Column(Date)
    CgcCpfMecena = Column(String, ForeignKey('Interessado.CgcCpf'))
    interessado_related = relationship('Interessado',
                                       foreign_keys=[CgcCpfMecena])
    # projeto_related = relationship('Projeto', primaryjoin='Captacao.PRONAC==Projeto.PRONAC')


class CertidoesNegativas(Base):
    __tablename__ = 'CertidoesNegativas'

    idCertidoesNegativas = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    DtEmissao = Column(Date)
    DtValidade = Column(Date)
    CodigoCertidao = Column(Integer)
    cdSituacaoCertidao = Column(Integer)
    CgcCpf = Column(String)


class Verificacao(Base):
    __tablename__ = 'Verificacao'

    idVerificacao = Column(Integer, primary_key=True)
    idTipo = Column(Integer)
    Descricao = Column(String)
    stEstado = Column(Integer)


class PlanoDivulgacao(Base):
    __tablename__ = 'PlanoDeDivulgacao'

    idPlanoDivulgacao = Column(Integer, primary_key=True)
    idPeca = Column(Integer)
    idVeiculo = Column(Integer)
    stPlanoDivulgacao = Column(Integer)

    idProjeto = Column(Integer, ForeignKey('Projetos.idProjeto'))
    projeto_related = relationship('Projeto', foreign_keys=[idProjeto])


class Produto(Base):
    __tablename__ = 'Produto'

    Codigo = Column(Integer, primary_key=True)
    Descricao = Column(String)
    Area = Column(String)
    Sintese = Column(String)
    Idorgao = Column(Integer)
    stEstado = Column(Integer)


class PlanoDistribuicao(Base):
    __tablename__ = 'PlanoDistribuicaoProduto'

    idPlanoDistribuicao = Column(Integer, primary_key=True)
    idProjeto = Column(Integer, ForeignKey('Projetos.idProjeto'))
    projeto_related = relationship('Projeto', foreign_keys=[idProjeto])
    idProduto = Column(Integer, ForeignKey('Produto.Codigo'))
    produto_related = relationship('Produto', foreign_keys=[idProduto])
    stPrincipal = Column(Integer)
    Segmento = Column(String, ForeignKey('Segmento.Codigo'))
    segmento_related = relationship('Segmento', foreign_keys=[Segmento])
    Area = Column(String, ForeignKey('Area.Codigo'))
    area_related = relationship('Area', foreign_keys=[Area])
    idPosicaoDaLogo = Column(Integer, ForeignKey('Verificacao.idVerificacao'))
    vetificacao_related = relationship('Verificacao',
                                       foreign_keys=[idPosicaoDaLogo])
    PrecoUnitarioNormal = Column(String)
    PrecoUnitarioPromocional = Column(String)
    QtdeProduzida = Column(Integer)
    QtdeProponente = Column(Integer)
    QtdePatrocinador = Column(Integer)
    QtdeOutros = Column(Integer)
    QtdeVendaNormal = Column(Integer)
    QtdeVendaPromocional = Column(Integer)
    QtdeUnitarioNormal = Column(Integer)
    QtdeUnitarioPromocional = Column(Integer)
    stPlanoDistribuicaoProduto = Column(Integer)
