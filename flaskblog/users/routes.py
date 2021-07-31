from flask import render_template,redirect,request,url_for,flash,Blueprint
from flask_login import current_user,login_required,login_user,logout_user
from flaskblog import db,bcrypt
from flaskblog.models import User,Post
from flaskblog.users.forms import RegistrationForm, LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email


#instance of blueprint
users = Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hash the password entered by the user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data,email =form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created succesfully you can now login!','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))#ternary conditional for redirects if there are arguments in the url
        else:
            flash(f'Login unsuccessful please check email and password','danger')
    return render_template('login.html',title='login',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET','POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

#route to show all the posts of a specific user
@users.route("/home/user/<string:username>")
def user_post(username):
    page = request.args.get('page,1,type=int')
    #query the user provided in the url
    user = User.query.filter_by(username=username).first_or_404()
    if user:
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=posts,user=user)


#route for reset password request
@users.route("/reset/password",methods=['GET','POST'])
def reset_request():
    #user has to be logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send the user an email with the token
        send_reset_email(user);
        flash('An email has been sent to you to reset your password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Request reset',form=form)

#actual password reset route
#accept a token
#this route is consumed by the user on the email
@users.route("/reset/password/<token>",methods=['GET','POST'])
def reset_token(token):
    #user has to be logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #token = request.args.get('token,None')
    #verify the reset token and get the user id from the email provided
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    #if all passes
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #hash the password entered by the user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)