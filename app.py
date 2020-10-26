#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import json
import babel
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Movie, Actor, setup_db
from auth import AuthError, requires_auth, get_token_auth_header
#----------------------------------------------------------------------------#
# Create and configure the app
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  db = SQLAlchemy()
  setup_db(app)

  # Set up CORS. Allow '*' for origins.
  cors = CORS(app)

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, DELETE, OPTIONS')
    return response

  # Gets all movies
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    formatted_movies = [movie.format() for movie in movies]

    total_movies = len(movies)

    if (total_movies == 0):
      abort(404)
    
    return jsonify({
      'success': True,
      'movies': formatted_movies,
      'total_movies': total_movies 
    })

  # Creates movies
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    body = request.get_json()

    new_movie = body.get('movie', None)
    genres = body.get('genres', None)
    age_rating = body.get('age_rating', None)

    try:
      movie = Movie(movie=new_movie, genres=genres, age_rating=age_rating)
      movie.insert()

      movies = Movie.query.all()
      formated_movies = [movie.format for movie in movies]

      return jsonify({
        'success': True,
        'created': movie.id,
        'total_movies': len(movies)
      })

    except BaseException as e:
      print(e)
      abort(422)

  # Deletes movies
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)

      movie.delete()

      return jsonify({
        'success': True,
        'deleted': movie_id
      })

    except BaseException as e:
      print(e)
      abort(422)

  # Modifies movies
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def modify_movie(payload, movie_id):
    body = request.get_json()

    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if movie is None:
        abort(404)

      if 'genres' in body:
        movie.genres = str(body.get('genres'))
      
      if 'age_rating' in body:
        movie.age_rating = str(body.get('age_rating'))

      movie.update()

      return jsonify({
        'success': True,
        'id': movie.id
      })

    except BaseException as e:
      print(e)
      abort(400)

  # Gets all actors
  @app.route('/actors')
  @requires_auth('get:actors')
  def actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    formatted_actors = [actor.format() for actor in actors]

    total_actors = len(actors)

    if (total_actors == 0):
      abort(404)
    
    return jsonify({
      'success': True,
      'actors': formatted_actors,
      'total_actors': total_actors
    })

  # Creates actors
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    body = request.get_json()

    new_actor = body.get('actor', None)
    age = body.get('age', None)
    awards = body.get('awards', None)

    try:
      actor = Actor(actor=new_actor, age=age, awards=awards)
      actor.insert()

      actors = Actor.query.all()
      formated_actors = [actor.format for actor in actors]

      return jsonify({
        'success': True,
        'created': actor.id,
        'total_actors': len(Actor.query.all())
      })

    except BaseException as e:
      print(e)
      abort(422)

  # Deletes actors
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor_id
      })

    except BaseException as e:
      print(e)
      abort(422)

  # Modifies actors
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def modify_actor(payload, actor_id):
    body = request.get_json()

    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)

      if 'age' in body:
        actor.age = int(body.get('age'))
      
      if 'awards' in body:
        actor.awards = str(body.get('awards'))

      actor.update()

      return jsonify({
        'success': True,
        'id': actor.id
      })

    except BaseException as e:
      print(e)
      abort(40)


#----------------------------------------------------------------------------#
# Error Handlers
#----------------------------------------------------------------------------#
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(401)
  def unauthorised_error(error):
      return jsonify({
      "success": False,
      "error": 401,
      "message": "unauthorised"
    }), 401

  @app.errorhandler(403)
  def forbidden(error):
      return jsonify({
      "success": False,
      "error": 403,
      "message": "access forbidden"
    }), 403

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def not_processed(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable entity"
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500
  

  return app


app = create_app()

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

