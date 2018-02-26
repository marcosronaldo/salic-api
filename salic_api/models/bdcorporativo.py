from sqlalchemy import Column, Integer, ForeignKey, Float, String, case

from .base import Base, DateTime


class ItemCusto(Base):
    """
    (BDCORPORATIVO.scSAC.ItemCusto)
    """
    __tablename__ = 'tbItemCusto'

    idItem = Column(Integer, primary_key=True)
    idPlanilhaAprovacao = Column(Integer, ForeignKey(
        'tbPlanilhaAprovacao.idPlanilhaAprovacao'))


class ComprovantePagamentoxPlanilhaAprovacao(Base):  # noqa: N801
    """
    Cruzamento de informação de comprovantes de pagamento e a planilha de aprovação
    (BDCORPORATIVO.scSAC.ComprovantePagamentoxPlanilhaAprovacao)
    """
    __tablename__ = 'tbComprovantePagamentoxPlanilhaAprovacao'

    idPlanilhaAprovacao = Column(Integer, primary_key=True)
    idComprovantePagamento = Column(
        Integer,
        ForeignKey('tbComprovantePagamento.idComprovantePagamento'))
    tpDocumento = Column(Integer)
    vlComprovado = Column(Float)
    nrOcorrencia = Column(Integer)
    DtEmissao = Column(DateTime)
    dsItemDeCusto = Column(String)
    dsMarca = Column(String)
    dsFabricante = Column(String)

    # Computed properties
    tpDocumentoLabel = case(
        [
            (tpDocumento == 1, 'Boleto Bancario'),
            (tpDocumento == 2, 'Cupom Fiscal'),
            (tpDocumento == 3, 'Nota Fiscal / Fatura'),
            (tpDocumento == 4, 'Recibo de Pagamento'),
            (tpDocumento == 5, 'RPA'),
        ],
        else_='Nao identificado',
    ).label('tipo_documento')


class ComprovantePagamento(Base):  # noqa: N801
    """
    Contem informações dos comprovantes de pagamentos realizados durante o projeto
    (BDCORPORATIVO.scSAC.ComprovantePagamento)
    """
    __tablename__ = 'tbComprovantePagamento'

    idComprovantePagamento = Column(Integer, primary_key=True)
    idFornecedor = Column(Integer)
    idArquivo = Column(Integer, ForeignKey('tbArquivo.idArquivo'))
    DtPagamento = Column(DateTime)
    dtEmissao = Column(DateTime)
    tpFormaDePagamento = Column(String)
    nrDocumentoDePagamento = Column(String)
    nrComprovante = Column(String)
    dsJustificativa = Column(String)
    vlComprovacao = Column(Float)


class Arquivo(Base):  # noqa: N801
    """
    (BDCORPORATIVO.scCorp.Arquivo)
    """
    __tablename__ = 'tbArquivo'

    idArquivo = Column(Integer, primary_key=True)
    nmArquivo = Column(String)


class ArquivoImagem(Base):
    """
    (BDCORPORATIVO.scCorp.ArquivoImagem)
    """
    __tablename__ = 'tbArquivoImagem'

    idArquivoImagem = Column(Integer, primary_key=True)
    idArquivo = Column(Integer, ForeignKey("tbArquivo.idArquivo"))
    imagem = Column(String)
    dsDocumento = Column(String)


class Documento(Base):
    """
    (BDCORPORATIVO.scCorp.Documento)
    """
    __tablename__ = 'tbDocumento'

    idDocumento = Column(Integer, primary_key=True)
    idArquivo = Column(Integer, ForeignKey("tbArquivo.idArquivo"))


class DocumentoProjeto(Base):
    """
    (BDCORPORATIVO.scCorp.DocumentoProjeto)
    """
    __tablename__ = 'tbDocumentoProjeto'

    idDocumentoProjeto = Column(Integer, primary_key=True)
    idDocumento = Column(Integer, ForeignKey("tbDocumento.idDocumento"))
    idTipoDocumento = Column(Integer)
    idPronac = Column(Integer)
