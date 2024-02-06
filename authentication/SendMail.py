# sending some email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, subject, body):
    # Your email and password
    sender_email = 'agreharshit610@gmail.com'
    sender_password = 'lbqxavlpxnewvczt'

    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

