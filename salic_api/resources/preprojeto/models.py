from sqlalchemy import desc
from ..query import Query, filter_query_like, filter_query
from ..shared_models import PreProjeto, Mecanismo


class PreProjetoQuery(Query):
    query_fields = (
        PreProjeto.NomeProjeto.label('nome'),
        PreProjeto.idPreProjeto.label('id'),
        PreProjeto.data_inicio_execucao.label('data_inicio'),
        PreProjeto.data_final_execucao.label('data_termino'),
        PreProjeto.data_aceite.label('data_aceite'),
        PreProjeto.data_arquivamento.label('data_arquivamento'),
        PreProjeto.Acessibilidade.label('acessibilidade'),
        PreProjeto.Objetivos.label('objetivos'),
        PreProjeto.Justificativa.label('justificativa'),
        PreProjeto.DemocratizacaoDeAcesso.label('democratizacao'),
        PreProjeto.EtapaDeTrabalho.label('etapa'),
        PreProjeto.FichaTecnica.label('ficha_tecnica'),
        PreProjeto.ResumoDoProjeto.label('resumo'),
        PreProjeto.Sinopse.label('sinopse'),
        PreProjeto.ImpactoAmbiental.label('impacto_ambiental'),
        PreProjeto.EspecificacaoTecnica.label('especificacao_tecnica'),
        PreProjeto.EstrategiadeExecucao.label('estrategia_execucao'),
        Mecanismo.Descricao.label('mecanismo'),
    )

    def query(self, limit=1, offset=0, id=None, nome=None, data_inicio=None,
              data_termino=None, sort_field=None, sort_order=None):
        query = self.raw_query(*self.query_fields)
        query = query.select_from(PreProjeto)
        query = query.join(Mecanismo)
        query = query.order_by(PreProjeto.idPreProjeto)
        query = filter_query_like(query, {
            PreProjeto.NomeProjeto: nome,
        })
        query = filter_query(query, {
            PreProjeto.idPreProjeto: id,
            PreProjeto.DtInicioDeExecucao: data_inicio,
            PreProjeto.DtFinalDeExecucao: data_termino,
        })

        sort_field = self.sort_field(sort_field)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_field))
        else:
            query = query.order_by(sort_field)
        return query

    def sort_field(self, sort_field=None):
        sorting_fields = {
            'nome': PreProjeto.NomeProjeto,
            'id': PreProjeto.idPreProjeto,
            'data_inicio': PreProjeto.DtInicioDeExecucao,
            'data_termino': PreProjeto.DtFinalDeExecucao,
            'data_aceite': PreProjeto.dtAceite,
            'data_arquivamento': PreProjeto.DtArquivamento,
        }
        return sorting_fields[sort_field or 'data_inicio']
