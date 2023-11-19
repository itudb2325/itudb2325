import sqlite3
import pandas as pd

from pathlib import Path
Path('static/game_goalie_stats.db').touch()
conn = sqlite3.connect('static/game_goalie_stats.db')
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS game_goalie_stats")
    
    
# constituents table
game_goalie_stats_query = '''
                    CREATE TABLE game_goalie_stats(
                        id int NOT NULL PRIMARY KEY,
                        game_id int NOT NULL,
                        player_id int NOT NULL,
                        team_id int,
                        timeOnIce int,
                        assists int,
                        goals int,
                        pim int,
                        shots int,
                        saves int,
                        powerPlaySaves int,
                        shortHandedSaves int,
                        evenSaves int,
                        shortHandedShotsAgainst int,
                        evenShotsAgainst int,
                        powerPlayShotsAgainst int,
                        decision char
                    )
                '''
c.execute(game_goalie_stats_query)
const_df = pd.read_csv('game_goalie_stats.csv', usecols=[
                        'id',
                        'game_id',
                        'player_id',
                        'team_id',
                        'timeOnIce',
                        'assists',
                        'goals',
                        'pim',
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
sorted_game_goalie_stats_df = const_df.sort_values(by=["game_id"], ascending=False)
game_goalie_stats_df = sorted_game_goalie_stats_df.head(10)
game_goalie_stats_df.to_sql('game_goalie_stats', conn, if_exists='append', index=False)
