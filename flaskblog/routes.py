from flask import render_template,url_for,flash,redirect,request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog.models import User, Post
from flask_login import login_user,current_user,logout_user,login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hash the password entered by the user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data,email =form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created succesfully you can now login!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #users log in with email
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            #log user in
            login_user(user,remember=form.remember.data)
            #get the parameters from url if they exist
            next_page = request.args.get('next')
            flash(f'Login successful!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))#ternary conditional for redirects if there are arguments in the url
        else:
            flash(f'Login unsuccessful please check email and password','danger')
    return render_template('login.html',title='login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')