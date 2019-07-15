from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }

class Todos(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True, nullable=False)
    done = db.Column(db.String(5), unique=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person')

    def __repr__(self):
        return '<Todos %r>' % self.label

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }