from .query import PreProjetoQuery
from ..resource import DetailResource


class PreProjetoDetail(DetailResource):
    query_class = PreProjetoQuery
    resource_path = 'propostas'
    csv_columns = [
        'impacto_ambiental', 'ficha_tecnica', 'data_termino', 'id',
        'mecanismo', 'data_arquivamento', 'data_inicio', 'democratizacao',
        'data_aceite', 'sinopse', 'nome', 'estrategia_execucao',
        'especificacao_tecnica', 'acessibilidade', 'objetivos', 'etapa',
        'resumo', 'justificativa'
    ]
    strip_html_fields = {
        'etapa', 'resumo', 'democratizacao', 'acessibilidade', 'justificativa',
        'objetivos', 'sinopse', 'especificacao_tecnica', 'ficha_tecnica',
        'estrategia_execucao', 'impacto_ambiental'
    }

    def hal_links(self, result):
        return {'self': self.url('/propostas/{}'.format(self.args['id']))}
