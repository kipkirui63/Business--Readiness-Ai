# from flask_mail import Message
# from flask import current_app
# from extensions import mail

# def send_pdf_email(to_email, subject, body, pdf_path):
#     with current_app.app_context():
#         msg = Message(subject, recipients=[to_email])
#         msg.body = body

#         with open(pdf_path, 'rb') as f:
#             msg.attach("ai_readiness_report.pdf", "application/pdf", f.read())

#         mail.send(msg)


import os
import smtplib
from email.message import EmailMessage

def send_pdf_email(to_email, subject, body, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv('MAIL_DEFAULT_SENDER')
    msg['To'] = to_email
    msg.set_content(body)

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename='report.pdf')

    smtp_server = os.getenv('MAIL_SERVER')
    smtp_port = int(os.getenv('MAIL_PORT'))
    username = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
