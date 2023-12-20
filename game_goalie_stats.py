import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG

#The game_goalie_stats table
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

#creating the player_info table

#Filtering the player_id column in player_info
cursor.execute("SELECT DISTINCT player_id FROM game_goalie_stats")
existing_player_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("DROP TABLE IF EXISTS player_info")
player_info_query = '''
    CREATE TABLE player_info(
        player_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        firstName varchar(20),
        lastName varchar(20),
        nationality varchar(10),
        birthCity varchar(40),
        primaryPosition varchar(10),
        height_cm double,
        shootsCatches char
    )
'''
cursor.execute(player_info_query)

const_df = pd.read_csv('nhl-db/player_info.csv', usecols=[
    'player_id',
    'firstName',
    'lastName',
    'nationality',
    'birthCity',
    'primaryPosition',
    'height_cm',
    'shootsCatches'
])

# Filter rows based on existing_player_ids
filtered_player_info_df = const_df[const_df['player_id'].isin(existing_player_ids)]

insert_query = '''
    INSERT INTO player_info
    (player_id, firstName, lastName, nationality, birthCity, 
    primaryPosition, height_cm, shootsCatches)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
'''
sorted_player_info_df = filtered_player_info_df.sort_values(by=["player_id"], ascending=True)
player_info_df = sorted_player_info_df

data_to_insert = player_info_df.where(pd.notna(player_info_df), None).to_numpy().tolist()
cursor.executemany(insert_query, data_to_insert)

foreign_key_query = '''
ALTER TABLE game_goalie_stats
ADD CONSTRAINT my_foreign_key
FOREIGN KEY (player_id)
REFERENCES player_info(player_id)
ON UPDATE CASCADE
ON DELETE CASCADE;
'''
cursor.execute(foreign_key_query)


#creating the team_info table
#Doing the same filtering
cursor.execute("SELECT DISTINCT team_id FROM game_goalie_stats")
existing_team_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
cursor.execute("DROP TABLE IF EXISTS team_info")
cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
team_info_query = '''
    CREATE TABLE team_info(
        team_id INT NOT NULL PRIMARY KEY,
        franchiseId INT,
        shortName varchar(50),
        teamName varchar(50),
        abbreviation varchar(10)
    )
'''
cursor.execute(team_info_query)

const_df = pd.read_csv('nhl-db/team_info.csv', usecols=[
    'team_id',
    'franchiseId',
    'shortName',
    'teamName',
    'abbreviation'
])

insert_query = '''
    INSERT INTO team_info
    (team_id, franchiseId, shortName, teamName, abbreviation)
    VALUES (%s, %s, %s, %s, %s)
'''
sorted_team_df = const_df.sort_values(by=["team_id"], ascending=True)
team_info_df = sorted_team_df

data_to_insert = team_info_df.where(pd.notna(team_info_df), None).to_numpy().tolist()
cursor.executemany(insert_query, data_to_insert)

foreign_key_query = '''
ALTER TABLE game_goalie_stats
ADD CONSTRAINT my_foreign_key2
FOREIGN KEY (team_id)
REFERENCES team_info(team_id)
ON UPDATE CASCADE
ON DELETE CASCADE;
'''
cursor.execute(foreign_key_query)

#Create game.csv
cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
cursor.execute("DROP TABLE IF EXISTS game")
cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
game_query = '''
    CREATE TABLE game(
        game_id INT NOT NULL PRIMARY KEY,
        away_team_id INT,
        home_team_id INT,
        outcome varchar(50),
        venue varchar(40)
    )
'''
cursor.execute(game_query)

const_df = pd.read_csv('nhl-db/game.csv', usecols=[
    'game_id',
    'away_team_id',
    'home_team_id',
    'outcome',
    'venue'
])

insert_query = '''
    INSERT INTO game
    (game_id, away_team_id, home_team_id, outcome, venue)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    away_team_id = VALUES(away_team_id),
    home_team_id = VALUES(home_team_id),
    outcome = VALUES(outcome),
    venue = VALUES(venue)
'''
sorted_game_df = const_df.sort_values(by=["game_id"], ascending=True)
game_df = sorted_game_df

data_to_insert = game_df.where(pd.notna(game_df), None).to_numpy().tolist()
cursor.executemany(insert_query, data_to_insert)

cursor.execute("DROP VIEW IF EXISTS game_team")
view_query = '''
        CREATE VIEW game_team AS
        SELECT
        	game.game_id,
            game.venue,
            game.away_team_id,
            team_info.teamName AS away_team_name,
            game.home_team_id,
            team_info_home.teamName AS home_team_name,
            game.outcome
        FROM
            game
        INNER JOIN
            team_info ON game.away_team_id = team_info.team_id
        INNER JOIN
            team_info AS team_info_home ON game.home_team_id = team_info_home.team_id;
'''
cursor.execute(view_query)

conn.commit()
cursor.close()
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

def get_goalie_info():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    info_query = '''
        select goalie.id, game.venue, game.away_team_name, game.home_team_name, game.outcome,
        player.firstName, player.lastName, player.birthCity, team.shortName, team.teamName
        from game_goalie_stats goalie
        inner join player_info player on goalie.player_id = player.player_id
        inner join team_info team on goalie.team_id = team.team_id
        inner join game_team game on goalie.game_id = game.game_id 
    '''
    cursor.execute(info_query)
    results = cursor.fetchall()

    conn.commit()
    conn.close()
    return results

def get_goalie_info_by_id(id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    info_query = '''
        select goalie.id, game.venue, game.away_team_name, game.home_team_name, game.outcome,
        player.firstName, player.lastName, player.birthCity, team.shortName, team.teamName
        from game_goalie_stats goalie
        inner join player_info player on goalie.player_id = player.player_id
        inner join team_info team on goalie.team_id = team.team_id
        inner join game_team game on goalie.game_id = game.game_id 
        where goalie.id = %s;
    '''
    cursor.execute(info_query, (id,))
    results = cursor.fetchall()

    conn.commit()
    conn.close()
    return results


def update_goalie_stats(id,
            timeOnIce, shots, saves, powerPlaySaves,
            evenSaves, evenShotsAgainst, powerPlayShotsAgainst):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()


    update_query = '''UPDATE game_goalie_stats SET timeOnIce = %s, shots = %s, saves = %s, powerPlaySaves = %s, 
        evenSaves = %s, evenShotsAgainst = %s, powerPlayShotsAgainst = %s WHERE id = %s'''
    cursor.execute(update_query, (timeOnIce, 
                                  shots, saves, powerPlaySaves, evenSaves, 
                                  evenShotsAgainst, powerPlayShotsAgainst, id))

    conn.commit()
    conn.close()


def update_player(player_id, firstName, lastName, nationality, birthCity, 
    primaryPosition, height_cm, shootsCatches):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    update_query = '''UPDATE player_info SET firstName = %s, lastName = %s, nationality = %s, birthCity = %s, 
    primaryPosition = %s, height_cm = %s, shootsCatches = %s WHERE player_id = %s'''
    cursor.execute(update_query, (firstName, lastName, nationality, birthCity, 
    primaryPosition, height_cm, shootsCatches, player_id,))

    conn.commit()
    conn.close()

def delete_goalie_stats_by_id(id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    delete_query = '''DELETE FROM game_goalie_stats WHERE id = %s'''
    cursor.execute(delete_query, (id,))

    conn.commit()
    conn.close()

def delete_player_by_id(player_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    delete_query = '''DELETE FROM player_info WHERE player_id = %s'''
    cursor.execute(delete_query, (player_id,))

    conn.commit()
    conn.close()

