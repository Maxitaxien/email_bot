from pathlib import Path
from loguru import logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
    
def login(server: smtplib.SMTP_SSL) -> str:
    '''
    Handle login either by secret files or by user input.
    :param: 
    :return: The sender's email for further use
    '''
    password_path = Path('secrets') / 'passwd'
    sender_email_path = Path('secrets') / 'sender'

    if sender_email_path.exists():
        sender_email = sender_email_path.read_text().strip()
    else:
        sender_email = input("Enter email to send from: ")

    if password_path.exists():
        password = password_path.read_text().strip()
    else:
        password = input("Enter password: ")
    
    try:
        server.login(sender_email, password)
        logger.info(f'Successfuly logged in to email: {sender_email}')
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f'Incorrect username or password: {e}')
        return ""
    except Exception as e:
        logger.error(f'Unknown error occured: {e}')
        return ""

    return sender_email

def send_email(
        server: smtplib.SMTP_SSL, sender_email: str, recipient_email: str, 
        subject: str='', txt: str='', html: str=''
    ) -> bool:
    '''
    Constructs a MIME message consisting of each part passed in
    Executes an email sending task from sender to recipient.
    :return: True if sending was a success else false
    '''
    message = MIMEMultipart("alternative")
    message["Subject"] = subject if subject else "No Subject"
    message["From"] = sender_email
    message["To"] = recipient_email

    # Convert to MIMEText
    if txt:
        message.attach(MIMEText(txt, "plain"))
    if html:
        message.attach(MIMEText(html, "html"))

    if not txt and not html:
        logger.error('No message given. Exiting without sending message.')
        return False

    try:
        server.sendmail(sender_email, recipient_email, message.as_string())
        return True
    except Exception as e:
        logger.error(f'An error occured: {e}')
        return False