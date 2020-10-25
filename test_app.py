import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, create_app, Actor, Movie
from app import app
class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
        DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
        PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')
 
        self.assistant_header = {
            'Content-Type': 'application/json',
            "Authorization":
                    "Bearer {}". format(ASSISTANT_TOKEN)
        }
        self.director_header = {
            'Content-Type': 'application/json',
            "Authorization":
                    "Bearer {}". format(DIRECTOR_TOKEN)
        }
        self.producer_header = {
            # 'Content-Type': 'application/json',
            "Authorization":
                    "Bearer {}". format(PRODUCER_TOKEN)
        }
        self.app = app
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
    def test_get_movies(self):#yes
        movie = Movie(movie='War of Titans', genres='Action', age_rating='Fifteen')
        movie.insert

        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    #test for get request error behaviour in questions
    def request_when_no_movies(self):
        res = self.client().get('/movies', headers=None)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorised')

    #test for successful get request in actors
    def test_get_actors(self):#yes
        actor = Actor(actor='Gemma Jones', age=27, awards='None')
        actor.insert

        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    #test for get request error behaviour in actors
    def request_when_no_actors(self):
        res = self.client().get('/actors', headers=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorised')

    #test for creation of new movie
    def test_create_new_movie(self):#yes
        res = self.client().post('/movies', headers=self.producer_header, json={'movie': 'War of Titans', 'genres': 'Action', 'age_rating': 'Fifteen'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    #test for movie creation which is not allowed
    def test_if_movie_creation_not_allowed(self):#yes
        res = self.client().post('/movies', headers=self.director_header, json={'movie': 'War of Titans', 'genres': 'Action', 'age_rating': 'Fifteen'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')

    #test for creation of new actor
    def test_create_new_actor(self):#yes
        res = self.client().post('/actors', headers=self.director_header, json={'actor': 'Derek Salt', 'age': 29, 'awards': 'Oscars'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    #test for actor creation which is not allowed
    def test_if_actor_creation_not_allowed(self):#yes
        res = self.client().post('/actors', headers=self.assistant_header, json={'actor': 'Derek Salt', 'age': 29, 'awards': 'Oscars'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')

    #test for movie update
    def test_update_movie(self):#yes
        res = self.client().patch('/movies/19', headers=self.director_header, json={'genres': 'Alternate'})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id==19)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie['genres'], 'Alternate')

    #test for failed movie update
    def test_for_failed_movie_update(self):#yes
        res = self.client().patch('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorised')

    #test for actor update
    def test_update_actor(self):
        res = self.client().patch('/actors/19', headers=self.director_header, json={'age': 25})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id==19)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor['age'], 25)

    #test for failed actor update
    def test_for_failed_actor_update(self):
        res = self.client().patch('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorised')

    #test for delete request in movies
    def test_delete_movie(self):#yes
        res = self.client().delete('/movies/21', headers=self.producer_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id==21).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 21)
        self.assertEqual(movie, None)

    #test for deletion of non-existant items in movies
    def test_422_if_movie_does_not_exist(self):#yes
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorised')

    #test for delete request in actors
    def test_delete_actor(self):#yes
        res = self.client().delete('/actors/21', headers=self.director_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id==21).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 21)
        self.assertEqual(actor, None)

    #test for deletion of non-existant items in movies
    def test_422_if_actor_does_not_exist(self):#yes
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorised')
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()