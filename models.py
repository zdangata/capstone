from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
database_path = os.environ.get('DATABASE_URL')
#database_path = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Database Setup
#----------------------------------------------------------------------------#


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    return app

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String)
    genres = db.Column(db.String)
    age_rating = db.Column(db.String)

    def __init__(self, movie, genres, age_rating):
        self.movie = movie
        self.genres = genres
        self.age_rating = age_rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie': self.movie,
            'genres': self.genres,
            'age_rating': self.age_rating
        }

    # def __repr__(self):
    # return f'<Movie {self.id} {self.name} {self.genres} {self.age_rating}>'


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String)
    age = db.Column(db.Integer)
    awards = db.Column(db.String)

    def __init__(self, actor, age, awards):
        self.actor = actor
        self.age = age
        self.awards = awards

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'actor': self.actor,
            'age': self.age,
            'awards': self.awards
        }

    # def __repr__(self):
    #     return f'<Actor {self.id} {self.name} {self.age} {self.awards}>'
