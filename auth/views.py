#### IMPORTS ####
from flask import render_template, request, redirect, Blueprint, session, url_for, flash
from functools import wraps
from email_validator import validate_email, EmailNotValidError


from datetime import timedelta
import json

# resources
from auth.resource import UserByUsername, UserOperations, UserByEmail
# views
from auth.views import *
from darkflow.resource import DarkFlow

#### CONFIG ####
auth = Blueprint('auth', __name__, template_folder='templates')

#### GLOBAL OBJECTS ####
userByUsernameObj = UserByUsername()
userOperationsObj = UserOperations()
userByEmailObj = UserByEmail()

darkflowObj = DarkFlow()

#### DECORATORS ####
# login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'x-platyfin-user' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('auth.login'))
    return wrap

#### ROUTES ####
# login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'x-platyfin-user' in session:
            return redirect(url_for('darkflow.getDarkflowList'))
        return render_template('login.html')
    if request.method == 'POST':
        if 'x-platyfin-user' in session:
            return redirect(url_for('darkflow.getDarkflowList'))
        if request.form['action'] == 'register':
            return redirect(url_for('auth.register'))
        if request.form['action'] == 'login':
            try:
                user_data = json.loads(userByUsernameObj.get(request.form['username'].lower()).get_data())
                if not user_data['user']:
                    error = "User is not in system."
                    return redirect(url_for('auth.register', error=error))
                else:
                    is_user = userOperationsObj.is_user(request.form['username'].lower(), request.form['password'])
                    if(is_user):
                        # set session
                        session['x-platyfin-user'] = request.form['username'].lower()
                        session.permanent = False
                        auth.permanent_session_lifetime = timedelta(minutes=30)
                        info = 'Welcome {} !'.format(request.form['username'].lower())
                        return redirect(url_for('darkflow.getDarkflowList', info=info))
                    else:
                        error = 'Invalid Credentials.'
                        return redirect(url_for('auth.login', error=error))
            except Exception as e:
                print("Error while login: {} ".format(e)) 
    else:
        return render_template('login.html', error=error, info=info)

# register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'x-platyfin-user' in session:
            return redirect(url_for('darkflow.getDarkflowList'))
        if request.args.get('error'):
            error = request.args.get('error')
        else:
            error = None
        return render_template('register.html', error=error)
    if request.method == 'POST':
        if 'x-platyfin-user' in session:
            return redirect(url_for('darkflow.getDarkflowList'))
        if request.form['inputEmail'] != '':
            try:
                # Validate email address
                validate_email(request.form['inputEmail'].lower())
                userByEmail = json.loads(userByEmailObj.get(request.form['inputEmail'].lower()).get_data())
                if userByEmail['user']:
                    return redirect(url_for('auth.register', error='Email exist in the system')) # return statement
            except EmailNotValidError as e:
                print("Invalid email provided : {} ".format(e))
        else:
            error = 'Missing email address'
            return redirect(url_for('auth.register', error=error))  # return statement

        if request.form['inputUsername'] != '' and request.form['inputPassword'] != '' and request.form['inputPasswordConfirm'] != '':
            try:
                user_data = json.loads(userByUsernameObj.get(request.form['inputUsername'].lower()).get_data())
                if user_data['user']:
                    return redirect(url_for('auth.register', error='Username is in system'))  # return statement
                elif request.form['inputPassword'] != request.form['inputPasswordConfirm']:
                    return redirect(url_for('auth.register', error='Enter two identical string for password'))  # return statement
                else:
                    user_id = userOperationsObj.post(request.form['inputUsername'].lower(), request.form['inputEmail'].lower(), request.form['inputPassword'])
                    info = 'USER CREATED WITH ID : {}'.format(str(user_id))
                    return redirect(url_for('auth.login', info=info))  # return statement
            except Exception as e:
                import traceback
                print("Error creating tables:  {} ".format(e))
                traceback.print_exc()        
        else:
            error = 'Missing require data'
            return redirect(url_for('auth.register', error=error))  # return statement

# logout
@auth.route('/logout')
@login_required
def logout():
    info = None
    session.pop('x-platyfin-user', None)
    info = 'You were logged out.'
    return redirect(url_for('auth.login', info=info))