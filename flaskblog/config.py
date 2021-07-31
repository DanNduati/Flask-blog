import os
#default values can be set here
#class based configs
#all configs in a single object
class Config:
	#csrf
	SECRET_KEY = os.environ.get('SECRET_KEY')
	#relative path to the development sqlite database 
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	#mail constants
	MAIL_SERVER = 'smtp.sendgrid.net'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'apikey'
	MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
	MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')