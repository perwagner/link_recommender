from flask_restful import Resource
from flask import current_app, request
import os
from . import api
from app.api_v1.recommender_engine.recommender import create_website_recommendation
from app.api_v1.recommender_engine.recommender import read_training_data


class Status(Resource):
    def get(self):
        response = {
            'status': 'the service is running',
        }

        return response, 200


class Recommender(Resource):
    def get(self, user_id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(dir_path, './recommender_engine/anonymous-msweb.data')
        data = read_training_data(data_path)
        rec = create_website_recommendation(user_id, data)

        return rec, 200


api.add_resource(Status, '/status', '/')
api.add_resource(Recommender, '/recommender/<int:user_id>')

