import pytest

from src import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app('flask-test.cfg')
    return app
