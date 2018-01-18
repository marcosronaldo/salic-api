from .models import AreaQuery
from ..resource_base import SalicResource


class Area(SalicResource):
    resource_path = 'projetos/areas'
    query_class = AreaQuery

    def get_hal_embedded(self, data, args):
        for area in data:
            link = self.get_url('/projetos/?area=%s' % area['codigo'])
            area['_links'] = {'self': link}
        return {'areas': data}
