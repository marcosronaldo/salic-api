import os

import pytest

import salic_api.utils
from salic_api.app import create_app

salic_api.utils.STATIC_IV = salic_api.utils.TESTING_IV

DIRNAME = os.path.dirname(__file__)
os.environ['TESTING'] = 'true'


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def example():
    return lambda x: os.path.join(DIRNAME, 'restapi', 'examples', x)
