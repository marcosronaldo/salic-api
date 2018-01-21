from .models import AreaQuery
from ..resource_base import ListResource


class Area(ListResource):
    resource_path = 'projetos/areas'
    query_class = AreaQuery
    embedding_field = 'areas'

    def hal_item_links(self, item):
        link = self.url('/projetos/?area=%s' % item['codigo'])
        return {'self': link}
