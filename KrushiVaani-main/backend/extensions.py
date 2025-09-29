# backend/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate

# Create extension objects
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
migrate = Migrate()