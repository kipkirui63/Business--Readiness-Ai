
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api(title="Business AI Readiness API", version="1.0", description="Handles readiness inputs and auth")
migrate = Migrate()
mail = Mail()
