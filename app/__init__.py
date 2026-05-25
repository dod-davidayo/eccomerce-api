from flask import Flask
from app.extension import db, Migrate, jwt
from app.config import Config
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.cart import Cart
from datetime import timedelta


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

# Config must come before init_app, otherwise it will not work
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# binding
    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

# import and register blueprints
    from app.routes.auth_routes import auth_rt
    from app.routes.product_routes import products_bp 
    from app.routes.category_routes import categories_bp
    from app.routes.cart_routes import cart_bp


    app.register_blueprint(auth_rt)
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(cart_bp)


    return app