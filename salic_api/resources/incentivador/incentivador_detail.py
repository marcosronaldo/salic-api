from .models import IncentivadorQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import DetailResource
from ...utils import decrypt


class IncentivadorDetail(DetailResource):
    query_class = IncentivadorQuery
    resource_path = 'incentivadores'

    def hal_links(self, result):
        encrypted_id = self.args['incentivador_id']
        url = self.url('/incentivadores/%s' % encrypted_id)
        return {
            'self': url,
            'doacoes': url + '/doacoes'
        }

    def build_query_args(self):
        args = dict(self.args)
        incentivador_id = args.pop('incentivador_id')
        args['cgccpf'] = decrypt(incentivador_id)
        return args

    def prepare_result(self, result):
        result["cgccpf"] = remove_blanks(str(result["cgccpf"]))
        result["cgccpf"] = cgccpf_mask(result["cgccpf"])
