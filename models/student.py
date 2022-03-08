from flaskapp.data_base import  data_base as db


class StudentModel(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)

    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('UniversityModel')

    def __init__(self, name, age, university_id):
        self.name = name
        self.age = age
        self.university_id = university_id

    def json(self):
        return {'name': self.name, 'age': self.age, 'university_id': self.university_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
