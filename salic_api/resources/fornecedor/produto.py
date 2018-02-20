from flask import current_app
from .query import ProductQuery
from ..resource import DetailResource, ListResource
from ...utils import encrypt, decrypt


class ProdutoDetail(DetailResource):

    def hal_links(self, result):
        fornecedor_id = self.args['fornecedor_id']
        return {
            'fornecedor': self.url('/fornecedores/%s' % fornecedor_id),
        }

class Produto(ListResource):
    query_class = ProductQuery
    embedding_field = 'produtos'
    detail_resource_class = ProdutoDetail
    detail_pk = 'cgccpf'

    def build_query_args(self):
        args = super().build_query_args()
        fornecedor_id = args.pop('fornecedor_id')
        args['cgccpf'] = decrypt(fornecedor_id)
        return args

    @property
    def resource_path(self):
        return "%s/%s/%s" % ("fornecedores", self.args['fornecedor_id'], 'produtos')
