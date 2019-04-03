from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText


def sendEmail(email, text):
    emailSubject = 'confirm your email'
    emailServer = "smtp.gmail.com"
    emailPort = "587"
    emailUsername = "tt9090969@gmail.com"
    emailPassword = "nopasswd1029"

    msg = MIMEMultipart()
    emailText = 'no reply'
    msg['Subject'] = emailSubject
    msg['From'] = emailUsername
    msg['To'] = ', '.join(email)
    msg.attach(MIMEText(text, 'plain'))
    s = smtplib.SMTP(emailServer, emailPort)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(emailUsername, emailPassword)
    s.sendmail(emailUsername, email, msg.as_string())
    s.quit()
    return 0