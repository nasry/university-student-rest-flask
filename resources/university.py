#!/usr/bin/env python3

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask_restful import Resource, reqparse
from flaskapp.models.university import UniversityModel
from flask_jwt_extended import jwt_required
from flaskapp.util.logger import create_logger

class University(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def post(self):
        
        data = University.parser.parse_args()

        if UniversityModel.find_by_name(data['name']):
            return {'message': "A university with name '{}' already exists.".format(data['name'])}, 400

        university = UniversityModel(data["name"])
        try:
            university.save_to_db()
        except:
            return {"message": "An error occurred while creating the university."}, 500

        return university.json(), 201

class UniversityByName(Resource):

    def __init__(self):
        self.logger = create_logger()

    def get(self, name):
        if not name:
            return {"message": "University name is required"}, 400
        university = UniversityModel.find_by_name(name)
        if university:
            return university.json()
        return {'message': 'University not found'}, 404

    @jwt_required()
    def delete(self, name):
        university = UniversityModel.find_by_name(name)
        if university:
            university.delete_from_db()

        return {'message': 'University deleted'}


class UniversityList(Resource):
    def get(self):
        return {'universities': [university.json() for university in UniversityModel.query.all()]}
