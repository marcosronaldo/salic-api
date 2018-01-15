import os

import pytest

from flask import current_app

DIRNAME = os.path.dirname(__file__)


@pytest.fixture
def app():
    return current_app()


@pytest.fixture
def example():
    return lambda x: os.path.join(DIRNAME, 'restapi', 'examples', x)
