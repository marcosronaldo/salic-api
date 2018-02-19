from sqlalchemy import Column, Date, DateTime, Integer, String, ForeignKey, \
    Text, Boolean, case, CHAR, DATE, func, VARCHAR, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy.orm import relationship

Base = declarative_base()

# TODO: can we support the money type in the SQL Server?
Money = String
use_sqlite = True

if use_sqlite:
    DateTime = Date
    date_column = (lambda x: func.cast(x, VARCHAR))
else:
    date_column = (lambda x: func.cast(x, DATE))


class Projeto(Base):
    """
    SAC.dbo.Projetos
    """
    __tablename__ = 'Projetos'

    IdPRONAC = Column(Integer, primary_key=True)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    NomeProjeto = Column(String)
    Localizacao = Column(String)
    DtInicioExecucao = Column(DateTime)  # Date?
    data_inicio_execucao = date_column(DtInicioExecucao)
    DtFimExecucao = Column(DateTime)
    data_fim_execucao = date_column(DtFimExecucao)
    UfProjeto = Column(CHAR)
    SolicitadoReal = Column(Money)
    SolicitadoUfir = Column(Money)
    SolicitadoCusteioUfir = Column(Money)
    SolicitadoCusteioReal = Column(Money)
    SolicitadoCapitalUfir = Column(Money)
    SolicitadoCapitalReal = Column(Money)
    ResumoProjeto = Column(Text)
    ProvidenciaTomada = Column(String)
    Segmento = Column(String, ForeignKey("Segmento.Codigo"))
    Situacao = Column(CHAR, ForeignKey("Situacao.Codigo"))
    CgcCpf = Column(String, ForeignKey("Interessado.CgcCpf"))
    idProjeto = Column(Integer, ForeignKey("PreProjeto.idPreProjeto"))

    # Original DB do not create a foreign key constraint
    Area = Column(CHAR, ForeignKey("Area.Codigo"))
    Mecanismo = Column(CHAR, ForeignKey("Mecanismo.Codigo"))

    # Related fields
    preprojeto_related = relationship("PreProjeto", foreign_keys=[idProjeto])
    situacao_related = relationship("Situacao", foreign_keys=[Situacao])
    interessado_related = relationship("Interessado", foreign_keys=[CgcCpf])
    segmento_related = relationship("Segmento", foreign_keys=[Segmento])
    area_related = relationship("Area", foreign_keys=[Area])
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])


class PreProjeto(Base):
    """
    SAC.dbo.PreProjeto
    """
    __tablename__ = 'PreProjeto'

    idPreProjeto = Column(Integer, primary_key=True)
    NomeProjeto = Column(String)
    DtInicioDeExecucao = Column(DateTime)
    data_inicio_execucao = date_column(DtInicioDeExecucao)
    DtFinalDeExecucao = Column(DateTime)
    data_final_execucao = date_column(DtFinalDeExecucao)
    dtAceite = Column(DateTime)
    data_aceite = date_column(dtAceite)
    DtArquivamento = Column(DateTime)
    data_arquivamento = date_column(DtArquivamento)
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

    # Original table does not use a foreign key constraint (possibly because
    # it uses the wrong data type in this column. The original table uses a
    # CHAR primary key).
    #
    # Values: 1 - Mecenato, 2 - FNC (maybe more...)
    Mecanismo = Column(Integer, ForeignKey("Mecanismo.Codigo"))

    # Related fields
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])


class Segmento(Base):
    """
    SAC.dbo.Segmento
    """
    __tablename__ = 'Segmento'

    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)

    # Values: 1 - Artigo 26 (30%), 2 - Artigo 18 (100%)
    tpEnquadramento = Column(CHAR)


class Enquadramento(Base):
    """
    SAC.dbo.Enquadramento
    """
    __tablename__ = 'Enquadramento'

    IdEnquadramento = Column(Integer, primary_key=True)
    Enquadramento = Column(Integer)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    IdPRONAC = Column(Integer, ForeignKey('Projetos.IdPRONAC'))

    # Computed properties
    enquadramento = case(
        [
            (Enquadramento == 1, 'Artigo 26'),
            (Enquadramento == 2, 'Artigo 18'),
        ],
        else_='Nao enquadrado',
    ).label('enquadramento')


class Mecanismo(Base):
    """
    SAC.dbo.Mecanismo
    """
    __tablename__ = 'Mecanismo'

    # Values:
    # 1 - Mecenato
    # 2 - FNC
    # The values bellow were removed from the database
    # 3 - Audiovisual (disabled)
    # 4 - Conversão da dívida externa (disabled)
    # 5 - Mecenato audiovisual (disabled)
    # 6 - Recurso do Tesouro
    # 7 - Outras fontes (disabled)
    Codigo = Column(CHAR, primary_key=True)
    Descricao = Column(String)


