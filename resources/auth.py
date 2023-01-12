from flask import Blueprint, request, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, jwt_required
from database.models import User
import datetime

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User(**request.form)
        user.hash_password()
        user.save()
        accessToken = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
        resp = make_response(redirect(url_for('auth.dashboard'))) # Redirect to wherever after login
        resp.set_cookie('access_token_cookie', accessToken, max_age=60*60*24) # Expires in 1 day
        return resp
    else:
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('auth.dashboard'))
        return render_template('signup.html') # Our signup page

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = request.form
        user = User.objects.get(email=body['email'])
        authorized = user.check_password(body['password'])
        if not authorized:
            return render_template('login.html', failed=True) # Our login page
        accessToken = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
        resp = make_response(redirect(url_for('auth.dashboard'))) # Redirect to wherever after login
        resp.set_cookie('access_token_cookie', accessToken, max_age=60*60*24) # Expires in 1 day
        return resp
    else:
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('auth.dashboard'))
        return render_template('login.html') # Our login page

@auth.after_app_request
@jwt_required(optional=True)
def refresh(response):
    identity = get_jwt_identity()
    if identity:
        expTimestamp = get_jwt()['exp']
        now = datetime.datetime.now()
        targetTimestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=30))
        if targetTimestamp > expTimestamp:
            accessToken = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=1))
            set_access_cookies(response, accessToken, max_age=60*60*24)
    return response

@auth.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')