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
from models import Movie, Actor

#----------------------------------------------------------------------------#
# Create and configure the app
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setuo_db(app)

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
  def get_movies():
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
  def create_movie():
    body = request.get_json()

    new_movie = body.get('movie', None)
    genres = body.get('genres', None)
    age_rating = body.get('age_rating', None)

    try:
      movie = Movie(movie=new_movie, genres=genres, age_rating=age_rating)
      movie.insert()

      return jsonify({
        'success': True,
        'created': movie.id,
        'total_movies': len(Movie.query.all())
      })

    except:
      abort(422)

  '''@app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  def modify_actor(movie_id):

  @app.route('/actors')
  def actors():

  @app.route('/actors', methods=['POST'])
  def create_actor():

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def modify_actor(actor_id):'''

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


APP = create_app()

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

