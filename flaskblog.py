from datetime import datetime
from flask import Flask, render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
#csrf
app.config['SECRET_KEY'] = '9a3cc8feaddaf1f84c1900967581d0ad'
#relative path to the development sqlite database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#create a db instance
db = SQLAlchemy(app)


#class models -> each class is a table in the dc
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    password = db.Column(db.String(60),nullable=False)#hashing method to be used returns 60 characters
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"


#pseudo posts for views tests 
posts = [
    {
        'author':'Daniel',
        'title':'Blog post 1',
        'content':'First blogpost go brr',
        'date_posted':'July 6, 2021'
    },
    {
        'author':'Chege',
        'title':'Blog post test',
        'content':'First blogpost test',
        'date_posted':'July 5, 2021'
    },
    {
        'author':'Nduati',
        'title':'Blog post',
        'content':'What to write',
        'date_posted':'July 4, 2021'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title ='About')
 
@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Successfully logged in!','success')
        return redirect(url_for('home'))
    return render_template('login.html',title='login',form=form)

if __name__ == '__main__':
    app.run(debug=True)