import json
from pprint import pprint
import pytest
import pandas as pd
from app.api_v1.recommender_engine.recommender import *
import os 


@pytest.mark.recommender_engine
def test_read_training_data_failure():
    data = read_training_data('./something.txt')

    assert data.empty


@pytest.mark.recommender_engine
def test_read_training_data_success():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_data = os.path.join(dir_path, 'testdata.data')
    data = read_training_data(test_data)

    assert not data.empty
    assert data.shape == (131659, 5)


@pytest.mark.recommender_engine
def test_create_attributes(create_testdata):
    attr = create_attributes(create_testdata)

    print(attr)

    assert list(attr.columns.values) == ['ID', 'title', 'url']


@pytest.mark.recommender_engine
def test_create_top_visited_websites(create_testdata):
    raw_data = create_testdata
    top_websites = create_top_visited_websites(raw_data, 100)

    assert len(list(top_websites)) == 104


@pytest.mark.recommender_engine
def test_get_websites_with_total_visits(create_testdata):
    website_visits = get_websites_with_total_visits(create_testdata)

    assert website_visits.shape == (285, 4)


@pytest.mark.under_test
@pytest.mark.recommender_engine
def test_get_webvisits(create_testdata):
    webvisits = get_webvisits(create_testdata)

    assert list(webvisits.columns.values) == ['user', 'ID']
    assert webvisits.shape == (98654, 2)


@pytest.mark.recommender_engine
def test_get_website_recommendation_34858(create_testdata):
    raw_data = create_testdata
    user_id = 34858
    recommendations = create_website_recommendation(
        user_id,
        raw_data
        )

    assert recommendations == ['/msdownload', '/windows']



@pytest.mark.recommender_engine
def test_get_website_recommendation_37130(create_testdata):
    raw_data = create_testdata
    user_id = 37130
    recommendations = create_website_recommendation(
        user_id,
        raw_data
        )

    assert recommendations == ['/products', '/excel']


@pytest.mark.recommender_engine
def test_get_website_recommendation_user_has_no_history(create_testdata):
    raw_data = create_testdata
    user_id = 99
    recommendations = create_website_recommendation(
        user_id,
        raw_data
        )

    assert recommendations == ['/msdownload', '/ie', '/search', '/isapi', '/products']










