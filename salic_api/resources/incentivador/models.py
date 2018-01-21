from sqlalchemy import func
from sqlalchemy.sql.expression import desc

from ..query import Query, filter_query_like, filter_query
from ..shared_models import Interessado, Projeto, Captacao
from ...utils.strings import pc_quote


class IncentivadorQuery(Query):
    group_by_fields = (
        Interessado.Nome,
        Interessado.Cidade,
        Interessado.Uf,
        Interessado.Responsavel,
        Interessado.CgcCpf,
        Interessado.tipo_pessoa,
    )

    total_doado = func.sum(Captacao.CaptacaoReal).label('total_doado')

    query_fields = (
        Interessado.Nome.label('nome'),
        Interessado.Cidade.label('municipio'),
        Interessado.Uf.label('UF'),
        Interessado.Responsavel.label('responsavel'),
        Interessado.CgcCpf.label('cgccpf'),
        total_doado,
        Interessado.tipo_pessoa,
    )

    TIPOS_PESSOA = {'fisica': '1', 'juridica': '2'}

    def query(self, limit=1, offset=0, nome=None, cgccpf=None, municipio=None,
              UF=None, tipo_pessoa=None, PRONAC=None, sort_field=None,
              sort_order=None):

        query = self.raw_query(*self.query_fields).join(Captacao)

        query = filter_query_like(query, {
            Interessado.CgcCpf: cgccpf,
            Interessado.Nome: nome,
        })

        query = filter_query(query, {
            Interessado.Uf: UF,
            Interessado.Cidade: municipio,
            Interessado.tipoPessoa: self.TIPOS_PESSOA.get(tipo_pessoa),
        })

        if PRONAC is not None:
            query = query \
                .join(Projeto, Captacao.PRONAC == Projeto.PRONAC) \
                .filter(Captacao.PRONAC == PRONAC)

        query = query.group_by(*self.group_by_fields)
        return self.sort_query(query, sort_field, sort_order)

    def sort_query(self, query, sort_field, sort_order):
        sorting_fields = {
            'cgccpf': Interessado.CgcCpf,
            'total_doado': self.total_doado
        }
        sort_field = sorting_fields[sort_field or 'cgccpf']

        if sort_order == 'desc':
            query = query.order_by(desc(sort_field))
        else:
            query = query.order_by(sort_field)
        return query


class DoacaoQuery(Query):
    query_fields = (
        Captacao.PRONAC,
        Captacao.CaptacaoReal.label('valor'),
        Captacao.DtRecibo.label('data_recibo'),
        Projeto.NomeProjeto.label('nome_projeto'),
        Captacao.CgcCpfMecena.label('cgccpf'),
        Interessado.Nome.label('nome_doador'),
    )

    def query(self, limit=None, offset=0, cgccpf=None):
        query = (
            self.raw_query(*self.query_fields)
                .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
                .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
        )
        if cgccpf is not None:
            return query.filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))
        return query

    def total(self, cgccpf):
        total = func.sum(Captacao.CaptacaoReal).label('total_doado')
        return (
            self.raw_query(total)
                .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
                .filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))
        )
