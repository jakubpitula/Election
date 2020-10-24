from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from election.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from election.main.routes import main
    from election.users.routes import users
    from election.candidates.routes import candidates
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(candidates)

    return app
