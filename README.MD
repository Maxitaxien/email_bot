# Python email helper

A simple email handler to allow for templating and sending of similar emails to
multiple people. Account to send from and login password can either be supplied in secrets through adding the files: `secrets/passwd` and `secrets/sender` (note no . suffix on these files).

Templates can be added in the `templates` folder. 

It is also supported to read in data from csv files which can be placed in the `data` folder. If you wish to extract only certain columns from the csv files to use in templating this can be done with the `data_extraction_script.py` file.

