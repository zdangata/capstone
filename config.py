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


SQLALCHEMY_DATABASE_URI = 'postgres://dkbpbwokimtlar:97fcfbf3e300a51c0d9a0941565925a0dadf2121476705e6e5d48e388d697b46@ec2-18-210-51-239.compute-1.amazonaws.com:5432/df1tirki6u3mi3'
SQLALCHEMY_TRACK_MODIFICATIONS = False