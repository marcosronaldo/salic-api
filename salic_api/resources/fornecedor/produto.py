from .query import ProductQuery
from ..resource import DetailResource, ListResource
from ...utils import decrypt


class ProdutoDetail(DetailResource):

    def hal_links(self, result):
        """
        Responsable for generate Projetos and Fornecedores' urls
        """
        fornecedor_id = self.args['fornecedor_id']
        return {
            'projeto': self.url('/projetos/%s' % result['PRONAC']),
            'fornecedor': self.url('/fornecedores/%s' % fornecedor_id),
        }


class Produto(ListResource):
    query_class = ProductQuery
    embedding_field = 'produtos'
    detail_resource_class = ProdutoDetail
    detail_pk = 'cgccpf'
    request_args = {'fornecedor_id', 'limit', 'offset', 'format'}

    default_sort_field = 'data_pagamento'
    sort_fields = {
        'data_pagamento'
    }

    def build_query_args(self):
        args = super().build_query_args()
        fornecedor_id = args.pop('fornecedor_id')
        args['cgccpf'] = decrypt(fornecedor_id)
        return args

    @property
    def resource_path(self):
        return "%s/%s/%s" % (
            "fornecedores", self.args['fornecedor_id'], 'produtos')
