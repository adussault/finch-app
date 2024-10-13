from flask import Flask
from dotenv import load_dotenv
import os
from redis import Redis
from flask_session import Session
#from flask


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = Redis(host='localhost', port=6379)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'This-is-a-test-key'
Session(app)


#Session(app)

from app import routes

