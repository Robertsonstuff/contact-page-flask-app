import smtplib
from email.mime.text import MIMEText

def send_mail(name, email, where, comments):
    message = f"<h3>New Feedback Submission</h3><ul><li>Name: {name}</li><li>Prefered email: {email}</li><li>where: {where}</li><li>Comments: {comments}</li></ul>"
    sender_email = 'email1'
    receiver_email = 'email2'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("username-from-mailtrap", "password-from-mailtrap")
        server.sendmail(sender_email, receiver_email, msg.as_string())


