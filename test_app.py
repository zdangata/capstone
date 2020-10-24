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

   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()