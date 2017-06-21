import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import ProductModelObject
from ..serialization import listify_queryset
from ..security import decrypt, encrypt
from ..format_utils import remove_blanks, cgccpf_mask


class Produto(ResourceBase):

     def build_links(self, args = {}):

        query_args = '&'
        fornecedor_id = args['fornecedor_id']

        last_offset = self.get_last_offset(args['n_records'], args['limit'])

        self.links['self'] += fornecedor_id + '/produtos/'

        for arg in request.args:
            if arg!= 'limit' and arg != 'offset':
                query_args+=arg+'='+request.args[arg]+'&'

        if args['offset']-args['limit'] >= 0:
            self.links["prev"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['offset']-args['limit'])+query_args
            

        if args['offset']+args['limit'] <= last_offset:
            self.links["next"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['offset']+args['limit'])+query_args
        
        self.links["first"] = self.links["self"] + '?limit=%d&offset=0'%(args['limit'])+query_args
        self.links["last"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], last_offset)+query_args
        self.links["self"] += '?limit=%d&offset=%d'%(args['limit'], args['offset'])+query_args

        self.produtos_links = []

        for produto in args['produtos']:
                produto_links = {}
                produto_links['projeto'] = app.config['API_ROOT_URL'] + 'projetos/%s'%produto['PRONAC']
                produto_links['fornecedor'] = app.config['API_ROOT_URL'] + 'fornecedores/%s'%fornecedor_id

                self.produtos_links.append(produto_links)

     def __init__(self):
        super (Produto, self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'fornecedores/',
        }

        def hal_builder(data, args = {}):

            total = args['total']
            count = len(data)

            hal_data = {'_links' : self.links, 'total' : total, 'count' : count}

            hal_data['_embedded'] = {'produtos' : ''}

            for index in range(len(data)):
                produto = data[index]
                produto['_links'] = self.produtos_links[index]
                
            hal_data['_embedded']['produtos'] = data

            return hal_data

        self.to_hal = hal_builder


     def get(self, fornecedor_id):
      
        cgccpf = decrypt(fornecedor_id)

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))

            if limit > app.config['LIMIT_PAGING']:
                results = {'message' : 'Max limit paging exceeded',
                        'message_code' : 7
                    }
                return self.render(results, status_code = 405)

        else:
            limit = app.config['LIMIT_PAGING']

        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = app.config['OFFSET_PAGING']

        try:
            results = ProductModelObject().all(limit, offset, cgccpf)
            n_records = ProductModelObject().count(cgccpf)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  17,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        results = listify_queryset(results)

        if n_records == 0 or len(results) == 0:

            result = {'message' : 'No Products were found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {'X-Total-Count' : n_records}

        data = results

        for produto in data:
            produto["cgccpf"] = remove_blanks(produto['cgccpf'])

        data = self.get_unique(cgccpf, data)


        self.build_links(args = {'fornecedor_id' : fornecedor_id, 'produtos' : data,
            'limit' : limit, 'offset' : offset, 'n_records' : n_records})

        for produto in data:
            produto["cgccpf"] = cgccpf_mask(produto["cgccpf"])

        return self.render(data, headers)
