from flask import Blueprint, request, make_response, render_template, redirect, url_for
from flask_restful_swagger_2 import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, create_refresh_token
from database.models import User
import datetime

class SignupApi(Resource):
    def post(self):
        user = User(**request.get_json())
        user.hash_password()
        user.save()
        return { 'id': str(user.id) }

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body['email'])
        authorized = user.check_password(body['password'])
        if not authorized:
            return 'Unauthorized Error', 401
        accessToken = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
        refreshToken = create_refresh_token(identity=str(user.id), expires_delta=datetime.timedelta(days=30))
        return { 'accessToken': accessToken, 'refreshToken': refreshToken }

class RefreshApi(Resource):
    @jwt_required(refresh=True)
    def get(self):
        accessToken = create_access_token(identity=get_jwt_identity(), expires_delta=datetime.timedelta(days=1))
        refreshToken = create_refresh_token(identity=get_jwt_identity(), expires_delta=datetime.timedelta(days=30))
        return { 'accessToken': accessToken, 'refreshToken': refreshToken }