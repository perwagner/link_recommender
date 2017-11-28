from flask_restful import Resource
from flask import current_app, request
import os
from sqlalchemy.exc import ProgrammingError
from . import api
from app.api_v1.recommender_engine.recommender import create_website_recommendation
from app.api_v1.recommender_engine.recommender import read_training_data
from app.model import User, db
from app.factories import UserFactory
import logging
from faker import Faker
fake = Faker()

class Status(Resource):
    def get(self):
        response = {
            'status': 'the service is running',
        }

        return response, 200


class UserAPI(Resource):
    def get(self):
        users = User.query.all()

        return len(users)

    def post(self):
        try:
            UserFactory()
            return 'created', 200
        except Exception as E:
            logging.error(E)
            return 'error', 404


class ResetAPI(Resource):
    def get(self):
        db.drop_all()
        db.create_all()
        for i in range(10):
            UserFactory()

        return 'full reset'

    def delete(self):
        db.drop_all()
        return 'delete_all()'

    def post(self):
        db.create_all()
        return 'create_all()'


class Recommender(Resource):
    def get(self, user_id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(dir_path, './recommender_engine/anonymous-msweb.data')
        data = read_training_data(data_path)
        rec = create_website_recommendation(user_id, data)

        return rec, 200


class ProductRecommender(Resource):
    def get(self, user, product):
        print("SSDFSFDSF")
        try:
            user = User.query.filter_by(username='peter').first()
        except ProgrammingError as E:
            print('programming error:')
            print(E)
        except Exception as E:
            print(E)

        return "SUCCESS"


api.add_resource(UserAPI, '/user')
api.add_resource(ResetAPI, '/reset')
api.add_resource(Status, '/status', '/')
api.add_resource(Recommender, '/recommender/<int:user_id>')
api.add_resource(ProductRecommender , '/recommender/product/<int:user>/<int:product>')
