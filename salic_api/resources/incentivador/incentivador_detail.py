from .query import IncentivadorQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource import DetailResource
from ...utils import decrypt


class IncentivadorDetail(DetailResource):
    query_class = IncentivadorQuery
    resource_path = 'incentivadores'
    csv_columns = ['cgccpf', 'nome', 'responsavel', 'tipo_pessoa', 'UF',
                   'municipio', 'total_doado']

    def hal_links(self, result):
        encrypted_id = self.args['incentivador_id']
        url = self.url('/incentivadores/%s' % encrypted_id)
        return {
            'self': url,
            'doacoes': url + '/doacoes'
        }

    def build_query_args(self):
        args = super().build_query_args()
        incentivador_id = args.pop('incentivador_id')
        args['cgccpf'] = decrypt(incentivador_id)
        return args

    def prepare_result(self, result):
        result["cgccpf"] = remove_blanks(str(result["cgccpf"]))
        result["cgccpf"] = cgccpf_mask(result["cgccpf"])
