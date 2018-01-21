from salic_api.app.security import decrypt
from salic_api.app.security import encrypt
from .models import DoacaoQuery
from ..format_utils import remove_blanks, cgccpf_mask
from ..resource_base import *
from ..serialization import listify_queryset


class Doacao(ListResource):
    def build_links(self, args={}):

        query_args = '&'
        incentivador_id = args['incentivador_id']
        last_offset = self.last_offset(args['n_records'], args['limit'])
        self.links['self'] += incentivador_id + '/doacoes/'

        for arg in request.args:
            if arg != 'limit' and arg != 'offset':
                query_args += arg + '=' + request.args[arg] + '&'

        if args['offset'] - args['limit'] >= 0:
            self.links["prev"] = self.links["self"] + '?limit=%d&offset=%d' % (
                args['limit'], args['offset'] - args['limit']) + query_args

        if args['offset'] + args['limit'] <= last_offset:
            self.links["next"] = self.links["self"] + '?limit=%d&offset=%d' % (
                args['limit'], args['offset'] + args['limit']) + query_args

        self.links["first"] = self.links["self"] + \
                              '?limit=%d&offset=0' % (
                                  args['limit']) + query_args
        self.links["last"] = self.links["self"] + \
                             '?limit=%d&offset=%d' % (
                                 args['limit'], last_offset) + query_args
        self.links["self"] += '?limit=%d&offset=%d' % (
            args['limit'], args['offset']) + query_args

        self.doacoes_links = []

        for doacao in args['doacoes']:
            doacao_links = {}
            doacao_links['projeto'] = current_app.config['API_ROOT_URL'] + \
                                      'projetos/%s' % doacao['PRONAC']
            incentivador_id = encrypt(doacao['cgccpf'])
            doacao_links['incentivador'] = current_app.config['API_ROOT_URL'] + \
                                           'incentivadores/%s' % incentivador_id

            self.doacoes_links.append(doacao_links)

    def __init__(self):
        super(Doacao, self).__init__()

        self.links = {
            "self": current_app.config['API_ROOT_URL'] + 'incentivadores/',
        }

        def hal_builder(data, args={}):

            total = args['total']
            count = len(data)

            hal_data = {'_links': '', 'total': total, 'count': count}

            hal_data['_links'] = self.links

            hal_data['_embedded'] = {'doacoes': ''}

            for index in range(len(data)):
                doacao = data[index]
                doacao['_links'] = self.doacoes_links[index]

            hal_data['_embedded']['doacoes'] = data

            return hal_data

        self.to_hal = hal_builder

    def get(self, incentivador_id):

        cgccpf = decrypt(incentivador_id)

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
        else:
            limit = current_app.config['LIMIT_PAGING']

        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = current_app.config['OFFSET_PAGING']

        try:
            results, n_records = DoacaoQuery().query(limit, offset, cgccpf)
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
                'message': 'No funding info was found with your criteria',
                'message_code': 11
            }

            return self.render(result, status_code=404)

        headers = {'X-Total-Count': n_records}

        data = listify_queryset(results)

        for doacao in data:
            doacao["cgccpf"] = remove_blanks(doacao['cgccpf'])

        data = self.unique_cgccpf(cgccpf, data)

        self.build_links(args={
            'incentivador_id': incentivador_id, 'doacoes': data,
            'limit': limit, 'offset': offset, 'n_records': n_records
        })

        for doacao in data:
            doacao["cgccpf"] = cgccpf_mask(doacao["cgccpf"])

        return self.render(data, headers)
