"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():

    all_people = People.get_all()

    if all_users:
        return jsonify([people.serialize() for people in all_people]), 200
    return {'error': 'User not found'}, 404

@api.route('/people/<int:id>', methods=['GET'])
def get_person(id):

    person = People.get_by_id(id)

    if not (person):
        return {'error': 'User not found'}, 404
    return jsonify(person.serialize())
    


@app.route('/planets', methods=['GET'])
def get_planets():

    all_planets = Planets.get_all()

    if all_planets:
        return jsonify([planet.serialize() for planet in all_planets]), 200
    return {'error': 'User not found'}, 404

@api.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):

    planet = Planets.get_by_id(id)

    if not (planet):
        return {'error': 'User not found'}, 404
    return jsonify(planet.serialize())

@app.route('/users', methods=['GET'])
def get_users():

    users = Users.get_all()

    if users:
        return jsonify([user.serialize() for user in users]), 200
    return {'error': 'User not found'}, 404

@app.route('/users/<int:id>/favourites', methods=['GET'])
def get_all_favourites(id):

    favourites = Favourites.get_all_favourites(id)

    if favourites:
        return jsonify([favourite.serialize() for favourite in favourites]), 200
    return {'error': 'User not found'}, 404

@api.route('/users/<int:id>/planets', methods=['POST'])
def post_planet(id):

#request data
    name = request.json.get('name', None)
    surname = request.json.get('surname', None)
    photo_url = request.json.get('photo_url', None)
# assign data to a variable
    planet = Planet(
        name = name,
        surname = surname,
        photo_url = photo_url,
        user_id = id
    )
    if planet:
        try: 
            planet.create()
            return jsonify(planet.serialize()), 201
        except exc.IntegrityError:
            return {'error':'Something is wrong'}, 409

@api.route('/users/<int:id>/people', methods=['POST'])
def post_people(id):
#request data
    name = request.json.get('name', None)
    surname = request.json.get('surname', None)
    photo_url = request.json.get('photo_url', None)
# assign data to a variable
    people = People(
        name = name,
        surname = surname,
        photo_url = photo_url,
        user_id = id
    )
    if people:
        try: 
            people.create()
            return jsonify(people.serialize()), 201
        except exc.IntegrityError:
            return {'error':'Something is wrong'}, 409

#soft-delete
@api.route('/favourites/<int:id>', methods=['DELETE'])
def delete_favourite(id):

    favourite = Favourite.get_by_id(id)
    
    if not favourite:
        return {'error': 'Favourite not found'}, 404 

    favourite.disable_user()

    return jsonify(favourite.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



    