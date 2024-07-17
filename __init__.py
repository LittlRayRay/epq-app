from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def app_init():
    app = Flask(__name)
    app.config['SECRET_KEY']='p@ssword06'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    return app
