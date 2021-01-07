import os
from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment

from db import db
from mail import mail
from chatsocket import socket_io

app = Flask(__name__)
moment = Moment(app)

# load app config
app.config.from_object('config.DevelopmentConfig')

db.init_app(app)
socket_io.init_app(app)
mail.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


from ciceropage.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# import views
from ciceropage.views.pages import pages
from ciceropage.views.auth import auth
from ciceropage.views.signup import signup
from ciceropage.views.home import home
from ciceropage.views.tours import tours
from ciceropage.views.users import users
from ciceropage.views.error_pages import error_pages

# register the blueprints
app.register_blueprint(home)
app.register_blueprint(signup)
app.register_blueprint(pages)
app.register_blueprint(auth)
app.register_blueprint(tours)
app.register_blueprint(users)
app.register_blueprint(error_pages)

# create database tables if don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socket_io.run(app, debug=True)
