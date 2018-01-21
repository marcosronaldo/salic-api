from sqlalchemy import case, func
from sqlalchemy.sql.expression import desc

from ..query import Query
from ..shared_models import Interessado, Projeto, Captacao
from ...utils.strings import pc_quote


class IncentivadorQuery(Query):
    def query(self, limit, offset, nome=None, cgccpf=None, municipio=None,
              UF=None, tipo_pessoa=None, PRONAC=None, sort_field=None,
              sort_order=None):

        start_row = offset
        end_row = offset + limit
        tipo_pessoa_case = case(
            [
                (Interessado.tipoPessoa == '1', 'fisica'),
            ],
            else_='juridica'
        )

        sort_mapping_fields = {
            'cgccpf': Interessado.CgcCpf,
            'total_doado': func.sum(Captacao.CaptacaoReal)
        }

        if sort_field == None:
            sort_field = 'cgccpf'

        sort_field = sort_mapping_fields[sort_field]

        res = self.sql_connector.session.select(
            Interessado.Nome.label('nome'),
            Interessado.Cidade.label('municipio'),
            Interessado.Uf.label('UF'),
            Interessado.Responsavel.label('responsavel'),
            Interessado.CgcCpf.label('cgccpf'),
            func.sum(Captacao.CaptacaoReal).label('total_doado'),
            tipo_pessoa_case.label('tipo_pessoa'),
        ).join(Captacao)

        if PRONAC is not None:
            res = res \
                .join(Projeto, Captacao.PRONAC == Projeto.PRONAC) \
                .filter(Captacao.PRONAC == PRONAC)

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

        res = res.group_by(
            Interessado.Nome,
            Interessado.Cidade,
            Interessado.Uf,
            Interessado.Responsavel,
            Interessado.CgcCpf,
            tipo_pessoa_case,
        )

        # order by descending
        if sort_order == 'desc':
            res = res.order_by(desc(sort_field))
        else:
            res = res.order_by(sort_field)
        total_records = res.count()
        res = res.slice(start_row, end_row)
        return res.query(), total_records


class DoacaoQuery(Query):
    def query(self, limit, offset, cgccpf=None):
        start_row = offset
        end_row = offset + limit

        res = (
            self.sql_connector.session.select(
                Captacao.PRONAC,
                Captacao.CaptacaoReal.label('valor'),
                Captacao.DtRecibo.label('data_recibo'),
                Projeto.NomeProjeto.label('nome_projeto'),
                Captacao.CgcCpfMecena.label('cgccpf'),
                Interessado.Nome.label('nome_doador'),
            )
                .join(Projeto,
                      Captacao.PRONAC == Projeto.PRONAC)
                .join(Interessado,
                      Captacao.CgcCpfMecena == Interessado.CgcCpf)
        )

        if cgccpf is not None:
            res = res.filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))

        res = res.order_by(desc(Captacao.DtRecibo))
        total_records = res.count()
        res = res.slice(start_row, end_row)
        return res.query(), total_records

    def total(self, cgccpf):
        total_doado = func.sum(Captacao.CaptacaoReal).label('total_doado')
        return (
            self.sql_connector.session.select(total_doado)
                .join(Interessado,
                      Captacao.CgcCpfMecena == Interessado.CgcCpf)
                .filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))
        )
