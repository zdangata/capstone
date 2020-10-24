import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, create_app, Actor, Movie


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
        DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
        PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')

        self.assistant_header = {
            'Content-Type': 'application/json',
            'Authorisation': ASSISTANT_TOKEN
        }

        self.director_header = {
            'Content-Type': 'application/json',
            'Authorisation': DIRECTOR_TOKEN
        }

        self.producer_header = {
            'Content-Type': 'application/json',
            'Authorisation': PRODUCER_TOKEN
        }

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        #create new actor
        '''self.new_actor = {
            'actor': 'Derek Salt',
            'age': 29,
            'awards': 'Oscars'
        }

        #create new movie
        self.new_movie = {
            'movie': 'Getting Knocked Out',
            'genres': 'Action',
            'age_rating': 'Fifteen'
        }'''
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #test for successful get request in movies
    def test_get_movies(self):
        movie = Movie(movie='War of Titans', genres='Action', age_rating='Fifteen')
        movie.insert

        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    #test for get request error behaviour in questions
    def test_404_sent_request_when_no_movies_present(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    #test for successful get request in actors
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    #test for get request error behaviour in actors
    def test_404_sent_request_when_no_actors_present(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #test for creation of new movie
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    #test for movie creation which is not allowed
    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies', json={'movie': 4455,'genres': 'Action','age_rating': 'Fifteen'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    #test for creation of new actor
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_actors'])

    #test for actor creation which is not allowed
    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors', json={'actor': 'Derek Salt', 'age': 'Twenty-nine', 'awards': 'Oscars'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    #test for movie update
    def test_update_movie(self):
        res = self.client().patch('/movies/1', json={'age_rating': 'Twenty-one'})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['age_rating'], 'Twenty-one')

    #test for failed movie update
    def test_400_for_failed_movie_update(self):
        res = self.client().patch('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    #test for actor update
    def test_update_movie(self):
        res = self.client().patch('/movies/1', json={'age_rating': 'Twenty-one'})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['age_rating'], 'Twenty-one')

    #test for failed actor update
    def test_400_for_failed_movie_update(self):
        res = self.client().patch('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    #test for delete request in movies
    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id==1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_movies'])
        self.assertEqual(movie, None)

    #test for deletion of non-existant items in movies
    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')

    #test for delete request in actors
    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id==1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_actors'])
        self.assertEqual(actor, None)

    #test for deletion of non-existant items in movies
    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')
   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()