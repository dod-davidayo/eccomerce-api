# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# import migration tool
from flask_migrate import Migrate

# create db instance
db = SQLAlchemy()

# create migrate instance
migrate = Migrate()

# create JWT manager instance
jwt = JWTManager()