from sqlalchemy import func

from ..projeto.query import custo_projeto
from ..query import Query, filter_query, filter_query_like
from ...models import Interessado, Projeto, Custos

use_sql_procedures = False


class ProponenteQuery(Query):
    query_fields = (
        custo_projeto.label('total_captado'),
        Interessado.Nome.label('nome'),
        Interessado.Cidade.label('municipio'),
        Interessado.Uf.label('UF'),
        Interessado.Responsavel.label('responsavel'),
        Interessado.CgcCpf.label('cgccpf'),
        Interessado.tipoPessoa.label('tipo_pessoa'),
    )

    group_by_fields = (
        Interessado.Nome,
        Interessado.Cidade,
        Interessado.Uf,
        Interessado.Responsavel,
        Interessado.CgcCpf,
        Interessado.tipoPessoa,
    )

    tipo_pessoa_map = {
        'fisica': '1',
        'juridica': '2',
    }

    def query(self, limit=1, offset=0, nome=None, cgccpf=None, municipio=None,
              UF=None, tipo_pessoa=None, sort_field=None, sort_order=None):

        query = self.raw_query(*self.query_fields)
        query = query.select_from(Interessado)

        if not use_sql_procedures:
            query = query.join(Custos)

        query = query.group_by(*self.group_by_fields)
        query = query.filter(Projeto.idProjeto.isnot(None))
        query = filter_query_like(query, {
            Interessado.CgcCpf: cgccpf,
            Interessado.Nome: nome,
        })
        query = filter_query(query, {
            Interessado.Uf: UF,
            Interessado.Cidade: municipio,
            Interessado.tipoPessoa: self.tipo_pessoa_map.get(tipo_pessoa),
        })

        return self.sorted(query, sort_field, sort_order)

    def sorted(self, query, sort_field, sort_order):
        # start_row = offset
        # end_row = offset + limit

        sort_mapping_fields = {
            'cgccpf': Interessado.CgcCpf,
            'total_captado': func.sum(
                func.sac.dbo.fnCustoProjeto(Projeto.AnoProjeto,
                                            Projeto.Sequencial))
        }

        if sort_field is None:
            sort_field = 'cgccpf'

        sort_field = sort_mapping_fields[sort_field]

        return query
####################################


#         # order by descending
#         if sort_order == 'desc':
#             query = query.order_by(desc(sort_field))
#         # order by ascending
#         else:
#             query = query.order_by(sort_field)
#
#         total_records = query.count()
#
#         query = query.slice(start_row, end_row)
#
#         return res.query(), total_records
