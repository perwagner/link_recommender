import json
from pprint import pprint
import pytest


@pytest.mark.api
@pytest.mark.recommender
def test_service_is_up(app):
    url = '/api/v1/status'

    with app.test_client() as client:
        resp = client.get(url)

    assert resp.status_code == 200


@pytest.mark.api
@pytest.mark.recommender
def test_recommender_endpoint_works(app):
    url = '/api/v1/recommender/10001'

    with app.test_client() as client:
        resp = client.get(url)

    assert resp.status_code == 200


@pytest.mark.api
@pytest.mark.recommender
def test_recommender_returns_recommended_sites_success(app):
    url = '/api/v1/recommender/34858'

    with app.test_client() as client:
        resp = client.get(url)

    data = json.loads(resp.data)
    print(data)

    assert data == ['/msdownload', '/windows']


@pytest.mark.api
@pytest.mark.recommender
def test_recommender_user_without_history(app):
    url = '/api/v1/recommender/1'

    with app.test_client() as client:
        resp = client.get(url)

    data = json.loads(resp.data)
    print(data)

    assert data == ['/msdownload', '/ie', '/search', '/isapi', '/products']   