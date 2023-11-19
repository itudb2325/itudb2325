from datetime import datetime

from flask import abort, current_app, render_template
import sqlite3


def index_page():
    return render_template("index.html")

def game_plays():
    return render_template("game_plays.html")


def game_skater_stats():
    return render_template("game_skater_stats.html")


def game_teams_stats():
    return render_template("game_teams_stats.html")

def get_goalie_stats():
    conn = sqlite3.connect('static/game_goalie_stats.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game_goalie_stats")
    results = cursor.fetchall()
    conn.close()
    return results

def game_goalie_stats(): #goalie stats page
    game_goalie_stats = get_goalie_stats()

    return render_template("game_goalie_stats.html", const=game_goalie_stats)