import smtplib, ssl
from pathlib import Path

port = 465 # ssl port
password = (Path('secrets') / 'passwd').read_text()

sender_email = "max.bakke.seymour@gmail.com"
receiver_email = "max.bakke.seymour+pythonbot@gmail.com"
message = """
Subject: Hi there!
This message is sent from Python
"""

# Create secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("max.bakke.seymour@gmail.com", password)

    server.sendmail(sender_email, receiver_email, message)

