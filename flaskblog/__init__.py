from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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

#routes is imported after the app initialization to avoid circular imports(routes import app instance)
from flaskblog import routes