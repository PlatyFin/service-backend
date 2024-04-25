import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow


app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.environ.get('SECRET_KEY', 'optional_default')

#### Models object ####
DB_URL = 'postgresql://{user}:{pw}@{host}/{db}'.format(user=os.environ['DATABASE_USER'],pw=os.environ['DATABASE_PASSWORD'],host=os.environ['DATABASE_HOST'],db=os.environ['DATABASE_NAME'])

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
bcrypt = Bcrypt(app)

try:
    from darkflow.views import darkflow
    from auth.views import auth
except Exception as e:
    print("Modules are Missing : {} ".format(e))


# BLUEPRINT REGISTER
app.register_blueprint(darkflow)
# DARKFLOW
app.register_blueprint(auth)


try:
    # Create database tables within the application context
    with app.app_context():
        if not db.engine.table_names():
            db.create_all()
except Exception as e:
    import traceback
    print("Error creating tables:", e)
    traceback.print_exc()