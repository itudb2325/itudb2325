from flask import Flask, current_app, abort, render_template, request, redirect, url_for
import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG  # Assuming you have a configuration file
from game_goalie_stats import delete_goalie_stats_by_game_id
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
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier handling of results
    cursor.execute("SELECT * FROM game_goalie_stats")
    results = cursor.fetchall()
    conn.close()
    return results

def game_goalie_stats():
    goalie_stats = get_goalie_stats()
    return render_template("game_goalie_stats.html", goalie_stats=goalie_stats)

def upload_goalie_stats():
    if request.method == 'POST':
        # Get form data
        game_id = request.form.get('game_id')
        # Repeat the above line for each column

        # Create a dictionary with column names and form data
        new_data_dict = {
            'game_id': game_id,
            # Repeat the above line for each column
        }

        # Convert the dictionary to a DataFrame
        new_data_df = pd.DataFrame([new_data_dict])

        # Call the function to upload the new data
        upload_goalie_stats(new_data_df)

    # Redirect to the goalie stats page after the upload
    return redirect(url_for('game_goalie_stats'))

def delete_goalie_stats():
    if request.method == 'POST':
        # Get the game_id to delete
        game_id_to_delete = request.form.get('gameIdToDelete')

        # Call the function to delete records by game_id
        delete_goalie_stats_by_game_id(game_id_to_delete)

    # Redirect to the goalie stats page after the delete
    return redirect(url_for('game_goalie_stats'))