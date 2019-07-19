from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    todos = db.relationship('Todo', backref='person', lazy=True)

    def __repr__(self):
            return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), nullable=True)
    done = db.Column(db.String(5), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)

    def __repr__(self):
            return '<Todos %r>' % self.label

    def serialize(self):
        return {
            "label": self.label,
            "done": self.done,
        }
