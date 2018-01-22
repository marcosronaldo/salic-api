from .models import FornecedordorQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import DetailResource
from ..serialization import listify_queryset
from ...app.security import decrypt


class FornecedorDetail(DetailResource):
    query_class = FornecedordorQuery
    resource_path = 'fornecedores'

    def build_links(self, args={}):
        fornecedor_id = args['fornecedor_id']
        self.links['self'] += fornecedor_id
        self.links['produtos'] = self.links['self'] + '/produtos'

    def build_query_args(self):
        args = dict(self.args)
        fornecedor_id = args.pop('fornecedor_id')
        args['cgccpf'] = decrypt(fornecedor_id)
        return args

    def _get(self, fornecedor_id):
        cgccpf = decrypt(fornecedor_id)

        try:
            results = FornecedordorQuery().query(limit=1, offset=0)
        except Exception as e:
            result = {
                'message': 'internal error',
                'message_code': 13,
                'more': 'something is broken'
            }
            return self.render(result, status_code=503)

        results = listify_queryset(results)

        n_records = len(results)

        if n_records == 0 or len(results) == 0:
            result = {
                'message': 'No supplier was found with your criteria',
                'message_code': 11
            }
            return self.render(result, status_code=404)

        headers = {}
        data = results
        fornecedor = data[0]
        fornecedor["cgccpf"] = remove_blanks(fornecedor["cgccpf"])
        self.build_links(args={'fornecedor_id': fornecedor_id})
        fornecedor["cgccpf"] = cgccpf_mask(fornecedor["cgccpf"])
        return self.render(fornecedor, headers)
