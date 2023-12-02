from flask import Flask, current_app, abort, render_template, request, redirect, url_for
import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG  # Assuming you have a configuration file
from game_goalie_stats import delete_goalie_stats_by_id, create_goalie_stats, update_goalie_stats
import os

def configure_app(app):
    img = os.path.join('static', 'img')
    app.config['UPLOAD_FOLDER'] = img

app = Flask(__name__)
configure_app(app)

def generate_image_paths():
    img_logo_path = '05_NHL_Shield.svg.webp' 
    img_youtube_path = 'youtube_logo.png'
    img_x_path = 'x_logo.png'
    img_instagram_path = 'instagram_logo.png'
    img_facebook_path = 'facebook_logo.png'
    
    full_img_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], img_logo_path)
    full_img_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], img_youtube_path)
    full_img_path3 = os.path.join(current_app.config['UPLOAD_FOLDER'], img_x_path)
    full_img_path4 = os.path.join(current_app.config['UPLOAD_FOLDER'], img_instagram_path)
    full_img_path5 = os.path.join(current_app.config['UPLOAD_FOLDER'], img_facebook_path)
    
    return {
        'icon': full_img_path1,
        'nhl_logo': full_img_path1,
        'youtube': full_img_path2,
        'x': full_img_path3,
        'instagram': full_img_path4,
        'facebook': full_img_path5,
    }

def index_page():
    image_paths = generate_image_paths()
    return render_template('index.html', **image_paths, active_page = 'index')

def game_plays():
    image_paths = generate_image_paths()
    return render_template("game_plays.html", **image_paths, active_page = 'game_plays')

def game_skater_stats():
    return render_template("game_skater_stats.html")

def game_teams_stats():
    return render_template("game_teams_stats.html")

def get_goalie_stats():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM game_goalie_stats")
    results = cursor.fetchall()
    conn.close()
    return results

def get_goalie_stats_by_id(id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier handling of results
    cursor.execute("SELECT * FROM game_goalie_stats WHERE id = %s", (id,))
    results = cursor.fetchall()
    conn.close()
    return results

def game_goalie_stats():
    goalie_stats = get_goalie_stats()
    return render_template("game_goalie_stats.html", goalie_stats=goalie_stats)

def delete_goalie_stats():
    if request.method == 'POST':
        id = request.form.get('id')
        delete_goalie_stats_by_id(id)

    return redirect(url_for('game_goalie_stats'))

def update_goalie(id):
    if request.method == 'GET':
        goalie_stats = get_goalie_stats_by_id(id)
        return render_template('update_goalie.html', id=id, goalie_stats=goalie_stats)

    else:
        game_id = request.form.get('game_id')
        player_id = request.form.get('player_id')
        team_id = request.form.get('team_id')
        timeOnIce = request.form.get('timeOnIce')
        shots = request.form.get('shots')
        saves = request.form.get('saves')
        powerPlaySaves = request.form.get('powerPlaySaves')
        evenSaves = request.form.get('evenSaves')
        evenShotsAgainst = request.form.get('evenShotsAgainst')
        powerPlayShotsAgainst = request.form.get('powerPlayShotsAgainst')

        update_goalie_stats(id, game_id, player_id, team_id, timeOnIce, 
                            shots, saves, powerPlaySaves, evenSaves, 
                            evenShotsAgainst, powerPlayShotsAgainst)

        return redirect(url_for('game_goalie_stats'))

def create_goalie():
    if request.method == 'GET':
        return render_template('create_goalie.html')

    else:
        game_id = request.form.get('game_id')
        player_id = request.form.get('player_id')
        team_id = request.form.get('team_id')
        timeOnIce = request.form.get('timeOnIce')
        shots = request.form.get('shots')
        saves = request.form.get('saves')
        powerPlaySaves = request.form.get('powerPlaySaves')
        evenSaves = request.form.get('evenSaves')
        evenShotsAgainst = request.form.get('evenShotsAgainst')
        powerPlayShotsAgainst = request.form.get('powerPlayShotsAgainst')

        create_goalie_stats(game_id, player_id, team_id, timeOnIce, 
                            shots, saves, powerPlaySaves, evenSaves, 
                            evenShotsAgainst, powerPlayShotsAgainst)

        return redirect(url_for('game_goalie_stats'))
