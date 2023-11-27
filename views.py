from flask import abort, current_app, render_template
import mysql.connector
from config import MYSQL_CONFIG  # Assuming you have a configuration file

def index_page():
    return render_template("index.html")

def game_plays():
    return render_template("game_plays.html")

def game_skater_stats():
    return render_template("game_skater_stats.html")

def game_teams_stats():
    return render_template("game_teams_stats.html")

def get_goalie_stats():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier handling of results
    cursor.execute("SELECT * FROM game_goalie_stats")
    results = cursor.fetchall()
    conn.close()
    return results

def game_goalie_stats():
    goalie_stats = get_goalie_stats()
    return render_template("game_goalie_stats.html", goalie_stats=goalie_stats)