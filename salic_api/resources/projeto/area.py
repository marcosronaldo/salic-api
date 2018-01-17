import logging

from flask import current_app

from .models import AreaModelObject
from ..resource_base import ResourceBase
from ..serialization import listify_queryset

log = logging.getLogger('salic-api')


class Area(ResourceBase):
    def __init__(self):
        super().__init__()
        self.to_hal = self.hal_builder

    def hal_builder(self, data, args={}):
        hal_data = {
            '_links': {
                'self': current_app.config['API_ROOT_URL'] + 'projetos/areas/'
            }
        }

        for area in data:
            link = current_app.config['API_ROOT_URL'] + \
                   'projetos/?area=%s' % area['codigo']
            area['_links'] = {'self': link}

        hal_data['_embedded'] = {'areas': data}
        return hal_data

    def get(self):
        try:
            result = AreaModelObject().all()
        except Exception as e:
            log.error('area not found')
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        result = listify_queryset(result)
        return self.render(result)
