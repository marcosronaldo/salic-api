import os

from ..resource import ListResource

dirname = os.path.dirname
SWAGGER_FILE = 'swagger_specification_PT-BR.json'
SWAGGER_DEF_PATH = os.path.join(dirname(dirname(__file__)), SWAGGER_FILE)
SWAGGER_DEF = None


class SwaggerDef(ListResource):
    def get(self):
        global SWAGGER_DEF

        if SWAGGER_DEF is None:
            with open(SWAGGER_DEF_PATH) as F:
                SWAGGER_DEF = F.read()

        return self.render(SWAGGER_DEF, raw=True)
