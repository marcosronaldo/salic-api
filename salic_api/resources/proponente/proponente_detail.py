from salic_api.app.security import decrypt
from .models import ProponenteQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import DetailResource


class ProponenteDetail(DetailResource):
    query_class = ProponenteQuery
    resource_path = 'proponentes'

    sort_fields = ['total_captado']

    def hal_links(self, result):
        proponente_id = self.args['proponente_id']
        return {
            'self': self.url('/proponentes/%s' % proponente_id),
            'projetos': self.url('/projetos/?proponente_id=%s' % proponente_id)
        }

    def build_query_args(self):
        args = dict(self.args)
        proponente_id = args.pop('proponente_id')
        args['cgccpf'] = decrypt(proponente_id)
        return args

    def prepare_result(self, result):
        result["cgccpf"] = remove_blanks(str(result["cgccpf"]))
        result["cgccpf"] = cgccpf_mask(result["cgccpf"])
