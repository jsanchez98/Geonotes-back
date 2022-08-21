from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

application = Flask(__name__, static_url_path='/',  static_folder="dist")

csrf = CSRFProtect(application)
application.config.from_object(Config)
application.secret_key="secreto"
db = SQLAlchemy(application)
migrate = Migrate(application, db)
print("running")
login = LoginManager(application)
#login.login_view = "login"
login.init_app(application)
login.session_protection = "strong"

csrf.init_app(application)
CORS(
    application,
    supports_credentials=True,
    resources={r'/*': {'origins': ['http://127.0.0.1:5173','http://localhost:8080']}},
    # Indicates that Content-Type and X-CSRFToken headers will be exposed
    expose_headers=["Content-Type", "X-CSRFToken"],
    )  # Allow cookies to be sent cross-domain

from .errors import APIError
from .models import User, Post
from .routes import *
 