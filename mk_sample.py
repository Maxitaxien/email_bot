import pandas as pd

'''
Simple script to create some sample data. 
Filled in with my email + an extension.
'''

df = pd.DataFrame({
    'name': ['Bob', 'Alice'], 
    'email': ['max.bakke.seymour+bob@gmail.com', 'max.bakke.seymour+alice@gmail.com'],
    'book_title': ['The Wizard Of Oz', 'The Lord of The Rings'],
    'status': ['overdue', 'soon overdue']
    })

df.to_csv('data/library_data.csv')