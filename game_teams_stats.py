import csv
import mysql.connector
import pandas as pd
# import numpy as np
from config import MYSQL_CONFIG

connection = mysql.connector.connect(**MYSQL_CONFIG)

cursor = connection.cursor(buffered=True)
cursor.execute("DROP TABLE IF EXISTS game_teams_stats")

create = '''
            CREATE TABLE game_teams_stats(
                id INT PRIMARY KEY AUTO_INCREMENT,
                game_id INT,
                team_id INT,
                HoA VARCHAR(255),
                won VARCHAR(255),
                settled_in VARCHAR(255),
                head_coach VARCHAR(255),
                goals INT,
                shots INT,
                hits INT,
                pim INT,
                powerPlayOpportunities INT,
                powerPlayGoals INT,
                faceOffWinPercentage DOUBLE,
                giveaways INT,
                takeaways INT,
                blocked INT,
                startRinkSide VARCHAR(255)
            );
        '''

cursor.execute(create)

const_df = pd.read_csv('nhl-db/game_teams_stats_1.csv', usecols=[
    "game_id",
    "team_id",
    "HoA",
    "won",
    "settled_in",
    "head_coach",
    "goals",
    "shots",
    "hits",
    "pim",
    "powerPlayOpportunities",
    "powerPlayGoals",
    "faceOffWinPercentage",
    "giveaways",
    "takeaways",
    "blocked",
    "startRinkSide"
])

const_df.replace(['', 'NA'], None, inplace=True)
const_df = const_df.where(pd.notna(const_df), None)
data_to_insert = const_df.to_records(index=False).tolist()
data_to_insert = [tuple(None if pd.isna(value) else value for value in row) for row in data_to_insert]
data_to_insert = data_to_insert[:50]

insert = '''
            INSERT INTO game_teams_stats (game_id, team_id, HoA, won, settled_in, head_coach, goals, shots, hits, pim, powerPlayOpportunities, powerPlayGoals, faceOffWinPercentage, giveaways, takeaways, blocked, startRinkSide) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

cursor.executemany(insert, data_to_insert)

connection.commit()

cursor.close()
connection.close()

def create_teams(game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    create = '''
                    INSERT INTO game_teams_stats(game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
    cursor.execute(create, (game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide))

    connection.commit()
    cursor.close()
    connection.close()

def update_teams(id,game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    update = '''
                    UPDATE game_teams_stats SET game_id = %s, team_id = %s, HoA = %s, won = %s, settled_in = %s, head_coach = %s, goals = %s, shots = %s, hits = %s, pim = %s, powerPlayOpportunities = %s, powerPlayGoals = %s, faceOffWinPercentage = %s, giveaways = %s, takeaways = %s, blocked = %s, startRinkSide = %s
                    WHERE id = %s
                '''
    cursor.execute(update, (game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide,id))

    connection.commit()
    cursor.close()
    connection.close()

def delete_teams_stats_by_id(id):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    delete = '''
                    DELETE FROM game_teams_stats 
                    WHERE id = %s
                '''
    cursor.execute(delete, (id,))

    connection.commit()
    cursor.close()
    connection.close()