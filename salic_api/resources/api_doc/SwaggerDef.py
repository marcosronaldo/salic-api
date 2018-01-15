from flask import current_app as app

from ..resource_base import ResourceBase
from ...utils.log import Log


class SwaggerDef(ResourceBase):
    def get(self):
        try:
            swagger_file = open(app.config['SWAGGER_DEF_PATH'])
        except Exception:
            Log.error(
                'error trying to open swagger definition file under the path:  \"%s\"' %
                app.config['SWAGGER_DEF_PATH'])
            result = {
                'message': 'internal error',
                'message_code': 13,
                'more': 'something is broken'
            }
            return self.render(result, status_code=503)

        def_data = swagger_file.read()

        return self.render(def_data, raw=True)
