import os #for env variables
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
#csrf
app.config['SECRET_KEY'] = '9a3cc8feaddaf1f84c1900967581d0ad'
#relative path to the development sqlite database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#create a db instance
db = SQLAlchemy(app)
#bcrypt instance 
bcrypt = Bcrypt(app)
#login instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'#configure login manager to redirect to the login route if one tries to access a restricted route
login_manager.login_message = 'Acha izo bruv!'
login_manager.login_message_category = 'danger'#improve "please log in to access this page" flash message

#mail constants
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

#initialize the mail extension
mail = Mail(app)

#routes is imported after the app initialization to avoid circular imports(routes import app instance)
from flaskblog import routes