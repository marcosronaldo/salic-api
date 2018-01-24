from .models import PreProjetoQuery
from ..resource_base import *
from ..sanitization import sanitize
from ..serialization import listify_queryset


class PreProjetoDetail(DetailResource):
    query_class = PreProjetoQuery
    resource_path = 'propostas'

    def hal_links(self, result):
        return {
            'self': self.url('/propostas/{}'.format(self.args['id']))
        }
