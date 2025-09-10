from pathlib import Path
from loguru import logger
import smtplib

    
def login(server: smtplib.SMTPL_SSL) -> str:
    '''
    Handle login either by secret files or by user input.
    :param: 
    :return: The sender's email for further use
    '''
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

def send_email():
    '''
    Executes an email sending task
    '''
    pass