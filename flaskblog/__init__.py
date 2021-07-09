from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
#csrf
app.config['SECRET_KEY'] = '9a3cc8feaddaf1f84c1900967581d0ad'
#relative path to the development sqlite database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#create a db instance
db = SQLAlchemy(app)
#
bcrypt = Bcrypt(app)
#routes is imported after the app initialization to avoid circular imports(routes import app instance)
from flaskblog import routes