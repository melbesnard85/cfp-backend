from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from flask_restful_swagger_2 import Api
from flask_cors import CORS

from database.db import initialize_db

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'cpf-secret-key'
app.config['MONGODB_SETTINGS'] = 'mongodb://localhost/cfp'
app.config['JWT_TOKEN_LOCATION'] = 'cookies'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api = Api(app)
cors = CORS(app, resources={r'/*': { 'origins': '*' }})

# initialize database
initialize_db(app)