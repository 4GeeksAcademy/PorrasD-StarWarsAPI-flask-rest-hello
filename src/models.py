from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id= db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id= db.Column(db.Integer, db.ForeignKey('character.id'))
    user= db.relationship(User)

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    planets= db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet= db.relationship(Favorite)

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    characters= db.Column(db.Integer, db.ForeignKey('character.id'))
    character= db.relationship(Favorite)

    def to_dict(self):
        return {}
