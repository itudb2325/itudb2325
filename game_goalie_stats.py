import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG


# Connect to MySQL using the configuration from config.py
conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor()

# Create game_goalie_stats table
cursor.execute("DROP TABLE IF EXISTS game_goalie_stats")
game_goalie_stats_query = '''
    CREATE TABLE game_goalie_stats(
        id INT NOT NULL PRIMARY KEY,
        game_id INT NOT NULL,
        player_id INT NOT NULL,
        team_id INT,
        timeOnIce INT,
        shots INT,
        saves INT,
        powerPlaySaves INT,
        shortHandedSaves INT,
        evenSaves INT,
        shortHandedShotsAgainst INT,
        evenShotsAgainst INT,
        powerPlayShotsAgainst INT,
        decision CHAR(1)
    )
'''
cursor.execute(game_goalie_stats_query)

# Read data from CSV
const_df = pd.read_csv('nhl-db/game_goalie_stats.csv', usecols=[
    'id',
    'game_id',
    'player_id',
    'team_id',
    'timeOnIce',
    'shots',
    'saves',
    'powerPlaySaves',
    'shortHandedSaves',
    'evenSaves',
    'shortHandedShotsAgainst',
    'evenShotsAgainst',
    'powerPlayShotsAgainst',
    'decision'
])

# Insert data into MySQL table using executemany
insert_query = '''
    INSERT INTO game_goalie_stats
    (id, game_id, player_id, team_id, timeOnIce, shots, saves,
    powerPlaySaves, shortHandedSaves, evenSaves, shortHandedShotsAgainst, evenShotsAgainst,
    powerPlayShotsAgainst, decision)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
sorted_game_goalie_stats_df = const_df.sort_values(by=["id"], ascending=True)
game_goalie_stats_df = sorted_game_goalie_stats_df.head(12)

data_to_insert = game_goalie_stats_df.where(pd.notna(game_goalie_stats_df), None).to_numpy().tolist()
cursor.executemany(insert_query, data_to_insert)

# Commit and close connection
conn.commit()
conn.close()