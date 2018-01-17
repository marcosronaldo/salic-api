import os

import pytest
from flask import current_app

from salic_api.app import create_app_

DIRNAME = os.path.dirname(__file__)


@pytest.fixture
def app():
    app = create_app_()
    app.testing = True
    return app

@pytest.fixture
def example():
    return lambda x: os.path.join(DIRNAME, 'restapi', 'examples', x)
