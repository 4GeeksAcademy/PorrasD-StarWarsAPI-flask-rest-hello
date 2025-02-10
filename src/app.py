import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    return jsonify([character.to_dict() for character in characters])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    character = Character.query.get_or_404(people_id)
    return jsonify(character.to_dict())

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.to_dict() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.to_dict())

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    user_id = request.args.get('user_id')  
    user = User.query.get_or_404(user_id)
    favorites = {
        "planets": [planet.to_dict() for planet in user.favorites_planets],
        "people": [character.to_dict() for character in user.favorites_people]
    }
    return jsonify(favorites)

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')  
    user = User.query.get_or_404(user_id)
    planet = Planet.query.get_or_404(planet_id)

    if planet not in user.favorites_planets:
        user.favorites_planets.append(planet)
        db.session.commit()
        return jsonify(planet.to_dict()), 201
    return jsonify({"message": "Planet already in favorites"}), 400

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.args.get('user_id')  
    user = User.query.get_or_404(user_id)
    character = Character.query.get_or_404(people_id)

    if character not in user.favorites_people:
        user.favorites_people.append(character)
        db.session.commit()
        return jsonify(character.to_dict()), 201
    return jsonify({"message": "Character already in favorites"}), 400

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = request.args.get('user_id')  
    user = User.query.get_or_404(user_id)
    planet = Planet.query.get_or_404(planet_id)

    if planet in user.favorites_planets:
        user.favorites_planets.remove(planet)
        db.session.commit()
        return jsonify(planet.to_dict()), 200
    return jsonify({"message": "Planet not found in favorites"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    user_id = request.args.get('user_id') 
    user = User.query.get_or_404(user_id)
    character = Character.query.get_or_404(people_id)

    if character in user.favorites_people:
        user.favorites_people.remove(character)
        db.session.commit()
        return jsonify(character.to_dict()), 200
    return jsonify({"message": "Character not found in favorites"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
