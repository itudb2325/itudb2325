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
    


    )



'''  