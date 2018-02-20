from sqlalchemy.sql import text

from ..query import Query, filter_query
from ..serialization import listify_queryset
from ...utils import encrypt
from ...models import Agentes, Nomes, Internet, \
    ComprovantePagamento as Comprovante, \
    ComprovantePagamentoxPlanilhaAprovacao as ComprovanteAprovacao, \
    PlanilhaAprovacao, PlanilhaItens, Arquivo, Produto, Projeto


class FornecedorQuery(Query):
    query_fields = (
        Agentes.CNPJCPF.label('cgccpf'),
        Nomes.Descricao.label('nome'),
        Internet.Descricao.label('email'),
    )

    def query(self, limit=1, offset=0, cgccpf=None, PRONAC=None, nome=None):
        query = self.raw_query(*self.query_fields)
        query = query.select_from(ComprovanteAprovacao)
        query = query.distinct(*self.query_fields)
        query = (query
                 .join(Comprovante,
                       ComprovanteAprovacao.idComprovantePagamento ==
                       Comprovante.idComprovantePagamento)
                 .outerjoin(Internet,
                            Comprovante.idFornecedor == Internet.idAgente)
                 .outerjoin(PlanilhaAprovacao,
                            ComprovanteAprovacao.idPlanilhaAprovacao ==
                            PlanilhaAprovacao.idPlanilhaAprovacao)
                 # FIXME: check if the explicit equality test is necessary
                 # now that we have a FK constraint
                 .outerjoin(PlanilhaItens,
                            PlanilhaAprovacao.idPlanilhaItem ==
                            PlanilhaItens.idPlanilhaItens)
                 .outerjoin(Nomes,
                            Comprovante.idFornecedor == Nomes.idAgente)
                 .outerjoin(Arquivo,
                            Comprovante.idArquivo == Arquivo.idArquivo)
                 .outerjoin(Agentes,
                            Comprovante.idFornecedor == Agentes.idAgente)

                 )

        if cgccpf is not None:
            query = query.filter(Agentes.CNPJCPF.like(cgccpf))

        # query = query.order_by('cgccpf')
        return query

        # FIXME: move this to a separarte function
        if cgccpf is not None:
            query = text(FORNECEDOR_CGCCPF)
            return self.session.execute(query, {
                'cgccpf': '%{}%'.format(cgccpf),
                'offset': offset,
                'limit': limit,
            })

        elif nome is not None:
            query = text(FORNECEDOR_NOME)
            return self.session.execute(query, {
                'nome': '%{}%'.format(nome),
                'offset': offset,
                'limit': limit,
            }).fetchall()

        elif PRONAC is not None:
            query = text(FORNECEDOR_PRONAC)
            return self.session.execute(query, {
                'PRONAC': PRONAC,
                'offset': offset,
                'limit': limit,
            }).fetchall()
        else:
            query = text(FORNECEDOR)
            return self.session.execute(query, {
                'offset': offset,
                'limit': limit,
            }).fetchall()

    def count(self, cgccpf=None, PRONAC=None, nome=None):
        if cgccpf is not None:
            query = text(FORNECEDOR_COUNT_CGCCPF)
            result = self.sql_connector.session.execute(
                query, {'cgccpf': '%{}%'.format(cgccpf)}).fetchall()

        elif nome is not None:
            query = text(FORNECEDOR_COUNT_NOME)
            result = self.sql_connector.session.execute(
                query, {'nome': '%{}%'.format(nome)}).fetchall()

        elif PRONAC is not None:
            query = text(FORNECEDOR_COUNT_PRONAC)
            result = self.sql_connector.session.execute(
                query, {'PRONAC': PRONAC}).fetchall()

        else:
            query = text(FORNECEDOR_COUNT)
            result = self.session.execute(query, {}).fetchall()

        n_records = listify_queryset(result)
        return n_records[0]['total']


class ProductQuery(Query):
    query_fields = (
        ComprovanteAprovacao.idPlanilhaAprovacao.label(
            "id_planilha_aprovacao"),
        Comprovante.dsJustificativa.label("justificativa"),
        Comprovante.dtEmissao.label("data_pagamento"),
        Produto.Descricao.label("nome"),
        Agentes.CNPJCPF.label("cgccpf"),
        Comprovante.tpFormaDePagamento.label("tipo_forma_pagamento"),
        Comprovante.DtPagamento.label("data_aprovacao"),
        ComprovanteAprovacao.vlComprovado.label("valor_pagamento"),
        Comprovante.idArquivo.label("id_arquivo"),
        Comprovante.nrComprovante.label("nr_comprovante"),
        Nomes.Descricao.label("nome_fornecedor"),
        Comprovante.idComprovantePagamento.label("id_comprovante_pagamento"),
        ComprovanteAprovacao.tpDocumentoLabel,
        Comprovante.nrDocumentoDePagamento.label("nr_documento_pagamento"),
        Arquivo.nmArquivo.label("nm_arquivo"),
        Projeto.PRONAC.label("PRONAC"),
    )

    def query(self, cgccpf, limit=100, offset=0):
        query = self.raw_query(*self.query_fields)

        query = query.select_from(Comprovante)
        query = query.order_by(ComprovanteAprovacao.idPlanilhaAprovacao)
        query = (query
                 .outerjoin(Nomes,
                            Comprovante.idFornecedor == Nomes.idAgente)
                 .outerjoin(Agentes,
                            Comprovante.idFornecedor == Agentes.idAgente)
                 .outerjoin(Projeto,
                            Comprovante.idFornecedor == Agentes.idAgente)
                 .filter(Agentes.CNPJCPF.like(cgccpf))
                )

        return query


FORNECEDOR_CGCCPF = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (g.CNPJCPF LIKE :cgccpf) AND g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR_NOME = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (e.Descricao LIKE :nome) AND g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR_PRONAC = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE (Projetos.AnoProjeto + Projetos.Sequencial = :PRONAC) AND g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR_COUNT_CGCCPF = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (g.CNPJCPF LIKE :cgccpf) AND g.CNPJCPF IS NOT NULL
"""

FORNECEDOR_COUNT_NOME = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (e.Descricao LIKE :nome) AND g.CNPJCPF IS NOT NULL
"""

FORNECEDOR_COUNT_PRONAC = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE (Projetos.AnoProjeto + Projetos.Sequencial = :PRONAC) AND g.CNPJCPF IS NOT NULL
"""

FORNECEDOR_COUNT = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE g.CNPJCPF IS NOT NULL
"""
