import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import app

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = 'postgres://mpqykadjmexknq:92e4eb5c8ebfbf0c2ab75deb48d30bf8d7f0da569c85891a7bf408fc75d0b2d3@ec2-23-20-70-32.compute-1.amazonaws.com:5432/d9ksod21on33pi'
SQLALCHEMY_TRACK_MODIFICATIONS = False