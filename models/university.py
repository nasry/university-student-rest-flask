from flaskapp.data_base import  data_base as db


class UniversityModel(db.Model):
    __tablename__ = 'university'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    students = db.relationship('StudentModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'students': [student.json() for student in self.students.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
