from flask import Flask
from app.extension import db, Migrate, jwt
from app.config import Config
from app.models.user import User





app = Flask(__name__)
app.config.from_object(Config)

# Config must come before init_app, otherwise it will not work
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

# binding
db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

# import and register blueprints
from app.routes.auth_routes import auth_rt
app.register_blueprint(auth_rt)


@app.route('/')
def hello():
    return "Hello, World!"



if __name__ == "__main__":
    app.run(debug=True)