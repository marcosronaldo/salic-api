from .models import FornecedorQuery
from ..resource_base import DetailResource
from ...utils import decrypt


class FornecedorDetail(DetailResource):
    query_class = FornecedorQuery
    resource_path = 'fornecedores'

    def build_query_args(self):
        args = super().build_query_args()
        fornecedor_id = args.pop('fornecedor_id')
        args['cgccpf'] = decrypt(fornecedor_id)
        return args

    def hal_links(self, result):
        fornecedor_id = self.args['fornecedor_id']
        return {
            'self': self.url('/fornecedores/%s' % fornecedor_id),
            'produtos': self.url('/fornecedores/%s/produtos' % fornecedor_id),
        }
