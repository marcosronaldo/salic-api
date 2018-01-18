import logging

from flask import current_app

from .models import CaptacaoQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import SalicResource
from ..serialization import listify_queryset
from ...app.security import encrypt

log = logging.getLogger('salic-api')


class Captacao(SalicResource):
    def build_links(self, args={}):

        self.projetos_links = []

        for PRONAC in args['projetos_PRONAC']:
            link = current_app.config['API_ROOT_URL'] + 'projetos/%s/' % PRONAC
            self.projetos_links.append(link)

        self.incentivador_links = []

        for incentivador_id in args['incentivador_ids']:
            url_id = encrypt(incentivador_id)
            link = current_app.config['API_ROOT_URL'] + \
                   'incentivadores/?url_id=%s' % url_id
            self.projetos_links.append(link)

    def hal_builder(self, data, args=None):

        hal_data = {}
        captacoes = []

        for index in range(len(data['captacoes'])):

            captacao = data['captacoes'][index]

            projeto_link = self.projetos_links[index]
            incentivador_link = self.incentivador_links[index]

            captacao['_links'] = {}
            captacao['_links']['projeto'] = projeto_link
            captacao['_links']['incentivador'] = incentivador_link

        data['_embedded'] = {'captacoes': captacoes}
        del data['captacoes']

        return data


    def get(self, PRONAC):

        try:
            results = CaptacaoQuery().all(PRONAC=PRONAC)
        except Exception as e:
            log.error(str(e))
            result = {
                'message': 'internal error',
                'message_code': 13,
                'more': 'something is broken'
            }
            return self.render(result, status_code=503)

        if len(results) == 0:
            results = {
                'message': 'No funding info was found with your criteria',
                'message_code': 11
            }
            return self.render(results, status_code=404)

        data = listify_queryset(results)

        projetos_PRONAC = []
        incentivador_ids = []

        for captacao in data:
            captacao["cgccpf"] = remove_blanks(captacao['cgccpf'])
            incentivador_ids.append(captacao['cgccpf'])
            projetos_PRONAC.append(captacaos_ids)

            captacao["cgccpf"] = cgccpf_mask(captacao["cgccpf"])

        self.build_links(
            args={
                'projetos_PRONAC': projetos_PRONAC,
                'incentivador_ids': incentivador_ids
            })

        return self.render(data)
