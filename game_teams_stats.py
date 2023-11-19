import csv
import MySQLdb

with open("\nhl-db\game_teams_stats.csv", 'r') as file:
    reader = csv.reader(file)

    connection = MySQLdb.connect(
                                    host="127.0.0.1",
                                    user="root",
                                    password="a7F0JK!r",
                                    db="nhl-db"
                                )

    cursor = connection.cursor()

    create = '''
                CREATE TABLE game_teams_stats(
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
                    startRinkSide VARCHAR(255), 
                    FOREIGN KEY (game_id)
                        REFERENCES game(game_id),
                    FOREIGN KEY (team_id)
                        REFERENCES team_info(tema_id)
                );
            '''

    cursor.execute(create)

    insert = '''
                INSERT INTO game_teams_stats (game_id, team_id, HoA, won, settled_in, head_coach, goals, shots, hits, pim, powerPlayOpportunities, powerPlayGoals, faceOffWinPercentage, giveaways, takeaways,blocked, startRinkSide) 
                VALUES(%(game_id)s, %(team_id)s, %(HoA)s, %(won)s, %(settled_in)s, %(head_coach)s, %(goals)s, %(shots)s, %(hits)s, %(pim)s, %(powerPlayOpportunities)s, %(powerPlayGoals)s, %(faceOffWinPercentage)s, %(giveaways)s, %(takeaways)s, %(blocked)s, %(startRinkSide)s);
            '''

    for row in reader:
        cursor.execute(insert, row)

    connection.commit()

cursor.close()
connection.close()