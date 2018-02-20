from flask import current_app
from .query import ProductQuery
from ..resource import ListResource
from ...utils import encrypt, decrypt


class Produto(ListResource):
    query_class = ProductQuery
    embedding_field = 'produtos'

    def build_query_args(self):
        args = super().build_query_args()
        fornecedor_id = args.pop('fornecedor_id')
        args['cgccpf'] = decrypt(fornecedor_id)
        return args

    @property
    def resource_path(self):
        return "%s/%s/%s" % ("fornecedores", self.args['fornecedor_id'], 'produtos')

    # def build_links(self, args={}):

    #     self.projetos_links = []

    #     for PRONAC in args['projetos_PRONAC']:
    #         link = current_app.config['API_ROOT_URL'] + 'projetos/%s/' % PRONAC
    #         self.projetos_links.append(link)

    #     self.fornecedor_links = []

    #     for fornecedor_id in args['fornecedor_id']:
    #         url_id = encrypt(fornecedor_id)
    #         link = current_app.config['API_ROOT_URL'] + \
    #             'fornecedores/?url_id=%s' % url_id
    #         self.projetos_links.append(link)

    # def hal_builder(self, data, args=None):
    #     produtos = []

    #     for index in range(len(data['produtos'])):

    #         produtos = data['produtos'][index]

    #         projeto_link = self.projetos_links[index]
    #         fornecedor_link = self.fornecedor_links[index]

    #         produtos['_links'] = {}
    #         produtos['_links']['projeto'] = projeto_link
    #         produtos['_links']['fornecedor'] = fornecedor_link

    #     data['_embedded'] = {'produtos': produtos}
    #     del data['produtos']

    #     return data
