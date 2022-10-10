from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    majors = db.relationship("Major")
    modules = db.relationship("Module")

class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'))
    modules = db.relationship("Module")

# I could have one module for many majors and many modules for one majors. Many-to-many relationship to make
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=True)
    major_id = db.Column(db.Integer, db.Foreignkey('major.id'), nullable=True)
    documents = db.relationship("Document")

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    document = db.Column(db.String(50), unique=True)
    module_id = db.Column(db.Integer, db.Foreignkey('module.id'))
