from ..model_base import QueryBase
from ..shared_models import PreProjeto, Mecanismo


class PreProjetoModelObject(QueryBase):
    def __init__(self):
        super(PreProjetoModelObject, self).__init__()

    def all(self, limit, offset, id=None, nome=None, data_inicio=None,
            data_termino=None, extra_fields=False):

        start_row = offset
        end_row = offset + limit

        if extra_fields:
            additional_fields = (
                PreProjeto.Acessibilidade.label('acessibilidade'),
                PreProjeto.Objetivos.label('objetivos'),
                PreProjeto.Justificativa.label('justificativa'),
                PreProjeto.DemocratizacaoDeAcesso.label('democratizacao'),
                PreProjeto.EtapaDeTrabalho.label('etapa'),
                PreProjeto.FichaTecnica.label('ficha_tecnica'),
                PreProjeto.ResumoDoProjeto.label('resumo'),
                PreProjeto.Sinopse.label('sinopse'),
                PreProjeto.ImpactoAmbiental.label('impacto_ambiental'),
                PreProjeto.EspecificacaoTecnica.label(
                    'especificacao_tecnica'),
                PreProjeto.EstrategiadeExecucao.label(
                    'estrategia_execucao'),
            )
        else:
            additional_fields = ()

        res = self.sql_connector.session.query(
            PreProjeto.NomeProjeto.label('nome'),
            PreProjeto.idPreProjeto.label('id'),
            PreProjeto.DtInicioDeExecucao.label('data_inicio'),
            PreProjeto.DtFinalDeExecucao.label('data_termino'),
            PreProjeto.dtAceite.label('data_aceite'),
            PreProjeto.DtArquivamento.label('data_arquivamento'),

            Mecanismo.Descricao.label('mecanismo'),

            *additional_fields

        ).join(Mecanismo) \
            .order_by(PreProjeto.idPreProjeto)

        if nome is not None:
            res = res.filter(
                PreProjeto.NomeProjeto.like('%' + nome + '%'))

        if id is not None:
            res = res.filter(PreProjeto.idPreProjeto == id)

        if data_inicio is not None:
            res = res.filter(PreProjeto.DtInicioDeExecucao == data_inicio)

        if data_termino is not None:
            res = res.filter(PreProjeto.DtFinalDeExecucao == data_termino)

        total_records = self.count(res)

        res = res.slice(start_row, end_row)

        return res.all(), total_records
