"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Todos

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

@app.route('/todos/user', methods=['POST', 'GET'])
def handle_person():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        user1 = Person(username=body['username'], email=body['email'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404


@app.route('/todos/user/<username>', methods=['PUT', 'GET', 'DELETE', 'POST'])
def get_single_person(username):

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = Person.query.filter_by(username=username)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        user1.todo = body

        db.session.commit()

        return "ok", 200

    # GET request
    if request.method == 'GET':
        user1 = Person.query.filter_by(username=username)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        user1 = list(map(lambda x: x.todo, user1))
        return jsonify(user1), 200

    # DELETE request  ****check****
    if request.method == 'DELETE':
        user1 = Person.query.filter_by(username=username)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        user1.delete()
        db.session.commit()
        return "ok", 200

    # POST request   ****check?****
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        user1 = Person.query.filter_by(username=username)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        user1.todo = []
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
