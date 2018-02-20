from .query import SegmentoQuery
from ..resource import ListResource


class Segmento(ListResource):
    resource_path = 'projetos/segmentos'
    query_class = SegmentoQuery
    has_pagination = False
    embedding_field = 'segmento'

    def hal_embedded(self, data, kwargs):
        for segmento in data:
            link = self.url('/projetos/?segmento=%s' % segmento['codigo'])
            segmento['_links'] = {'self': link}
        return {'segmentos': sorted(data)}
