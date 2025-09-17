from pathlib import Path
from loguru import logger
import pandas as pd
from jinja2 import Template

def extract_data(file_name: str, columns: list = []) -> pd.DataFrame:
    '''
    Either extracts specific columns, or just loads in dataframe including all columns
    if no argument is given to columns.
    Data is used for filling in arguments in templates.
    Supports both .json and .csv and will try to find both if no suffix is given.
    '''
    file_path = Path('data') / file_name
    if not file_path.exists():
        logger.warning(f'File {file_name} not found. Searching for {file_name}.csv and {file_name}.json...')

        csv_path = Path('data' / file_name + '.csv')
        json_path = Path('data' / file_name + '.json')

        if csv_path.exists():
            logger.info(f'Found file: {file_name}.csv')
            df = pd.read_csv(csv_path)
        elif json_path.exists():
            logger.info(f'Found file: {file_name}.json')
            df = pd.read_json(json_path)
        else:
            logger.warning(f'File {file_name} not found. Returning empty DataFrame.')
            return pd.DataFrame()
    else:
        try:
            df = pd.read_csv(file_path) if file_path.suffix == '.csv' else pd.read_json(file_path)
        except pd.errors.ParserError or pd.errors.ValueError:
            print('Malformed file. Provide a valid .csv or .json file.')
            return
    
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
    if len(available_cols) == 0:
        logger.error('No requested columns found. Returning empty DataFrame.')
        return pd.DataFrame()
     
    logger.info(f'Extracting columns: {", ".join(available_cols)} from {file_name}.')
    return df[available_cols]

def load_templates(template_name: str) -> tuple[Template, Template]:
    '''
    Loads in either an html or txt template, or both.
    :param str template_name: Name of the template, with no suffix. Should correspond to one of the directories under templates/
    :return: A tuple object where the first element is the .txt template and second is the .html template.
    Empty templates are returned if either are missing
    '''
    file_path = Path('templates') / template_name
    if not file_path.exists():
        logger.warning(f'Template {template_name} could not be found. Verify that a directory templates/{template_name} exists.')
        return (Template(''), Template(''))
    
    txt_file = None
    html_file = None

    for filename in file_path.iterdir():
        if filename.suffix == ".txt":
            if txt_file is None:
                txt_file = filename
            else:
                logger.warning(f'Found multiple .txt files: {txt_file} and {filename}. Will use first found file {txt_file}.')
        
        elif filename.suffix == ".html":
            if html_file is None:
                html_file = filename
            else:
                logger.warning(f'Found multiple .html files: {html_file} and {filename}. Will use first found file {html_file}.')
    
    txt_template = Template('')
    html_template = Template('')

    if txt_file:
        logger.info(f'Found text file: {txt_file}. Loading in file.')
        txt_template = Template(txt_file.read_text())
    else:
        logger.warning('No txt file found.')
    
    if html_file:
        logger.info(f'Found html file: {html_file}. Loading in file.')
        html_template = Template(html_file.read_text())
    else:
        logger.warning('No html file found.')
    
    return (txt_template, html_template)

def find_email_col(data: pd.DataFrame) -> tuple[pd.Series, str]:
    '''
    Finds column of data where emails are located
    Extracts this column
    :return: A tuple object consisting of the column and its name
    '''
    # Simple test: Checks for common column names
    candidates = ["mail", "email", "email_address", "contact_email", "user_email"]
    for cand in candidates:
        if cand in data.columns:
            logger.info(f"Using column {cand} as email column. Rename correct column to 'mail' if this is incorrect")
            return (data[cand], cand) 

    # None found -> search for @
    for col in data:
        if data[col].str.contains("@"):
            logger.info(f"Using column {col} as email column. Rename correct column to 'mail' if this is incorrect")
            return (data[col], col)
    
    logger.warning("No email column found.")
    return (pd.Series(dtype=str), "")

def find_subject_col(data: pd.DataFrame) -> tuple[pd.Series, str]:
    '''
    Similar to find_email_col - finds column where subjects are located
    :return: A tuple object consisting of the column and its name
    '''
    # Common subject names
    candidates = ["subject", "subject_line", "email_subject", "title", "heading"]
    for cand in candidates:
        if cand in data.columns:
            logger.info(f"Using column {cand} as subject line. Rename correct column to 'subject' if this is incorrect")
            return (data[cand], cand) 
    
    logger.warning("No subject column found.")
    return (pd.Series(dtype=str), "")