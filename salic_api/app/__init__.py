from flask import Flask

from .rate_limiting import limiter
from .security import encrypt, decrypt


def create_app_(config_file='development.cfg'):
    from .urls import make_urls
    from .general_config import ENVIRONMENT

    app = Flask(__name__)
    app.config.from_pyfile(ENVIRONMENT)

    make_urls(app)
    return app
