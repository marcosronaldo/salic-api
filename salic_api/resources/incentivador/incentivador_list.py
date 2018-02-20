from .incentivador_detail import IncentivadorDetail
from .query import IncentivadorQuery
from ..resource import ListResource
from ...utils import encrypt


class IncentivadorList(ListResource):
    query_class = IncentivadorQuery
    resource_path = 'incentivadores'
    embedding_field = 'incentivadores'
    detail_resource_class = IncentivadorDetail
    detail_pk = 'cgccpf'

    sort_fields = {
        'total_doado'
    }

    filter_fields = {
        'nome', 'incentivador_id', 'cgccpf', 'municipio', 'UF', 'tipo_pessoa',
        'PRONAC'
    }

    def prepared_detail_object(self, item):
        detail_resource = super().prepared_detail_object(item)
        detail_resource.args['incentivador_id'] = encrypt(item['cgccpf'])
        return detail_resource
