from sqlalchemy import Column, Date, Integer, String, ForeignKey, Text, case
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
    Situacao = Column(String, ForeignKey("Situacao.Codigo"))
    Area = Column(String, ForeignKey("Area.Codigo"))
    CgcCpf = Column(String, ForeignKey("Interessado.CgcCpf"))
    idProjeto = Column(Integer, ForeignKey("PreProjeto.idPreProjeto"))
    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))

    # Related fields
    Area_related = relationship("Area", foreign_keys=[Area])
    preprojeto_related = relationship("PreProjeto", foreign_keys=[idProjeto])
    Situacao_related = relationship("Situacao", foreign_keys=[Situacao])
    Interessado_related = relationship("Interessado", foreign_keys=[CgcCpf])
    Segmento_related = relationship("Segmento", foreign_keys=[Segmento])
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])


class PreProjeto(Base):
    __tablename__ = 'PreProjeto'

    idPreProjeto = Column(Integer, primary_key=True)
    NomeProjeto = Column(String)
    DtInicioDeExecucao = Column(Date)
    DtFinalDeExecucao = Column(Date)
    dtAceite = Column(Date)
    DtArquivamento = Column(Date)
    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
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

    # Related fields
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])


class Segmento(Base):
    __tablename__ = 'Segmento'

    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)


class Enquadramento(Base):
    __tablename__ = 'Enquadramento'

    IdEnquadramento = Column(Integer, primary_key=True)
    Enquadramento = Column(Integer)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    IdPRONAC = Column(Integer, ForeignKey('Projetos.IdPRONAC'))

    # Computed properties
    enquadramento = case(
        [
            (Enquadramento == '1', 'Artigo 26'),
            (Enquadramento == '2', 'Artigo 18'),
        ],
        else_='Nao enquadrado',
    ).label('enquadramento')


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

    # Related field
    captacao_related = relationship(
        'Captacao',
        primaryjoin='Interessado.CgcCpf==Captacao.CgcCpfMecena',
    )
    projeto_related = relationship(
        'Projeto',
        primaryjoin='Interessado.CgcCpf==Projeto.CgcCpf',
    )


class Captacao(Base):
    __tablename__ = 'Captacao'

    Idcaptacao = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    CaptacaoReal = Column(String)
    DtRecibo = Column(Date)
    CgcCpfMecena = Column(String, ForeignKey('Interessado.CgcCpf'))

    # Related fields
    interessado_related = relationship(
        'Interessado',
        foreign_keys=[CgcCpfMecena],
    )
    # projeto_related = relationship(
    #     'Projeto',
    #     primaryjoin='Captacao.PRONAC==Projeto.PRONAC',
    # )


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

    # Related fields
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
    idProduto = Column(Integer, ForeignKey('Produto.Codigo'))
    stPrincipal = Column(Integer)
    Segmento = Column(String, ForeignKey('Segmento.Codigo'))
    Area = Column(String, ForeignKey('Area.Codigo'))
    idPosicaoDaLogo = Column(Integer, ForeignKey('Verificacao.idVerificacao'))
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

    # Related fields
    area_related = relationship('Area', foreign_keys=[Area])
    produto_related = relationship('Produto', foreign_keys=[idProduto])
    projeto_related = relationship('Projeto', foreign_keys=[idProjeto])
    segmento_related = relationship('Segmento', foreign_keys=[Segmento])
    verificacao_related = relationship('Verificacao',
                                       foreign_keys=[idPosicaoDaLogo])


#
# This data is stored as SQL procedures. We create a new table when working
# with local Sqlite data
#
class Custos(Base):
    __tablename__ = 'Custos'

    idCustos = Column(Integer, primary_key=True)
    IdPRONAC = Column(Integer, ForeignKey("Projetos.IdPRONAC"))
    valor_proposta = Column(Integer)
    valor_solicitado = Column(Integer)
    valor_aprovado = Column(Integer)
    valor_aprovado_convenio = Column(Integer)
    custo_projeto = Column(Integer)
    outras_fontes = Column(Integer)
