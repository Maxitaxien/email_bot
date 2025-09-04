import smtplib, ssl
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465 # ssl port
password_path = Path('secrets') / 'passwd'
sender_email_path = Path('secrets') / 'sender'

if sender_email_path.exists():
    sender_email = sender_email_path.read_text()
else:
    sender_email = input("Enter email to send from: ")

if password_path.exists():
    password = password_path.read_text()
else:
    password = input("Enter password: ")


# By default, just send to the same email with the tag pythonbot
receiver_email = sender_email[:sender_email.find('@')] + "+pythonbot" + sender_email[sender_email.find('@'):]



message = MIMEMultipart("alternative")
message["Subject"] = "Multipart test"
message["From"] = sender_email
message["To"] = receiver_email

text = """\
This is a test using the MIME message type.
The nice thing about this is that we can send both
plain text and html. 
See my website:
https://maxitaxien.github.io/portfolioWebsite/
"""

html = """\
<html>
    <body>
        <p>This is a test using the MIME message type.<br>
        The nice thing about this is that we can send both<br>
        plain text and html.<br>
        See my website:<br>
        <a href="https://maxitaxien.github.io/portfolioWebsite/">Website </a><br>
        </p>
    </body>
</html>
"""

# Turn iunto MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Attach to multipartmessage, last part will try to be rendered first
message.attach(part1)
message.attach(part2)

# Create secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_email, message.as_string())
