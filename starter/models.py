import os
from settings import DATABASE_URL
from flask_sqlalchemy import SQLAlchemy

database_path = DATABASE_URL

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    description = db.Column(db.String, nullable=True)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'rating': self.rating,
            'description': self.description
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_of_birth = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=True)
    nationality = db.Column(db.String, nullable=True)
    bio = db.Column(db.String, nullable=True)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'year_of_birth': self.year_of_birth,
            'gender': self.gender,
            'nationality': self.nationality,
            'bio': self.bio
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
