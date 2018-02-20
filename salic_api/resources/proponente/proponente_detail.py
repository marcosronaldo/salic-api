from .query import ProponenteQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource import DetailResource
from ...utils import decrypt


class ProponenteDetail(DetailResource):
    resource_path = 'proponentes'
    query_class = ProponenteQuery

    # sort_fields = ['total_captado']
    csv_columns = ['cgccpf', 'nome', 'responsavel', 'tipo_pessoa',
                   'UF', 'total_captado', 'municipio']

    def hal_links(self, result):
        proponente_id = self.args['proponente_id']
        return {
            'self': self.url('/proponentes/%s' % proponente_id),
            'projetos': self.url('/projetos/?proponente_id=%s' % proponente_id)
        }

    def build_query_args(self):
        args = super().build_query_args()
        proponente_id = args.pop('proponente_id')
        args['cgccpf'] = decrypt(proponente_id)
        return args

    def prepare_result(self, result):
        result["cgccpf"] = remove_blanks(str(result["cgccpf"]))
        result["cgccpf"] = cgccpf_mask(result["cgccpf"])
