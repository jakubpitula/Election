from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from election.config import Config
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from election.main.routes import main
    app.register_blueprint(main)

    return app
