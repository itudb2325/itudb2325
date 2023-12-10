import mysql.connector
import pandas as pd
import numpy as np
from config import MYSQL_CONFIG

# connection details
mydb = mysql.connector.connect(**MYSQL_CONFIG)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS game_plays")

# query for creating the game_plays table
create_game_plays_table = '''
    CREATE TABLE game_plays(
        play_id VARCHAR(15) NOT NULL PRIMARY KEY,
        game_id INT NOT NULL,
        team_id_for INT,
        team_id_against INT,
        event VARCHAR(255),
        secondary_type VARCHAR(255),
        x INT,
        y INT,
        period INT,
        period_type VARCHAR(255),
        period_time INT,
        period_time_remaining INT,
        date_time DATETIME,
        goals_away INT,
        goals_home INT,
        description VARCHAR(255),
        st_x INT,
        st_y INT,

        FOREIGN KEY (team_id_for) REFERENCES team_info(team_id),
        FOREIGN KEY (team_id_against) REFERENCES team_info(team_id)
    )
'''

mycursor.execute(create_game_plays_table)

# read the data file
csv_file = pd.read_csv('nhl-db/game_plays.csv', usecols=[
    'play_id',
    'game_id',
    'team_id_for',
    'team_id_against',
    'event',
    'secondaryType',
    'x',
    'y',
    'period',
    'periodType',
    'periodTime',
    'periodTimeRemaining',
    'dateTime',
    'goals_away',
    'goals_home',
    'description',
    'st_x',
    'st_y'
])

csv_file.replace(['', 'NA'], None, inplace=True)
csv_file = csv_file.where(pd.notna(csv_file), None)
data_to_insert = csv_file.to_records(index=False).tolist()
data_to_insert = [tuple(None if pd.isna(value) else value for value in row) for row in data_to_insert]

insert_query = '''
    INSERT INTO game_plays
    (play_id,
    game_id,
    team_id_for,
    team_id_against,
    event,
    secondary_type,
    x,
    y,
    period,
    period_type,
    period_time,
    period_time_remaining,
    date_time,
    goals_away,
    goals_home,
    description,
    st_x,
    st_y)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

mycursor.executemany(insert_query, data_to_insert)

mydb.commit()
mydb.close()