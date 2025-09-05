from pathlib import Path
from loguru import logger
import pandas as pd
import smtplib

def extract_data(file_name: str, columns: list = []) -> pd.DataFrame:
    '''
    Either extracts specific columns, or just loads in dataframe including all columns
    if no argument is given to columns.
    Data is used for filling in arguments in templates.
    '''
    if not file_name.endswith('.csv'): # try to attach csv suffix if not included in filename
        logger.info('Added file suffix: .csv')
        file_name += '.csv'
    
    file_path = Path('data') / file_name
    if not file_path.exists():
        logger.warning(f'File {file_name} not found. Returning empty DataFrame.')
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    # return as-is if no column selection is made
    if len(columns) == 0:
        logger.info(f'Extracting all columns from {file_name}.')
        return df

    # check if all the columns the user asked for was present
    available_cols = []
    for col in columns:
        if col not in df.columns:
            logger.warning(f'Could not locate column: {col} in loaded .csv file.')
        else:
            available_cols.append(col)
    logger.info(f'Extracting columns: {", ".join(available_cols)} from {file_name}.')
    return df[available_cols]

def load_templates(template_name: str) -> tuple[str, str]:
    '''
    Loads in either an html or txt template, or both.
    :param str template_name: Name of the template, with no suffix. Should correspond to one of the directories under templates/
    :return: A tuple object where the first element is the .txt template and second is the .html template.
    Empty strings are returned if either are missing
    '''
    file_path = Path('templates') / template_name
    if not file_path.exists():
        logger.warning(f'Template {template_name} could not be found. Verify that a directory templates/{template_name} exists.')
        return ('', '') 
    
    txt_filename = ''
    html_filename = ''

    for filename in file_path.iterdir():
        if filename.endswith('.txt') and not txt_filename:
            txt_filename = filename
        elif txt_filename:
            logger.warning(f'Found multiple .txt files: {txt_filename} and {filename}. Will use first found file {txt_filename}.')
        
        if filename.endswith('.html') and not html_filename:
            html_filename = filename
        elif html_filename:
            logger.warning(f'Found multiple .html files: {html_filename} and {filename}. Will use first found file {html_filename}.')
    
    txt_template = ''
    html_template = ''

    if txt_filename:
        logger.info(f'Found text file: {txt_filename}. Loading in file.')
        txt_template = (Path(file_path) / txt_filename).read_text()
    else:
        logger.warning('No txt file found.')
    
    if html_filename:
        logger.info(f'Found html file: {html_filename}. Loading in file.')
        html_template = (Path(file_path) / html_filename).read_text()
    else:
        logger.warning('No html file found.')
    
    return (txt_template, html_template)


    
def login(server: smtplib.SMTPL_SSL, receiver_email: str = ''):
    '''
    Handle login either by secret files or by user input.
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
    
    server.login(sender_email, password)
