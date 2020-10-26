# Full Stack Capstone Project

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized.
First cd into the `/capstone` capstone directory then follow the instructions below to set up a virual enviornment for your platform.
[python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by staying in the `/capstone` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Gunicorn](https://docs.gunicorn.org/en/stable/) is the production ready server which we will be using to deploy our app.

## Running the server

From within the `capstone` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Authentication
Role Based Access Control (RBAC) has been configured using [Auth0](https://auth0.com/).
Three user profiles were created and each assigned one of the following rules:

* casting assistant
* casting director
* executive producer

Each role has a unique bearer token, which will be used to authorise the requests available to that particular role.
The tokens can be found in the setup.sh file

## Environment Variables
To export the environment variables correctly, run teh following command from the terminal:

`source setup.sh` 


## Testing
### Using Unittest
#### Setting up the test database
Run the following commands to create the test database and add the required schemas.
```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < casting.psql
python test_app.py
```
#### Running the test script
To run the unittests, run the following command from the capstone directory:

`python3 test_app.py`
Make sure you change the DATABASE_URL environment variable in setup.sh file to have your own database url.

### Using Postman
The app is hosted at the Heroku URL address below.

`https://zdcastagency.herokuapp.com/`

This should be used for requests in postman.

#### Example Requests
Requests should be sent to either of the two resources below...
```
https://zdcastagency.herokuapp.com/actors
https://zdcastagency.herokuapp.com/movies
```
## Endpoints
### GET /movies
* General:

    * Returns a list of each of the movie objects
    * Returns the total number of objects
* Sample: `https://zdcastagency.herokuapp.com/movies`

```
{
    "movies": [
        {
            "age_rating": "Fifteen",
            "genres": "Action",
            "id": 4,
            "movie": "War of Titans"
        },
        {
            "age_rating": "Fifteen",
            "genres": "Action",
            "id": 5,
            "movie": "War of Titans"
        }
    ],
    "success": true,
    "total_movies": 2
}
```
### GET /actors
* General:

    * Returns a list of each of the actor objects
    * Returns the total number of objects
* Sample: `https://zdcastagency.herokuapp.com/actors`
```
{
    "actors": [
        {
            "actor": "Derek Salt",
            "age": 29,
            "awards": "Oscars",
            "id": 6
        },
        {
            "actor": "Derek Salt",
            "age": 29,
            "awards": "Oscars",
            "id": 7
        }
    ],
    "success": true,
    "total_actors": 2
}
```

### POST /movies
* General:

    * Creates a new movie
    * Returns the number of the created movie, the success status of the request and the new total number of movies
* Sample: `https://zdcastagency.herokuapp.com/movies`
* JSON Sample for post request: `{
    "movie": "Click the Dot",
    "genres": "Alternative",
    "age_rating": "Universal"
}`

```
{
    "created": 26,
    "success": true,
    "total_movies": 11
}
```

### POST /actors
* General:

    * Creates a new actor
    * Returns the number of the created actor, the success status of the request and the new total number of actors
* Sample: `https://zdcastagency.herokuapp.com/actors`
* JSON Sample for post request: `{
    "actor": "Mike Birch",
    "age": "29",
    "awards": "None"
}`

```
{
    "created": 28,
    "success": true,
    "total_movies": 12
}
```

### DELETE /movies
* General:

    * Deletes a specific movie, using its unique id as in input
    * Returns the deleted movie number and the success status of the request.
* Sample: `https://zdcastagency.herokuapp.com/movies/11`

```
{
    "deleted": 11,
    "success": true
}
```

### DELETE /actors
* General:

    * Deletes a specific actor, using its unique id as in input
    * Returns the deleted actor number and the success status of the request.
* Sample: `https://zdcastagency.herokuapp.com/actors/13`

```
{
    "deleted": 13,
    "success": true
}
```
### PATCH /movies
* General:

    * Modifies the details of a movie
    * Returns the success status of the request and the id of the updated movie
* Sample: `https://zdcastagency.herokuapp.com/movies/15`
* JSON Sample for post request: `{
    "genres": "Rom Com",
    "age_rating": "Fifteen"
}`

```
{
    "id": 15,
    "success": true
}
```

### PATCH /actors
* General:

    * Modifies the details of a movie
    * Returns the success status of the request and the id of the updated actor
* Sample: `https://zdcastagency.herokuapp.com/actors/14`
* JSON Sample for post request: `{
    "id": 15,
    "success": true
}`

```
{
    "id": 14,
    "success": true
}
```
## Authors
Udacity provided the starter files for the project.

Zanang Dangata built the API, deployed the app using Heroku and created the test suite.

## Motivations
I have completed this project to verify that I still have a strong grasp of the skills I have developed throughout this nanodegree.
I am blessed to have this opportunity to upskill in Software Engineering!

## Acknowledgements
I would first like to thank Jesus Christ for giving me the strength to complete this nanodegree and for being my rock from start to finish.

Shout out to my mentor, Jonathan Carrol for guiding me through this process.

I would also like to thank Nicolas Georgiou, Calvin Connaghan and Andrew Muir for their support in this assignment.