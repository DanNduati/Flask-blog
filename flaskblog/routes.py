import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm,RequestResetForm,ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message #enables one to send email 

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page,1,type=int')
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
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

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #save the posts to our db
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='Create post',form=form,legend ='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    #post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    #ensure only the author of the post can update it
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        #pre fill the form with the post data in the database
        form.content.data = post.content
        form.title.data = post.title
    return render_template('create_post.html',title='Update post',form=form,legend ='Update Post')

@app.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    #ensure only the author of the post can delete it
    if post.author != current_user:
        abort(403)
    #delete post
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted!','success')
    return redirect(url_for('home'))

#route to show all the posts of a specific user
@app.route("/home/user/<string:username>")
def user_post(username):
    page = request.args.get('page,1,type=int')
    #query the user provided in the url
    user = User.query.filter_by(username=username).first_or_404()
    if user:
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=posts,user=user)


#function to send email
def send_reset_email(user):
    #get token from the function in the user model
    token = user.get_reset_token()
    #send the email with the url with the reset token
    msg = Message('Password Reset Request',recipients=[user.email])
    msg.html = f'''To reset your password, visit: 
{url_for('reset_token',token=token,_external=True)}
If you did not not make this request please ignore this email
'''
    #send 
    mail.send(msg)



#route for reset password request
@app.route("/reset/password",methods=['GET','POST'])
def reset_request():
    #user has to be logged out
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send the user an email with the token
        send_reset_email(user);
        flash('An email has been sent to you to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Request reset',form=form)

#actual password reset route
#accept a token
#this route is consumed by the user on the email
@app.route("/reset/password/<token>",methods=['GET','POST'])
def reset_token(token):
    #user has to be logged out
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #token = request.args.get('token,None')
    #verify the reset token and get the user id from the email provided
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    #if all passes
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #hash the password entered by the user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password',form=form)