from flask import Flask
from config import Config
from .admin.routes import admin
from .site.routes import site
from .authentication.routes import auth
from .models import db as root_db, login_manager#, ma
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ash_app.helpers import JSONEncoder
from flask_cors import CORS



# from flask_cors import CORS
app = Flask(__name__)


app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(admin)


root_db.init_app(app)

migrate = Migrate(app,root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin' # Specify which page to load for Non-Authenticated Users

# ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)