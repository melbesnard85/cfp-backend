from .auth import auth

def initialize_routes(app):
    app.register_blueprint(auth)