from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from flaskapp.resources.student import Student, StudentByName, StudentList
from flaskapp.resources.university import University, UniversityByName, UniversityList

from flaskapp.resources.user import UserSignUp, UserSignIn, User
from flaskapp.config import postgresqlConfig


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig

app.config["JWT_SECRET_KEY"] = "it.tecos.FIDELITY-APP"

jwt = JWTManager(app)
api = Api(app)

@app.before_first_request
def create_tables():
    from flaskapp.data_base import data_base as db
    db.init_app(app)
    db.create_all()


api.add_resource(UserSignUp, '/signup')
api.add_resource(UserSignIn, '/signin')

api.add_resource(User, '/user')

api.add_resource(Student,       '/student')
api.add_resource(StudentByName, '/student/<string:name>')
api.add_resource(StudentList,   '/students')

api.add_resource(University,        '/university')
api.add_resource(UniversityByName,  '/university/<string:name>')
api.add_resource(UniversityList,    '/universities')
