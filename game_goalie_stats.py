import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG

class GoalieStats:
    def __init__(self, id, game_id, player_id, team_id, timeOnIce, shots, saves,
                 powerPlaySaves, evenSaves, evenShotsAgainst, powerPlayShotsAgainst):
        self.id = id
        self.game_id = game_id
        self.player_id = player_id
        self.team_id = team_id
        self.timeOnIce = timeOnIce
        self.shots = shots
        self.saves = saves
        self.powerPlaySaves = powerPlaySaves
        self.evenSaves = evenSaves
        self.evenShotsAgainst = evenShotsAgainst
        self.powerPlayShotsAgainst = powerPlayShotsAgainst

conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS game_goalie_stats")
game_goalie_stats_query = '''
    CREATE TABLE game_goalie_stats(
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        game_id INT NOT NULL,
        player_id INT NOT NULL,
        team_id INT,
        timeOnIce INT,
        shots INT,
        saves INT,
        powerPlaySaves INT,
        evenSaves INT,
        evenShotsAgainst INT,
        powerPlayShotsAgainst INT
    )
'''
cursor.execute(game_goalie_stats_query)

const_df = pd.read_csv('nhl-db/game_goalie_stats.csv', usecols=[
    'id',
    'game_id',
    'player_id',
    'team_id',
    'timeOnIce',
    'shots',
    'saves',
    'powerPlaySaves',
    'evenSaves',
    'evenShotsAgainst',
    'powerPlayShotsAgainst'
])

insert_query = '''
    INSERT INTO game_goalie_stats
    (id, game_id, player_id, team_id, timeOnIce, shots, saves,
    powerPlaySaves, evenSaves, evenShotsAgainst,
    powerPlayShotsAgainst)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
sorted_game_goalie_stats_df = const_df.sort_values(by=["id"], ascending=True)
game_goalie_stats_df = sorted_game_goalie_stats_df.head(50)

data_to_insert = game_goalie_stats_df.where(pd.notna(game_goalie_stats_df), None).to_numpy().tolist()
cursor.executemany(insert_query, data_to_insert)

conn.commit()
conn.close()

def create_goalie_stats(game_id, player_id, team_id, timeOnIce,
                        shots, saves, powerPlaySaves,
                        evenSaves, evenShotsAgainst, powerPlayShotsAgainst):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    create_query = '''INSERT INTO game_goalie_stats
    (game_id, player_id, team_id, timeOnIce, shots, saves,
    powerPlaySaves, evenSaves, evenShotsAgainst,
    powerPlayShotsAgainst)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(create_query, (game_id, player_id, team_id, timeOnIce,
                                  shots, saves, powerPlaySaves,
                                  evenSaves, evenShotsAgainst, powerPlayShotsAgainst))

    conn.commit()
    conn.close()

def update_goalie_stats(id, game_id, player_id, team_id,
            timeOnIce, shots, saves, powerPlaySaves,
            evenSaves, evenShotsAgainst, powerPlayShotsAgainst):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    update_query = '''UPDATE game_goalie_stats SET game_id = %s, 
        player_id = %s, team_id = %s, timeOnIce = %s, shots = %s, saves = %s, powerPlaySaves = %s, 
        evenSaves = %s, evenShotsAgainst = %s, powerPlayShotsAgainst = %s WHERE id = %s'''
    cursor.execute(update_query, (game_id, player_id, team_id, timeOnIce, 
                                  shots, saves, powerPlaySaves, evenSaves, 
                                  evenShotsAgainst, powerPlayShotsAgainst, id))

    conn.commit()
    conn.close()

def delete_goalie_stats_by_id(id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    delete_query = '''DELETE FROM game_goalie_stats WHERE id = %s'''
    cursor.execute(delete_query, (id,))

    conn.commit()
    conn.close()