class Situacao(Base):
    """
    SAC.dbo.Situacao
    """
    __tablename__ = 'Situacao'

    Codigo = Column(CHAR, primary_key=True)
    Descricao = Column(String)


class Area(Base):
    """
    SAC.dbo.Area
    """
    __tablename__ = 'Area'

    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)


class Interessado(Base):
    """
    SAC.dbo.Interessado
    """
    __tablename__ = 'Interessado'

    CgcCpf = Column(String, primary_key=True)
    Nome = Column(String)
    Responsavel = Column(String)
    Uf = Column(CHAR)
    Cidade = Column(String)
    tipoPessoa = Column(CHAR)

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
    """
    SAC.dbo.Captacao
    """
    __tablename__ = 'Captacao'

    Idcaptacao = Column(Integer, primary_key=True)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    CaptacaoReal = Column(Money)
    DtRecibo = Column(DateTime)
    data_recibo = date_column(DtRecibo)
    CgcCpfMecena = Column(String, ForeignKey('Interessado.CgcCpf'))

    # Related fields
    interessado_related = relationship(
        'Interessado',
        foreign_keys=[CgcCpfMecena],
    )


class CertidoesNegativas(Base):
    """
    SAC.dbo.CertidoesNegativas
    """
    __tablename__ = 'CertidoesNegativas'

    idCertidoesNegativas = Column(Integer, primary_key=True)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    DtEmissao = Column(DateTime)
    data_emissao = date_column(DtEmissao)
    DtValidade = Column(DateTime)
    data_validade = date_column(DtValidade)
    CodigoCertidao = Column(Integer)
    cdSituacaoCertidao = Column(Integer)
    CgcCpf = Column(String, ForeignKey('Interessado.CgcCpf'))


class Verificacao(Base):
    """
    SAC.dbo.Verificacao
    """
    __tablename__ = 'Verificacao'

    idVerificacao = Column(Integer, primary_key=True)
    idTipo = Column(Integer)
    Descricao = Column(String)
    stEstado = Column(Boolean)


class PlanoDivulgacao(Base):
    """
    SAC.dbo.PlanoDivulgacao
    """
    __tablename__ = 'PlanoDeDivulgacao'

    idPlanoDivulgacao = Column(Integer, primary_key=True)
    stPlanoDivulgacao = Column(Boolean)
    idPeca = Column(Integer, ForeignKey('Verificacao.idVerificacao'))
    idVeiculo = Column(Integer, ForeignKey('Verificacao.idVerificacao'))
    idProjeto = Column(Integer, ForeignKey('PreProjeto.idPreProjeto'))

    # Related fields
    projeto_related = relationship('PreProjeto', foreign_keys=[idProjeto])


class Produto(Base):
    """
    SAC.dbo.Produto
    """
    __tablename__ = 'Produto'

    Codigo = Column(Integer, primary_key=True)
    Descricao = Column(String)
    Sintese = Column(Text)
    Idorgao = Column(Integer)
    stEstado = Column(Boolean)

    # Original table does not use a foreign key constraint
    Area = Column(CHAR, ForeignKey('Area.Codigo'))


class PlanoDistribuicao(Base):
    """
    SAC.dbo.PlanoDistribuicaoProduto
    """
    __tablename__ = 'PlanoDistribuicaoProduto'

    idPlanoDistribuicao = Column(Integer, primary_key=True)
    QtdeProduzida = Column(Integer)
    QtdeProponente = Column(Integer)
    QtdePatrocinador = Column(Integer)
    QtdeOutros = Column(Integer)
    QtdeVendaNormal = Column(Integer)
    QtdeVendaPromocional = Column(Integer)
    QtdeUnitarioNormal = Column(Integer)
    QtdeUnitarioPromocional = Column(Integer)
    PrecoUnitarioPromocional = Column(Money)
    PrecoUnitarioNormal = Column(Money)
    stPlanoDistribuicaoProduto = Column(Boolean)
    stPrincipal = Column(Boolean)
    idProjeto = Column(Integer, ForeignKey('Projetos.idProjeto'))
    idProduto = Column(Integer, ForeignKey('Produto.Codigo'))
    idPosicaoDaLogo = Column(Integer, ForeignKey('Verificacao.idVerificacao'))

    # Original table does not use a foreign key constraint
    Segmento = Column(String, ForeignKey('Segmento.Codigo'))
    Area = Column(CHAR, ForeignKey('Area.Codigo'))

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
class tbComprovantePagamentoxPlanilhaAprovacao(Base):  # noqa: N801
    """
    BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao
    """
    __tablename__ = 'tbComprovantePagamentoxPlanilhaAprovacao'

    idPlanilhaAprovacao = Column(Integer, primary_key=True)
    idComprovantePagamento = Column(
        Integer,
        ForeignKey('tbComprovantePagamento.idComprovantePagamento'))
    tpDocumento = Column(Integer)
    vlComprovado = Column(Float)
    nrOcorrencia = Column(Integer)
    DtEmissao = Column(Date)
    dsItemDeCusto = Column(String)
    dsMarca = Column(String)
    dsFabricante = Column(String)


