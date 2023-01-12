from .auth import SignupApi, LoginApi, RefreshApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(RefreshApi, 'auth/refesh')