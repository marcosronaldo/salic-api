from salic_api.app.security import decrypt
from .models import Incentivador
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import ResourceBase
from ..serialization import listify_queryset
from flask import current_app
from ...utils.log import Log


class IncentivadorDetail(ResourceBase):
    def build_links(self, args={}):
        incentivador_id = args['incentivador_id']
        self.links['self'] += incentivador_id
        self.links['doacoes'] = self.links['self'] + '/doacoes'

    def __init__(self):
        self.tipos_pessoa = {'1': 'fisica', '2': 'juridica'}
        super(IncentivadorDetail, self).__init__()

        self.links = {
            "self": current_app.config['API_ROOT_URL'] + 'incentivadores/'
        }

        def hal_builder(data, args={}):
            hal_data = data
            hal_data['_links'] = self.links

            return hal_data

        self.to_hal = hal_builder

    def get(self, incentivador_id):

        cgccpf = decrypt(incentivador_id)

        try:
            results, n_records = Incentivador().all(
                limit=1, offset=0, cgccpf=cgccpf)

        except Exception as e:
            Log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
                'more': 'something is broken'
            }
            return self.render(result, status_code=503)

        if n_records == 0 or len(results) == 0:

            result = {
                'message': 'No donator was found with your criteria',
                'message_code': 11
            }

            return self.render(result, status_code=404)

        headers = {}
        data = listify_queryset(results)
        incentivador = data[0]
        incentivador["cgccpf"] = remove_blanks(str(incentivador["cgccpf"]))
        self.build_links(args={'incentivador_id': incentivador_id})
        incentivador["cgccpf"] = cgccpf_mask(incentivador["cgccpf"])
        return self.render(incentivador, headers)
