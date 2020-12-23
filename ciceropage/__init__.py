import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

#  pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"


###########################
#### BLUEPRINT CONFIGS #######
#########################

from ciceropage.core.views import core
from ciceropage.users.views import users
from ciceropage.tour_posts.views import tour_posts
from ciceropage.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(users)
app.register_blueprint(tour_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
