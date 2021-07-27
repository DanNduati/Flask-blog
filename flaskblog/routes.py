import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm,LoginForm,UpdateAccountForm
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

#function to set the users profile picture
def save_picture(form_picture):
    #randomize the name of the image
    random_hex = secrets.token_hex(8)
    #get the extension using the os module
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    #dir where the image will be saved
    #use the root path attribute of our application 
    #profile_pics within the static folder
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    #resize the image before saving
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #update the username and email
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)