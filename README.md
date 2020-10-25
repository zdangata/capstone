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
### GET /actors
* General:

    * Returns a list of each of the actor objects
    * Returns the total number of objects

### POST /movies
* General:

    * Creates a new movie
    * Returns the number of the created movie, the success status of the request and the new total number of movies

### POST /actors
* General:

    * Creates a new actor
    * Returns the number of the created actor, the success status of the request and the new total number of actors

### DELETE /movies
* General:

    * Deletes a specific movie, using its unique id as in input
    * Returns the deleted movie number and the success status of the request.

### DELETE /actors
* General:

    * Deletes a specific actor, using its unique id as in input
    * Returns the deleted actor number and the success status of the request.

### PATCH /movies
* General:

    * Returns the success status of the request and the id of the updated movie

### PATCH /actors
* General:

    * Returns the success status of the request and the id of the updated actor