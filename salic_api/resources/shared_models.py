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

    # FIXME: descobrir qual é o tipo do Codigo de Mecanismo (String ou Integer?)
    Codigo = Column(String, primary_key=True)
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

    # Computed fields
    tipo_pessoa = case(
        [
            (tipoPessoa == '1', 'fisica'),
        ],
        else_='juridica'
    ).label('tipo_pessoa')


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
# Additional tables from other databases
#
class tbComprovantePagamentoxPlanilhaAprovacao(Base):
    # planilha "a"
    _full_name = 'BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao'
    __tablename__ = 'tbComprovantePagamentoxPlanilhaAprovacao'

    idPlanilhaAprovacao = Column(Integer, primary_key=True)
    idComprovantePagamento = Column(
        Integer,
        ForeignKey('tbComprovantePagamento.idComprovantePagamento'))
    tpDocumento = Column(Integer)
    vlComprovado = Column(String)


class tbComprovantePagamento(Base):
    # planilha "b"
    _full_name = 'BDCORPORATIVO.scSAC.tbComprovantePagamento'
    __tablename__ = 'tbComprovantePagamento'

    idComprovantePagamento = Column(Integer, primary_key=True)
    idFornecedor = Column(Integer)
    idArquivo = Column(Integer, ForeignKey('tbArquivo.idArquivo'))
    DtPagamento = Column(Date)
    dtEmissao = Column(Date)
    tpFormaDePagamento = Column(String)
    nrDocumentoDePagamento = Column(String)
    nrComprovante = Column(String)
    dsJustificativa = Column(String)


class tbArquivo(Base):
    # planilha "f"
    _full_name = 'BDCORPORATIVO.scCorp.tbArquivo'
    __tablename__ = 'tbArquivo'

    idArquivo = Column(Integer, primary_key=True)
    nmArquivo = Column(String)
    dtEnvio = Column(Date)


class tbPlanilhaAprovacao(Base):
    # planilha "f"
    _full_name = 'SAC.dbo.tbPlanilhaAprovacao'
    __tablename__ = 'tbPlanilhaAprovacao'

    idPlanilhaAprovacao = Column(Integer, primary_key=True)
    idPlanilhaItem = Column(Integer)
    idPronac = Column(Integer)


class tbPlanilhaItens(Base):
    _full_name = 'SAC.dbo.tbPlanilhaItens'
    __tablename__ = 'tbPlanilhaItens'

    idPlanilhaItens = Column(Integer, primary_key=True)
    idPlanilhaItem = Column(Integer)
    Descricao = Column(String)


class Nomes(Base):
    _full_name = 'Agentes.dbo.Nomes'
    __tablename__ = 'Nomes'

    idNome = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey('Agentes.idAgente'))
    Descricao = Column(String)


class Agentes(Base):
    _full_name = 'Agentes.dbo.Agentes'
    __tablename__ = 'Agentes'

    idAgente = Column(Integer, primary_key=True)
    CNPJCPF = Column(String)


class Internet(Base):
    _full_name = 'Agentes.dbo.Internet'
    __tablename__ = 'Internet'

    idInternet = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey('Agentes.idAgente'))
    Descricao = Column(String)


#
# This data is stored as SQL procedures. We create a new table when working
# with local Sqlite data
#
class Custos(Base):
    __tablename__ = 'Custos'

    idCustos = Column(Integer, primary_key=True)
    IdPRONAC = Column(Integer, ForeignKey("Projetos.IdPRONAC"))
    idInteressado = Column(Integer, ForeignKey("Interessado.CgcCpf"))
    valor_proposta = Column(Integer)
    valor_solicitado = Column(Integer)
    valor_aprovado = Column(Integer)
    valor_aprovado_convenio = Column(Integer)
    custo_projeto = Column(Integer)
    outras_fontes = Column(Integer)


# FIXME put right columns when given access to this table
class tbArquivoImagem(Base):
    _full_name = 'BDCORPORATIVO.scCorp.tbArquivoImagem'
    __tablename__ = 'tbArquivoImagem'

    idArquivoImagem = Column(Integer, primary_key=True)
    idArquivo = Column(Integer, ForeignKey("tbArquivo.idArquivo"))
    imagem = Column(String)
    dsDocumento = Column(String)


class tbDocumento(Base):
    _full_name = 'BDCORPORATIVO.scCorp.tbDocumento'
    __tablename__ = 'tbDocumento'

    idDocumento = Column(Integer, primary_key=True)
    idArquivo = Column(Integer, ForeignKey("tbArquivo.idArquivo"))


class tbDocumentoProjeto(Base):
    _full_name = 'BDCORPORATIVO.scCorp.tbDocumentoProjeto'
    __tablename__ = 'tbDocumentoProjeto'

    idDocumentoProjeto = Column(Integer, primary_key=True)
    idDocumento = Column(Integer, ForeignKey("tbDocumento.idDocumento"))
    idTipoDocumento = Column(Integer)
    idPronac = Column(Integer)


class Pais(Base):
    __tablename__ = 'Pais'
    _full_name = 'Agentes.dbo.Pais'

    idPais = Column(Integer, primary_key=True)
    Descricao = Column(String)


class uf(Base):
    __tablename__ = 'uf'
    _full_name = 'Agentes.dbo.uf'

    iduf = Column(Integer, primary_key=True)
    Descricao = Column(String)


class Municipios(Base):
    __tablename__ = 'Municipios'
    _full_name = 'Agentes.dbo.Municipios'

    idMunicipioIBGE = Column(Integer, primary_key=True)
    Descricao = Column(String)


class tbDeslocamento(Base):
    __tablename__ = 'tbDeslocamento'

    idDeslocamento = Column(Integer, primary_key=True)
    Qtde = Column(Integer)
    idProjeto = Column(Integer, ForeignKey('Projetos.idProjeto'))
    idPaisOrigem = Column(Integer, ForeignKey('Pais.idPais'))
    idUFOrigem = Column(Integer, ForeignKey('uf.iduf'))
    idMunicipioOrigem = Column(Integer, ForeignKey('Municipios.idMunicipioIBGE'))
    idPaisDestino = Column(Integer, ForeignKey('Pais.idPais'))
    idUFDestino = Column(Integer, ForeignKey('uf.iduf'))
    idMunicipioDestino = Column(Integer, ForeignKey('Municipios.idMunicipioIBGE'))
