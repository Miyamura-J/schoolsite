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

# Add many to many between grade/major and module
class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    years = db.relationship("Year", backref='year')

class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    fillier_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    modules = db.relationship("Module", backref='major')

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=True)
    documents = db.relationship("Document", backref='module')

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    document = db.Column(db.String(50), unique=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))