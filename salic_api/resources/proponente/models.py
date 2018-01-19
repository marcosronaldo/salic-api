from sqlalchemy import case, func
from sqlalchemy.sql.expression import desc

from ..query import Query
from ..shared_models import Interessado, Projeto


class ProponenteQuery(Query):
    def all(self, limit, offset, nome=None, cgccpf=None, municipio=None,
            UF=None, tipo_pessoa=None, sort_field=None, sort_order=None):

        start_row = offset
        end_row = offset + limit

        sort_mapping_fields = {
            'cgccpf': Interessado.CgcCpf,
            'total_captado': func.sum(
                func.sac.dbo.fnCustoProjeto(Projeto.AnoProjeto,
                                            Projeto.Sequencial))
        }

        if sort_field == None:
            sort_field = 'cgccpf'

        sort_field = sort_mapping_fields[sort_field]

        tipo_pessoa_case = case(
            [(Interessado.tipoPessoa == '1', 'fisica'), ],
            else_='juridica')

        res = self.sql_connector.session.query(
            func.sum(func.sac.dbo.fnCustoProjeto(Projeto.AnoProjeto,
                                                 Projeto.Sequencial)).label(
                'total_captado'),
            Interessado.Nome.label('nome'),
            Interessado.Cidade.label('municipio'),
            Interessado.Uf.label('UF'),
            Interessado.Responsavel.label('responsavel'),
            Interessado.CgcCpf.label('cgccpf'),
            tipo_pessoa_case.label('tipo_pessoa'),
        ).join(Interessado)

        res = res.group_by(Interessado.Nome,
                           Interessado.Cidade,
                           Interessado.Uf,
                           Interessado.Responsavel,
                           Interessado.CgcCpf,
                           tipo_pessoa_case
                           )

        res = res.filter(Projeto.idProjeto.isnot(None))

        if cgccpf is not None:
            res = res.filter(Interessado.CgcCpf.like('%' + cgccpf + '%'))

        if nome is not None:
            res = res.filter(Interessado.Nome.like('%' + nome + '%'))

        if UF is not None:
            res = res.filter(Interessado.Uf == UF)

        if municipio is not None:
            res = res.filter(Interessado.Cidade == municipio)

        if tipo_pessoa is not None:
            if tipo_pessoa == 'fisica':
                tipo_pessoa = '1'
            else:
                tipo_pessoa = '2'

            res = res.filter(Interessado.tipoPessoa == tipo_pessoa)

        # order by descending
        if sort_order == 'desc':
            res = res.order_by(desc(sort_field))
        # order by ascending
        else:
            res = res.order_by(sort_field)

        total_records = res.count()

        res = res.slice(start_row, end_row)

        return res.all(), total_records
