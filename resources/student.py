#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flaskapp.models.student import StudentModel
from flaskapp.util.logger import create_logger

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('age', type=int, required=True, help='This field is required')
    parser.add_argument('university_id', type=int, required=True, help='This field is required')

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def post(self):
        self.logger.info(f'parsed args: {Student.parser.parse_args()}')
        data = Student.parser.parse_args()
        if StudentModel.find_by_name(data['name']):
            return {'message': "A student with name '{}' already exists.".format(data['name'])}, 400
        
        student = StudentModel(data['name'], data['age'], data['university_id'])

        try:
            student.save_to_db()
        except:
            return {"message": "An error occured while saving the student."}, 500
        return student.json(), 201

class StudentByName(Resource):

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return student.json()
        return {'message': 'Student not found'}, 404

    @jwt_required()
    def delete(self, name):

        student = StudentModel.find_by_name(name)
        if student:
            student.delete_from_db()

            return {'message': 'student deleted successfully'}

    @jwt_required()
    def put(self, name):
        # Create or Update
        data = Student.parser.parse_args()
        student = StudentModel.find_by_name(name)

        if student is None:
            student = StudentModel(name, data['age'])
        else:
            student.age = data['age']

        student.save_to_db()

        return student.json()


class StudentList(Resource):
    @jwt_required()
    def get(self):
        return {
            'students': [student.json() for student in StudentModel.query.all()]}
