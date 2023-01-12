import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from flask_restful_swagger_2 import Api
from flask_cors import CORS

from database.db import initialize_db
from resources.routes import initialize_routes
from database.models import User


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
# initialize routes
initialize_routes(api)

# Admin account initialization for first uses
user = User.objects(email='admin@gmail.com')
if not user:
    login = User(email='admin@gmail.com', password='asdfASDF')
    login.hash_password()
    login.save()

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='localhost', port=port)