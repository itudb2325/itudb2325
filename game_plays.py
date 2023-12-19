import mysql.connector
import pandas as pd
import numpy as np
from config import MYSQL_CONFIG
from team_info import create_team_info

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
        date_time VARCHAR(255),
        goals_away INT,
        goals_home INT,
        description VARCHAR(255),
        st_x INT,
        st_y INT
    )
'''

mycursor.execute(create_game_plays_table)

#create_team_info();
#
#foreign_key_query = '''
#    ALTER TABLE game_plays
#    FOREIGN KEY (team_id_for)
#    REFERENCES team_info(team_id)
#    ON UPDATE CASCADE
#    ON DELETE CASCADE;
#'''
#mycursor.execute(foreign_key_query)
#
#foreign_key_query = '''
#    ALTER TABLE game_plays
#    FOREIGN KEY (team_id_against)
#    REFERENCES team_info(team_id)
#    ON UPDATE CASCADE
#    ON DELETE CASCADE;
#'''
#mycursor.execute(foreign_key_query)

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

csv_file.replace(['', 'NA'], None, inplace = True)
csv_file = csv_file.where(pd.notna(csv_file), None)
csv_file = csv_file.sort_values(by = 'dateTime', ascending = True)
data_to_insert = csv_file.to_records(index = False).tolist()
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

def update_game(play_id, game_id, team_id_for, team_id_against, event, secondary_type,
                x, y, period, period_type, period_time, period_time_remaining, date_time,
                goals_away, goals_home, description, st_x, st_y):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    update_query = '''
        UPDATE game_plays
        SET
            game_id = %s,
            team_id_for = %s,
            team_id_against = %s,
            event = %s,
            secondary_type = %s,
            x = %s,
            y = %s,
            period = %s,
            period_type = %s,
            period_time = %s,
            period_time_remaining = %s,
            date_time = %s,
            goals_away = %s,
            goals_home = %s,
            description = %s,
            st_x = %s,
            st_y = %s
        WHERE
            play_id = %s
    '''

    cursor.execute(update_query, (game_id, team_id_for, team_id_against, event, secondary_type,
                                    x, y, period, period_type, period_time, period_time_remaining, date_time,
                                    goals_away, goals_home, description, st_x, st_y, play_id))

    connection.commit()
    cursor.close()
    connection.close()

def create_game(play_id, game_id, team_id_for, team_id_against, event, secondary_type,
                x, y, period, period_type, period_time, period_time_remaining, date_time,
                goals_away, goals_home, description, st_x, st_y):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    create_query = '''
        INSERT INTO game_plays
        SET
            play_id = %s,
            game_id = %s,
            team_id_for = %s,
            team_id_against = %s,
            event = %s,
            secondary_type = %s,
            x = %s,
            y = %s,
            period = %s,
            period_type = %s,
            period_time = %s,
            period_time_remaining = %s,
            date_time = %s,
            goals_away = %s,
            goals_home = %s,
            description = %s,
            st_x = %s,
            st_y = %s
    '''

    cursor.execute(create_query, (play_id, game_id, team_id_for, team_id_against, event, secondary_type,
                                    x, y, period, period_type, period_time, period_time_remaining, date_time,
                                    goals_away, goals_home, description, st_x, st_y))

    connection.commit()
    cursor.close()
    connection.close()

def delete_game_plays_by_id(play_id):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    delete_query = '''
        DELETE FROM game_plays
        WHERE play_id = %s
    '''

    cursor.execute(delete_query, (play_id,))

    connection.commit()
    cursor.close()
    connection.close()