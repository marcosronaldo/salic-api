from .models import AreaQuery
from ..resource_base import ListResource


class Area(ListResource):
    resource_path = 'projetos/areas'
    query_class = AreaQuery

    def hal_embedded(self, data, args):
        for area in data:
            link = self.url('/projetos/?area=%s' % area['codigo'])
            area['_links'] = {'self': link}
        return {'areas': data}
