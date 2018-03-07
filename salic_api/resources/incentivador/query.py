from sqlalchemy import func
from sqlalchemy.sql.expression import desc

from ..query import Query, filter_query_like, filter_query
from ...models import Interessado, Projeto, Captacao
from ...utils import pc_quote

class IncentivadorQuery(Query):

    group_by_fields = (
        Interessado.Nome,
        Interessado.Cidade,
        Interessado.Uf,
        Interessado.Responsavel,
        Interessado.CgcCpf,
        Interessado.tipoPessoa,
    )

    labels_to_fields = {
        'nome': Interessado.Nome,
        'municipio': Interessado.Cidade,
        'UF': Interessado.Uf,
        'responsavel': Interessado.Responsavel,
        'cgccpf': Interessado.CgcCpf,
        'total_doado': func.sum(Captacao.CaptacaoReal),
        'tipo_pessoa': Interessado.tipoPessoa,
    }

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

        return query.group_by(*self.group_by_fields)

class DoacaoQuery(Query):
    query_fields = (
        Captacao.PRONAC,
        Captacao.CaptacaoReal.label('valor'),
        Captacao.data_recibo.label('data_recibo'),
        Projeto.NomeProjeto.label('nome_projeto'),
        Captacao.CgcCpfMecena.label('cgccpf'),
        Interessado.Nome.label('nome_doador'),
    )

    def query(self, cgccpf, limit=100, offset=0):
        query = (
            self.raw_query(*self.query_fields)
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
        )
        if cgccpf is not None:
            query =  query.filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))
        return query

    def total(self, cgccpf):
        total = func.sum(Captacao.CaptacaoReal).label('total_doado')
        return (
            self.raw_query(total)
                .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
                .filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))
        )

