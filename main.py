import smtplib, ssl
from dataloaders import *
from email_helpers import *
from time import sleep

# Constants:
# SSL Port
port = 465

# Create secure SSL context
context = ssl.create_default_context()

def main(
        template_name: str,
        subject: str = '',
        data_name: str = '',
        columns: list = [],
        recipients: list = [],
        preview: bool=True,
    ) -> None:
    '''
    Main function for email handler.
    Subject can be given either as a string if the same for all emails, or can be supplied in data if it should be personalized.

    If no template arguments are needed, the list of recipients is still needed. The list of recipients
    can be passed as a datafile using a file referred to with data_name, or in this case the receipients arg can be used.

    If any template arguments indicated through "{ }" exist in the template, the program expects data to fill these in.
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
        
        # Load in templates to use
        txt_template, html_template = load_templates(template_name)

        # Build list of messages to send
        subjects, contexts = [], []

        # Load in data for parameter filling
        if data_name:
            data = extract_data(data_name, columns)

            if not subject: # if subject was not given, search for it in the data
                subjects, sub_col = find_subject_col(data)
                if sub_col:
                    data = data.drop(sub_col, axis=1)
            else: # if subject is given, it is a single string that we can duplicate
                subjects = [subject] * len(data)

            email_col = ""
            if not recipients: # if recipients are not supplied, search for them in the data
                recipients, email_col = find_email_col(data)
                if email_col:
                    data = data.drop(email_col, axis=1) # remove from templating data
            if not email_col:
                # fallback to sender+pythonbot
                receiver_email = sender_email[:sender_email.find('@')] + "+pythonbot" + sender_email[sender_email.find('@'):]
                recipients = [receiver_email] * len(data)
            
            contexts = [row for _,row in data.iterrows()]

        
        # No data given - send template as-is
        else: 
            logger.info("No data provided. Sending provided templates without adding any arguments.")
            if not recipients:
                logger.warning("No recipients provided. Please add a list of recipients to the function call.")
                return 
            subjects = [subject] * len(recipients)
            contexts = [{}] * len(recipients) # no formatting arguments
        
        for subj, recipient, ctx in zip(subjects, recipients, contexts):
            txt = txt_template.render(**ctx)
            html = html_template.render(**ctx)
            if preview:
                print('='*40)
                print(f'Preview for {recipient}\n')
                print(f"Subject: {subj}")
                print(f"Plain text:\n{txt}\n")
                print(f"HTML:\n{html}")

                choice = input("Send this email? (y/n/q) ").lower()
                if choice.startswith("q"):
                    print("Aborting bulk send.")
                    return
                elif not choice.startswith("y"):
                    print("Skipped.")
                    continue

            send_email(server, sender_email, recipient, subj, txt, html)
            sleep(1) # to not overload server

if __name__ == '__main__':
    main(template_name = 'example', subject = 'Book status', data_name = 'library_data.csv')