from .auth import SignupApi, LoginApi, RefreshApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/create_user')
    api.add_resource(LoginApi, '/api/get_token')
    api.add_resource(RefreshApi, '/api/refresh')