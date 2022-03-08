from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user
from flaskapp.models.user import UserModel
from flaskapp.util.encoder import AlchemyEncoder
import json
from flaskapp.util.logger import create_logger


class UserSignIn(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field is required')
    parser.add_argument('password', type=str, required=True, help='This field is required')

    def post(self):
        data = UserSignIn.parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {'message': 'Wrong username or password.'}, 401

        access_token = create_access_token(identity = json.dumps(user, cls=AlchemyEncoder))

        return jsonify(access_token = access_token)

class User(Resource):

    @jwt_required()
    def get(self):
        # current_user contains the connected user
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            username=current_user.username,
        )


class UserSignUp(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field is required')
    parser.add_argument('password', type=str, required=True, help='This field is required')

    def post(self):
        data = UserSignUp.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User already created.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
