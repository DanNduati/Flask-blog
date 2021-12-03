import os
from os.path import join,dirname
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

# Retrieve send-grid api key, sender and recepient email from .env 
api_key = os.environ.get('API_KEY',None)
from_email = os.environ.get('EMAIL',None)
to_email = os.environ.get('EMAIL',None)

message = Mail(
        from_email = from_email,
        to_emails = to_email,
        subject = 'Test email send with Twilio Sendgrid',
        html_content = '<strong>Hello there!</strong>'
        )
try:
    sg =SendGridAPIClient(api_key)
    response = sg.send(message)
    #print(response.status_code)
    if response.status_code != 202:
        raise ValueError('Could not send email!')
    print('Email sent successfully!')
    #print(response.body)
    #print(response.headers)

except Exception as e:
    print(e.message)
