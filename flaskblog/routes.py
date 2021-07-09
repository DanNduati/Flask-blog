from flask import render_template,url_for,flash,redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog.models import User, Post
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
        #hash the password entered by the user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data,email =form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created for you can now login!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Successfully logged in!','success')
        return redirect(url_for('home'))
    return render_template('login.html',title='login',form=form)