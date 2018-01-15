from .models import SegmentoModelObject
from ..app import app
from ..resource_base import ResourceBase
from ..serialization import listify_queryset


class Segmento(ResourceBase):
    def __init__(self):
        super(Segmento, self).__init__()

        def hal_builder(data, args={}):
            hal_data = {
                '_links': {
                    'self': app.config['API_ROOT_URL'] + 'projetos/segmentos/'
                }
            }

            for segmento in data:
                link = app.config['API_ROOT_URL'] + \
                       'projetos/?segmento=%s' % segmento['codigo']
                segmento['_links'] = {'self': link}

            hal_data['_embedded'] = {'segmentos': data}

            return hal_data

        self.to_hal = hal_builder

    def get(self):
        try:
            result = SegmentoModelObject().all()
        except:
            result = {
                'message': 'internal error',
                'message_code': 13
            }
            return self.render(result, status_code=503)

        result = listify_queryset(result)
        result = sorted(result)
        return self.render(result)
