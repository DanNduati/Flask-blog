import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
        from_email = 'dannduati2@gmail.com',
        to_emails = 'dannduati2@gmail.com',
        subject = 'Test email send with Twilio Sendgrid',
        html_content = '<strong>Hello there Daniel!</strong>'
        )
try:
    sg =SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

except Exception as e:
    print(e.message)

