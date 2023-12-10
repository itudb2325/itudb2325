import mysql.connector
import pandas as pd
import numpy as np
from config import MYSQL_CONFIG

# connection details
mydb = mysql.connector.connect(**MYSQL_CONFIG)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS team_info")

# query for creating the team_info table
create_team_info_table = '''
    CREATE TABLE team_info(
        team_id INT NOT NULL PRIMARY KEY,
        franchise_id INT NOT NULL,
        short_name VARCHAR(255),
        team_name VARCHAR(255),
        abbreviation VARCHAR(255),
        link VARCHAR(255)
    )
'''

mycursor.execute(create_team_info_table)

# read the data file
csv_file = pd.read_csv('nhl-db/team_info.csv', usecols=[
    'team_id',
    'franchiseId',
    'shortName',
    'teamName',
    'abbreviation',
    'link'
])

csv_file.replace(['', 'NA'], None, inplace=True)
csv_file = csv_file.where(pd.notna(csv_file), None)
data_to_insert = csv_file.to_records(index=False).tolist()
data_to_insert = [tuple(None if pd.isna(value) else value for value in row) for row in data_to_insert]

insert_query = '''
    INSERT INTO team_info
    (team_id,
    franchise_id,
    short_name,
    team_name,
    abbreviation,
    link)
    VALUES (%s, %s, %s, %s, %s, %s)
'''

mycursor.executemany(insert_query, data_to_insert)

mydb.commit()
mydb.close()