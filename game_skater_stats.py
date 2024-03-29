import mysql.connector
import pandas as pd
import numpy as np
from config import MYSQL_CONFIG

#we need to make a connection
mydb = mysql.connector.connect(**MYSQL_CONFIG)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS game_skater_stats")

create_game_skater_stats_table = '''
    CREATE table game_skater_stats(
        id INT AUTO_INCREMENT PRIMARY KEY,
      
        game_id INT,
        player_id INT NOT NULL , 
        team_id INT,
        timeOnIce INT,
        assists INT,
        goals INT,
        shots INT,
        hits INT,
        powerPlayGoals INT,
        powerPlayAssists INT,
        penaltyMinutes INT,
        faceOffWins INT,
        faceoffTaken INT,
        takeaways INT,
        giveaways INT,
        shortHandedGoals INT,
        shortHandedAssists INT,
        blocked INT,
        plusMinus INT,
        evenTimeOnIce INT,
        shortHandedTimeOnIce INT,
        powerPlayTimeOnIce INT,
        
        FOREIGN KEY (team_id) REFERENCES team_info(team_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (game_id) REFERENCES game(game_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES player_info(player_id) ON UPDATE CASCADE ON DELETE CASCADE

    

    )



'''  

mycursor.execute(create_game_skater_stats_table)

csv_file= pd.read_csv('nhl-db/game_skater_stats.csv', usecols=[
         
        'game_id',
        'player_id',
        'team_id',
        'timeOnIce',
        'assists',
        'goals',
        'shots',
        'hits',
        'powerPlayGoals',
        'powerPlayAssists',
        'penaltyMinutes',
        'faceOffWins',
        'faceoffTaken',
        'takeaways',
        'giveaways',
        'shortHandedGoals',
        'shortHandedAssists',
        'blocked',
        'plusMinus',
        'evenTimeOnIce',
        'shortHandedTimeOnIce',
        'powerPlayTimeOnIce'

])

# Replace empty and 'NA' values with None
csv_file.replace(['', 'NA'], None, inplace=True)
csv_file = csv_file.where(pd.notna(csv_file), None)



insert_query = '''
    INSERT INTO game_skater_stats(

    game_id ,
    player_id , 
    team_id ,
    timeOnIce ,
    assists ,
    goals ,
    shots ,
    hits ,
    powerPlayGoals ,
    powerPlayAssists ,
    penaltyMinutes ,
    faceOffWins ,
    faceoffTaken ,
    takeaways ,
    giveaways ,
    shortHandedGoals ,
    shortHandedAssists ,
    blocked ,
    plusMinus ,
    evenTimeOnIce ,
    shortHandedTimeOnIce ,
    powerPlayTimeOnIce )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)


'''
# Convert DataFrame to records and insert into MySQL
data_to_insert = csv_file.to_records(index=False).tolist()
data_to_insert = [tuple(None if pd.isna(value) else value for value in row) for row in data_to_insert]
mycursor.executemany(insert_query, data_to_insert)

# Commit the changes
mydb.commit()

def update_game_skater (  id,  game_id ,player_id , team_id ,timeOnIce , assists ,goals ,shots ,hits ,powerPlayGoals ,powerPlayAssists,penaltyMinutes ,faceOffWins ,faceoffTaken ,takeaways ,giveaways ,shortHandedGoals , shortHandedAssists , blocked , plusMinus ,evenTimeOnIce , shortHandedTimeOnIce ,powerPlayTimeOnIce ):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    update = '''
                    UPDATE game_skater_stats SET game_id = %s, player_id = %s, team_id = %s, timeOnIce = %s, assists = %s, goals = %s, shots = %s, hits = %s, powerPlayGoals = %s, powerPlayAssists = %s, penaltyMinutes= %s, faceOffWins= %s, faceoffTaken= %s,takeaways= %s,giveaways= %s,shortHandedGoals= %s,shortHandedAssists= %s,blocked= %s,plusMinus= %s,evenTimeOnIce= %s,shortHandedTimeOnIce= %s,powerPlayTimeOnIce= %s
                    WHERE id = %s
                '''
    cursor.execute(update, ( game_id ,player_id , team_id ,timeOnIce , assists ,goals ,shots ,hits ,powerPlayGoals ,powerPlayAssists,penaltyMinutes ,faceOffWins ,faceoffTaken ,takeaways ,giveaways ,shortHandedGoals , shortHandedAssists , blocked , plusMinus ,evenTimeOnIce , shortHandedTimeOnIce ,powerPlayTimeOnIce , id))

    connection.commit()
    cursor.close()
    connection.close()

def delete_skater_stats_by_id(id):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    delete = '''
                    DELETE FROM game_skater_stats 
                    WHERE id = %s
                '''
    cursor.execute(delete, (id,))

    connection.commit()
    cursor.close()
    connection.close()

def create_skater(game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, powerPlayGoals, powerPlayAssists, penaltyMinutes, faceOffWins, faceoffTaken, takeaways, giveaways, shortHandedGoals, shortHandedAssists, blocked, plusMinus, evenTimeOnIce, shortHandedTimeOnIce, powerPlayTimeOnIce):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    create = '''
        INSERT INTO game_skater_stats(
            game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, 
            powerPlayGoals, powerPlayAssists, penaltyMinutes, faceOffWins, faceoffTaken, 
            takeaways, giveaways, shortHandedGoals, shortHandedAssists, blocked, plusMinus, 
            evenTimeOnIce, shortHandedTimeOnIce, powerPlayTimeOnIce
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(create, (game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, powerPlayGoals, powerPlayAssists, penaltyMinutes, faceOffWins, faceoffTaken, takeaways, giveaways, shortHandedGoals, shortHandedAssists, blocked, plusMinus, evenTimeOnIce, shortHandedTimeOnIce, powerPlayTimeOnIce))

    

    connection.commit()
    cursor.close()
    connection.close()

