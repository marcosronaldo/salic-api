from .models import PreProjetoQuery
from .pre_projeto_detail import PreProjetoDetail
from ..resource_base import *
from ..sanitization import sanitize
from ..serialization import listify_queryset


class PreProjetoList(ListResource):
    query_class = PreProjetoQuery
    resource_path = 'propostas'
    embedding_field = 'propostas'
    detail_resource_class = PreProjetoDetail
    detail_pk = 'id'

    sort_fields = {
        'nome', 'id', 'data_inicio', 'data_termino', 'data_aceite',
        'data_arquivamento',
    }
    filter_fields = {
        'id', 'nome', 'data_inicio', 'data_termino'
    }
