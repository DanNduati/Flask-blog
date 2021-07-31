from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


#Extensions initialized without the app variable
#This as per flask documentation - this is so that the extension object does not initially get bound to the application
#Using this design pattern,no app specific state is stored on the extension object and as so one extension object
#can be used for multiple apps

#create a db instance
db = SQLAlchemy()
#bcrypt instance 
bcrypt = Bcrypt()
#login instance
login_manager = LoginManager()
login_manager.login_view = 'users.login'#configure login manager to redirect to the login route if one tries to access a restricted route
login_manager.login_message = 'Acha izo bruv!'
login_manager.login_message_category = 'danger'#improve "please log in to access this page" flash message
#initialize the mail extension
mail = Mail()

#routes is imported after the app initialization to avoid circular imports(routes import app instance)
#from flaskblog import routes


def create_app(config_class = Config):
	#has app creation and blueprints not the extensions
	app = Flask(__name__)
	#app config from the config class
	app.config.from_object(Config)

	#use the init_app method to pass the application to the extensions
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	#import all the blueprint objects from the packages(users and post) and register them as routes
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main

	#register the blueprints
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app