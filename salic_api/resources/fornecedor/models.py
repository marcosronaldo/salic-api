from sqlalchemy.sql import text

from ..projeto.models import ProjetoQuery
from ..query import Query
from ..serialization import listify_queryset
from ..shared_models import Agentes, Nomes, Internet, \
    tbComprovantePagamento as Comprovante, \
    tbComprovantePagamentoxPlanilhaAprovacao as ComprovanteAprovacao, \
    tbPlanilhaAprovacao, tbPlanilhaItens, tbArquivo


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
                 .outerjoin(tbPlanilhaAprovacao,
                            ComprovanteAprovacao.idPlanilhaAprovacao ==
                            tbPlanilhaAprovacao.idPlanilhaAprovacao)
                 # FIXME: check if the explicit equality test is necessary
                 # now that we have a FK constraint
                 .outerjoin(tbPlanilhaItens,
                            tbPlanilhaAprovacao.idPlanilhaItem ==
                            tbPlanilhaItens.idPlanilhaItens)
                 .outerjoin(Nomes,
                            Comprovante.idFornecedor == Nomes.idAgente)
                 .outerjoin(tbArquivo,
                            Comprovante.idArquivo == tbArquivo.idArquivo)
                 .outerjoin(Agentes,
                            Comprovante.idFornecedor == Agentes.idAgente)

                 )

        if cgccpf is not None:
            query = query.filter(Agentes.CNPJCPF.like(cgccpf))

        query = query.order_by('cgccpf')
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
    def query(self, limit, offset, cgccpf):
        return ProjetoQuery().payments_listing(limit, offset, cgccpf=cgccpf)

    def count(self, cgccpf):
        return ProjetoQuery().payments_listing_count(cgccpf=cgccpf)


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
