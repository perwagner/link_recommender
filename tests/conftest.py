import pytest
from app import create_app
import os, datetime
from app.api_v1.recommender_engine.recommender import read_training_data


@pytest.fixture(autouse=True)
def app(request):
    """Creates a Flask app object fixture"""
    env = os.getenv("ENV") or "local"
    app = create_app(env.lower())

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def create_testdata():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_data = os.path.join(dir_path, 'testdata.data')
    data = read_training_data(test_data)    
    return data
