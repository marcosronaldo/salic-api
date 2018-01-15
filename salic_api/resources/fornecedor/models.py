from sqlalchemy.sql import text

from ..model_base import ModelsBase
from ..projeto.models import ProjetoModelObject
from ..serialization import listify_queryset


class FornecedordorModelObject(ModelsBase):
    def all(self, limit, offset, cgccpf=None, PRONAC=None, nome=None):

        if cgccpf is not None:
            query = text("""
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
              """)

            return self.sql_connector.session.execute(query, {
                'cgccpf': '%' + cgccpf + '%', 'offset': offset, 'limit': limit
            }).fetchall()

        elif nome is not None:
            query = text("""
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

              """)

            return self.sql_connector.session.execute(query, {
                'nome': '%' + nome + '%', 'offset': offset, 'limit': limit
            }).fetchall()

        elif PRONAC is not None:
            query = text("""
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

              """)

            return self.sql_connector.session.execute(query, {
                'PRONAC': PRONAC, 'offset': offset, 'limit': limit
            }).fetchall()

        else:

            query = text("""
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


              """)

            return self.sql_connector.session.execute(query, {
                'offset': offset, 'limit': limit
            }).fetchall()

    def count(self, cgccpf=None, PRONAC=None, nome=None):

        if cgccpf is not None:
            query = text("""
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

              """)

            result = self.sql_connector.session.execute(
                query, {'cgccpf': '%' + cgccpf + '%'}).fetchall()

        elif nome is not None:
            query = text("""
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

              """)

            result = self.sql_connector.session.execute(
                query, {'nome': '%' + nome + '%'}).fetchall()

        elif PRONAC is not None:
            query = text("""
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

              """)

            result = self.sql_connector.session.execute(
                query, {'PRONAC': PRONAC}).fetchall()

        else:
            query = text("""
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

              """)

            result = self.sql_connector.session.execute(query, {}).fetchall()

        n_records = listify_queryset(result)

        return n_records[0]['total']


class ProductModelObject(ModelsBase):
    def __init__(self):
        super(ProductModelObject, self).__init__()

    def all(self, limit, offset, cgccpf):
        return ProjetoModelObject().payments_listing(limit, offset,
                                                     cgccpf=cgccpf)

    def count(self, cgccpf):
        return ProjetoModelObject().payments_listing_count(cgccpf=cgccpf)

        # n_records = listify_queryset(result)

        # print 'full list:' + str(n_records)

        # return n_records[0]['total']
