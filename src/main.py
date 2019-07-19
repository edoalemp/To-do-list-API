"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Todo

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET','POST'])
def manage_users():

    if request.method == 'GET':
        people = Person.query.all()
        people = list(map(lambda x: x.serialize(), people))
        return jsonify(people), 200

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        person = Person(username=body['username'], email=body['email'])
        db.session.add(person)
        db.session.commit()
        return "ok", 200

@app.route('/todos/user/<username>', methods=['PUT', 'GET', 'DELETE', 'POST'])
def get_person_todos(username):

    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        person = Person.query.filter_by(username=username).first()
        if person is None:
            raise APIException('User not found', status_code=404)
        new_todos = []
        for todo_data in body:
            new_todos.append(Todo(label=todo_data["label"],done=todo_data["done"],person_id = person.id))
        person.todos = new_todos
        db.session.commit()
        return "ok", 200

    if request.method == 'GET':
        person = Person.query.filter_by(username=username).first()
        if person is None:
            raise APIException('User not found', status_code=404)
        todos = person.todos
        todos = list(map(lambda x: x.serialize(), todos))
        return jsonify(todos), 200

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        person = Person.query.filter_by(username=username).first()
        if person is None:
            raise APIException('User not found', status_code=404)
        person.todos = body
        db.session.commit()
        return "ok", 200

    if request.method == 'DELETE':
        person = Person.query.filter_by(username=username).first()
        if person is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(person)
        db.session.commit()
        return "ok", 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