class tbComprovantePagamento(Base):  # noqa: N801
    """
    BDCORPORATIVO.scSAC.tbComprovantePagamento
    """
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
    vlComprovacao = Column(Float)



class tbArquivo(Base):  # noqa: N801
    """
    BDCORPORATIVO.scCorp.tbArquivo
    """
    __tablename__ = 'tbArquivo'

    idArquivo = Column(Integer, primary_key=True)
    nmArquivo = Column(String)


class tbPlanilhaAprovacao(Base):  # noqa: N801
    """
    SAC.dbo.tbPlanilhaAprovacao
    """
    __tablename__ = 'tbPlanilhaAprovacao'

    idPlanilhaAprovacao = Column(Integer, primary_key=True)
    idPlanilhaItem = Column(Integer,
                            ForeignKey('tbPlanilhaItens.idPlanilhaItens'))
    IdPRONAC = Column(Integer, ForeignKey('Projetos.IdPRONAC'))


class tbPlanilhaItens(Base):  # noqa: N801
    """
    SAC.dbo.tbPlanilhaItens
    """
    __tablename__ = 'tbPlanilhaItens'

    idPlanilhaItens = Column(Integer, primary_key=True)
    Descricao = Column(String)


# This table actually describes city names
class Nomes(Base):
    """
    Agentes.dbo.Nomes
    """
    __tablename__ = 'Nomes'

    idNome = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey('Agentes.idAgente'))
    Descricao = Column(String)


class Agentes(Base):
    """
    Agentes.dbo.Agentes
    """
    __tablename__ = 'Agentes'

    idAgente = Column(Integer, primary_key=True)
    CNPJCPF = Column(String)


class Internet(Base):
    """
    Agentes.dbo.Internet
    """
    __tablename__ = 'Internet'

    idInternet = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey('Agentes.idAgente'))
    Descricao = Column(String)


# TODO: manually check those tables!
class tbArquivoImagem(Base):
    """
    BDCORPORATIVO.scCorp.tbArquivoImagem
    """
    __tablename__ = 'tbArquivoImagem'

    idArquivoImagem = Column(Integer, primary_key=True)
    idArquivo = Column(Integer, ForeignKey('tbArquivo.idArquivo'))


class tbDocumento(Base):
    """
    BDCORPORATIVO.scCorp.tbDocumento
    """
    __tablename__ = 'tbDocumento'

    idDocumento = Column(Integer, primary_key=True)
    idArquivo = Column(Integer, ForeignKey('tbArquivo.idArquivo'))


class tbDocumentoProjeto(Base):
    """
    BDCORPORATIVO.scCorp.tbDocumentoProjeto
    """
    __tablename__ = 'tbDocumentoProjeto'

    idDocumentoProjeto = Column(Integer, primary_key=True)
    idDocumento = Column(Integer, ForeignKey('tbDocumento.idDocumento'))
    idTipoDocumento = Column(Integer)
    idPronac = Column(Integer)


#
# This data is stored as SQL procedures. We create a new table when working
# with local Sqlite data
#
class Custos(Base):
    __tablename__ = 'Custos'

    idCustos = Column(Integer, primary_key=True)
    IdPRONAC = Column(String, ForeignKey("Projetos.IdPRONAC"))
    idInteressado = Column(String, ForeignKey("Interessado.CgcCpf"))
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


class Usuarios(Base):
    _full_name = 'TABELAS.dbo.Usuarios'
    __tablename__ = 'Usuarios'

    usu_codigo = Column(Integer, primary_key=True)
    usu_nome = Column(String)


# FIXME put right columns when given access to this table.
# for now using made up primary key
class prorrogacao(Base):
    __tablename__ = 'prorrogacao'

    idProrrogacao = Column(Integer, primary_key=True)
    Logon = Column(Integer)
    DtPedido = Column(Date)
    DtInicio = Column(Date)
    DtFinal = Column(Date)
    Observacao = Column(String)
    Atendimento = Column(String)
    idPronac = Column(Integer)


class tbPlanilhaEtapa(Base):
    __tablename__ = 'tbPlanilhaEtapa'
    idPlanilhaEtapa = Column(Integer, primary_key=True)
    Descricao = Column(String)


class tbPlanilhaUnidade(Base):
    __tablename__ = 'tbPlanilhaUnidade'

    idUnidade = Column(Integer, primary_key=True)
    Descricao = Column(String)


class tbItemCusto(Base):
    __tablename__ = 'tbItemCusto'

    idItem = Column(Integer, primary_key=True)
    idPlanilhaAprovacao = Column(Integer, ForeignKey('tbPlanilhaAprovacao.idPlanilhaAprovacao'))
