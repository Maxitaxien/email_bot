import smtplib, ssl
from dataloaders import *
from email_helpers import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Constants:
# SSL Port
port = 465

# Create secure SSL context
context = ssl.create_default_context()

def main(template_name: str, subject: str = '', data_name: str = '', columns: list = [], recipients: list = []) -> None:
    '''
    Main function for email handler.
    Subject can be given either as a string if the same for all emails, or can be supplied in data if it should be personalized.

    If no template arguments are needed, the list of recipients is still needed. The list of recipients
    can be passed as a datafile using a file referred to with data_name, or in this case the receipients arg can be used.

    If any template arguments { } exist in the template, the program expects data to fill these in.
    This should be given through a file located in data/ using the data_name argument.


    :param template_name str: Name of template to use for filling in text.
    :param subject str: Subject line, can be supplied as single string if the same for all emails.
    :param data_name str: Data name to look for under the data/ dir. 
    :param columns list: A list of specific columns from the data to use.
    :param recipients list: When not parameterizing, can be used to pass a list of recipient emails.
    '''
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        sender_email = login(server)

        if not sender_email:
            logger.info('Exiting program run.')
            return

        # Setup email sending tasks
        tasks = []

        # Load in templates to use
        txt_template, html_template = load_templates(template_name)
        needs_format = (txt_template.find('{') and txt_template.find('}')) or (html_template.find('{') and html_template.find('}'))

        # Load in data for parameter filling
        if data_name:
            data = extract_data(data_name, columns)
            recipients, col = find_email_col(data)
        

        # If formatting:
        if needs_format:
            pass

        # If no email recipients were found, return to sender
        if not recipients and not data_name:
            receiver_email = sender_email[:sender_email.find('@')] + "+pythonbot" + sender_email[sender_email.find('@'):]


        # If not formatting, send email as-is
        for recipient in recipients:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject # make this inferrable from data
            message["From"] = sender_email
            message["To"] = receiver_email

            # Convert to MIMETexxt
            text_part = MIMEText(txt_template, "plain")
            html_part = MIMEText(html_template, "html")

            # Attach, trying to render last part first
            message.attach(text_part)
            message.attach(html_part)

            server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == '__main__':
    main(template_name = 'example', subject = 'Book status')