from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from election.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.filters['zip'] = zip

    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Musisz się zalogować, żeby mieć dostęp do tej strony.'

    mail.init_app(app)
    bcrypt.init_app(app)
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
