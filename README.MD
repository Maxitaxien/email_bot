# Python email helper

A simple email handler to allow for templating and sending of similar emails to
multiple people. Account to send from and login password can either be supplied in secrets through adding the files: `secrets/passwd` and `secrets/sender` (note no . suffix on these files) or can be input manually upon running the program.

For most gmail accounts, login through normal password is not supported within another application because of 2-factor authentication issues. 

To circumvent this, use Google App Passwords: https://myaccount.google.com/apppasswords. Here, you can create a password to use which supports use from within the app. 


Templates can be added in the `templates` folder. 

It is also supported to read in data from csv files which can be placed in the `data` folder through the use of the `extract_data` function placed in `helper_scripts.py`. This script also supports reading in of only specific columns from the csv file.

## Example usage

Example usage is illustrated through the templates/example/.



