from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_url_path='/',  static_folder="dist")
csrf = CSRFProtect(app)
app.config.from_object(Config)
app.secret_key="secreto"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
 
login = LoginManager(app)
#login.login_view = "login"
login.init_app(app)
login.session_protection = "strong"

csrf.init_app(app)
CORS(
    app,
    supports_credentials=True,
    resources={r'/*': {'origins': 'http://localhost:8080'}},
    # Indicates that Content-Type and X-CSRFToken headers will be exposed
    expose_headers=["Content-Type", "X-CSRFToken"],
    )  # Allow cookies to be sent cross-domain

from App import routes, models, errors
