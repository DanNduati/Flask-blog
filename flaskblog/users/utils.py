import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from flaskblog import mail
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
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    #resize the image before saving
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


#function to send email
def send_reset_email(user):
    #get token from the function in the user model
    token = user.get_reset_token()
    #send the email with the url with the reset token
    msg = Message('Password Reset Request',recipients=[user.email])
    msg.html = f'''To reset your password, visit: 
{url_for('users.reset_token',token=token,_external=True)}
If you did not not make this request please ignore this email
'''
    #send 
    mail.send(msg)