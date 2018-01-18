from .models import SegmentoQuery
from ..resource_base import *


class Segmento(SalicResource):
    resource_path = 'projetos/segmentos'
    query_class = SegmentoQuery

    def get_hal_embedded(self, data, args):
        for segmento in data:
            link = self.get_url('/projetos/?segmento=%s' % segmento['codigo'])
            segmento['_links'] = {'self': link}
        return {'segmentos': sorted(data)}
