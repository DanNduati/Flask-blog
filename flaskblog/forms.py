from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=15)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')
	#custom validation from wtforms
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).all()
		if user:
			raise ValidationError('Username already taken please choose a different one')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).all()
		if email:
			raise ValidationError('Email is taken please choose a different one')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=15)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])#profile picture field
	submit = SubmitField('Update')
	#only do the custom validation checks only when the user changes any of the fields
	#custom validation from wtforms
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).all()
			if user:
				raise ValidationError('Username already taken please choose a different one')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).all()
			if email:
				raise ValidationError('Email already taken please choose a different one')