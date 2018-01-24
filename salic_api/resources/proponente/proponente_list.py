from .models import ProponenteQuery
from .proponente_detail import ProponenteDetail
from ..resource_base import ListResource
from ...utils import encrypt


class ProponenteList(ListResource):
    query_class = ProponenteQuery
    resource_path = 'proponentes'
    embedding_field = 'proponentes'
    detail_resource_class = ProponenteDetail
    detail_pk = 'cgccpf'

    sort_fields = {
        'total_captado'
    }

    filter_fields = {
        'nome', 'cgccpf', 'proponente_id', 'municipio', 'UF', 'tipo_pessoa'
    }

    def prepared_detail_object(self, item):
        detail_resource = super().prepared_detail_object(item)
        detail_resource.args['proponente_id'] = encrypt(item['cgccpf'])
        return detail_resource
