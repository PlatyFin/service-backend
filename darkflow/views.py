from flask import render_template, request, Blueprint, session, redirect
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from auth import views
from .resource import DarkFlow

#### CONFIG ####
darkflow = Blueprint('darkflow', __name__, template_folder='templates')


#### ROUTES ####
# login
@darkflow.route('/', methods=['GET'])
def trendingChart():
    error = info = None
    if request.method == 'GET':
        if 'x-platyfin-user' in session:
            return redirect('/darkflow')
        return render_template('landing.html')


# addSubscribeEmail
@darkflow.route('/addSubscribeEmail', methods=['POST'])
def addSubscribeEmail():
    error = info = None
    if 'x-platyfin-user' in session:
            return redirect('/darkflow')
    if request.form.get('subscriberEmail') != '':
        try:
            # Validate email address
            validate_email(request.form.get('subscriberEmail'))
        except EmailNotValidError as e:
            print("Invalid email provided : {} ".format(e))
    else:
        error = 'Missing email address'
        return render_template('landing.html', error=error, info=info)

    info = 'Thank you. Email {} added.'.format(request.form.get('subscriberEmail'))
    with open("subscriberEmailList.txt", "a") as file:
        lineToAdd = '{}~{}~{}\n'.format(request.form.get('subscriberEmail'), request.remote_addr, str(datetime.now()))
        file.write(lineToAdd)
    return render_template('landing.html', error=error, info=info)

@darkflow.route('/darkflow', methods=['GET'])
@views.login_required
def getDarkflowList():
    error = info = None
    if request.method == 'GET':
        darkflowCompanyList = DarkFlow().getDarkflowList()
        return render_template('darkflow.html', company_list = darkflowCompanyList)