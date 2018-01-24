import logging

from flask import current_app as app

from ..resource_base import ListResource

log = logging.getLogger('salic-api')


class SwaggerDef(ListResource):
    def get(self):
        try:
            swagger_file = open(app.config['SWAGGER_DEF_PATH'])
        except Exception:
            log.error(
                'error trying to open swagger definition file under the path:  \"%s\"' %
                app.config['SWAGGER_DEF_PATH'])
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        def_data = swagger_file.read()

        return self.render(def_data, raw=True)
