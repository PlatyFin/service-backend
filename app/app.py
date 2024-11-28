import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
import alpaca_trade_api as tradeapi

app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.environ.get('SECRET_KEY', 'optional_default')

#### Models object ####
DB_URL = os.environ.get('DB_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
bcrypt = Bcrypt(app)

# Replace 'your_api_key' and 'your_secret_key' with your actual API keys
paper_api = tradeapi.REST(os.environ.get('ALPACA_API_KEY'), os.environ.get('ALPACA_SECRET_KEY'), base_url='https://paper-api.alpaca.markets', api_version='v2')

try:
    from landing.views import landing
    from auth.views import auth
    from strategies.views import strategies
except Exception as e:
    print("Modules are Missing : {} ".format(e))

# BLUEPRINT REGISTER
app.register_blueprint(landing)
app.register_blueprint(auth)
app.register_blueprint(strategies)

try:
    # Create database tables within the application context
    with app.app_context():
        if not inspect(db.engine).get_table_names():
            db.create_all()
except Exception as e:
    import traceback
    print("Error creating tables:", e)
    traceback.print_exc()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)