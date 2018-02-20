from .query import FornecedorQuery
from ..resource import ListResource
from .fornecedor_detail import FornecedorDetail
from ...utils import encrypt


class FornecedorList(ListResource):
    query_class = FornecedorQuery
    resource_path = 'fornecedores'
    embedding_field = 'fornecedores'
    detail_resource_class = FornecedorDetail
    detail_pk = 'cgccpf'

    sort_fields = {
        'cgccpf'
    }

    filter_fields = {
        'nome', 'email', 'cgccpf'
    }

    def prepared_detail_object(self, item):
        detail_resource = super().prepared_detail_object(item)
        detail_resource.args['fornecedor_id'] = encrypt(item['cgccpf'])
        return detail_resource
