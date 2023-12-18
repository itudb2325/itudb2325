from flask import Flask, current_app, abort, render_template, request, redirect, url_for
import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG  # Assuming you have a configuration file
from game_goalie_stats import delete_goalie_stats_by_id, delete_player_by_id, create_goalie_stats, update_goalie_stats, update_player, get_goalie_info, get_goalie_info_by_id
from game_teams_stats import delete_teams_stats_by_id, create_teams, update_teams
from game_skater_stats import update_game_skater
from game_plays import update_game
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

# Game Plays

def game_plays():
    game_plays = get_game_plays()
    return render_template("game_plays.html", active_page = 'game_plays', game_plays = game_plays)

def get_game_plays():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    game_plays_query = "SELECT play_id, game_id, team_id_for as team1, team_id_against as team2 FROM game_plays"
    #, game_schedule_time, game_finish_time, number_of_goals, number_of_face_offs, number_of_shots, number_of_missed_shots, number_of_takeaways
    cursor.execute(game_plays_query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_game_plays_by_id(play_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    game_plays_query = "SELECT * FROM game_plays WHERE play_id = %s"
    cursor.execute(game_plays_query, (play_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def update_game_plays(play_id):
    if request.method == 'GET':
        game_plays = get_game_plays_by_id(play_id)
        return render_template('update_game_plays.html', play_id = play_id, results = game_plays)
    else:
        game_id = request.form.get('game_id')
        team_id_for = request.form.get('team_id_for')
        team_id_against = request.form.get('team_id_against')
        event = request.form.get('event')
        secondary_type = request.form.get('secondary_type')
        x = request.form.get('x')
        y = request.form.get('y')
        period = request.form.get('period')
        period_type = request.form.get('period_type')
        period_time = request.form.get('period_time')
        period_time_remaining = request.form.get('period_time_remaining')
        date_time = request.form.get('date_time')
        goals_away = request.form.get('goals_away')
        goals_home = request.form.get('goals_home')
        description = request.form.get('description')
        st_x = request.form.get('st_x')
        st_y = request.form.get('st_y')

        update_game(play_id, game_id, team_id_for, team_id_against, event, secondary_type,
                     x, y, period, period_type, period_time, period_time_remaining, date_time,
                     goals_away, goals_home, description, st_x, st_y)
        return redirect(url_for('game_plays'))

# Game Skater Stats
def get_skater_stats():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT id, game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, powerPlayGoals, powerPlayAssists FROM game_skater_stats")
    results = cursor.fetchall()
    # for i in results:
    #     print(i)
    conn.close()
    return results

def get_skater_stats_by_id(id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier handling of results
    cursor.execute("SELECT id, game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, powerPlayGoals, powerPlayAssists FROM game_skater_stats WHERE id = %s", (id,))
    results = cursor.fetchall()
    conn.close()
    return results


  


def game_skater_stats():

    skater_stats = get_skater_stats()
    return render_template("game_skater_stats.html", results=skater_stats)

def update_skater_stats(id):
    if request.method == 'GET':
        skater_stats = get_skater_stats_by_id(id)
        return render_template('update_skater_stats.html',id=id, results=skater_stats)
    else:
        game_id = request.form.get('game_id')
        player_id = request.form.get('player_id')
        team_id = request.form.get('team_id')
        timeOnIce = request.form.get('timeOnIce')
        assists = request.form.get('assists')
        goals = request.form.get('goals')
        shots = request.form.get('shots')
        hits = request.form.get('hits')
        powerPlayGoals = request.form.get('powerPlayGoals')
        powerPlayAssists = request.form.get('powerPlayAssists')

        update_game_skater(id, game_id, player_id, team_id, timeOnIce, 
                            assists, goals, shots, hits, 
                            powerPlayGoals, powerPlayAssists)

        return redirect(url_for('game_skater_stats'))




#Game Goalie Stats Table
# Game Goalie Stats

def get_goalie_stats():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM game_goalie_stats")
    results = cursor.fetchall()
    conn.close()
    return results

def get_player_info():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM player_info")
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

def get_player_info_by_id(player_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM player_info WHERE player_id = %s", (player_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def game_goalie_stats():
    goalie_stats = get_goalie_stats()
    player_info = get_player_info()
    goalie_info = get_goalie_info()
    return render_template("game_goalie_stats.html", goalie_stats=goalie_stats, player_info=player_info, active_page = 'game_goalie_stats', goalie_info=goalie_info)

def delete_goalie_stats():
    if request.method == 'POST':
        id = request.form.get('id')
        delete_goalie_stats_by_id(id)

    return redirect(url_for('game_goalie_stats'))

def delete_player():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        delete_player_by_id(player_id)

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
    
def update_player_info(player_id):
    if request.method == 'GET':
        player_info = get_player_info_by_id(player_id)
        return render_template('update_player.html', player_id=player_id, player_info=player_info)

    else:
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        nationality = request.form.get('nationality')
        birthCity = request.form.get('birthCity')
        primaryPosition = request.form.get('primaryPosition')
        height_cm = request.form.get('height_cm')
        
        update_player(player_id, firstName, lastName, nationality, birthCity, 
    primaryPosition, height_cm)

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
    
    
def search_by_game_id(game_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM game_goalie_stats WHERE game_id LIKE %s", (str(game_id) + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def search_goalie_stats():
    if request.method == 'POST':
        search_val = request.form.get('search')
        goalie_stats = search_by_game_id(search_val)
        player_info = get_player_info()
        goalie_info = get_goalie_info()
        return render_template("game_goalie_stats.html", goalie_stats=goalie_stats, player_info=player_info, goalie_info=goalie_info)

    return render_template("game_goalie_stats.html")

def goalie_info(id):
    if request.method == 'GET':
        info = get_goalie_info_by_id(id)
        return render_template('game_goalie_stats.html', id=id, goalie_info=info)

        

    

# Game Teams Stats

def get_teams_stats():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM game_teams_stats")
    results = cursor.fetchall()
    conn.close()
    return results

def get_teams_stats_by_id(id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier handling of results
    cursor.execute("SELECT * FROM game_teams_stats WHERE id = %s", (id,))
    results = cursor.fetchall()
    conn.close()
    return results

def game_teams_stats():
    teams_stats = get_teams_stats()
    return render_template("game_teams_stats.html", teams_stats=teams_stats)

def delete_teams_stats():
    if request.method == 'POST':
        id = request.form.get('id')
        delete_teams_stats_by_id(id)

    return redirect(url_for('game_teams_stats'))

def update_teams_stats(id):
    if request.method == 'GET':
        teams_stats = get_teams_stats_by_id(id)
        return render_template('update_teams_stats.html', id=id, teams_stats=teams_stats)

    else:
        game_id = request.form.get('game_id')
        team_id = request.form.get('team_id')
        HoA = request.form.get('HoA')
        won = request.form.get('won')
        settled_in = request.form.get('settled_in')
        head_coach = request.form.get('head_coach')
        goals = request.form.get('goals')
        shots = request.form.get('shots')
        hits = request.form.get('hits')        
        pim = request.form.get('pim')
        powerPlayOpportunities = request.form.get('powerPlayOpportunities')
        powerPlayGoals = request.form.get('powerPlayGoals')
        faceOffWinPercentage = request.form.get('faceOffWinPercentage')
        giveaways = request.form.get('giveaways')
        takeaways = request.form.get('takeaways')
        blocked = request.form.get('blocked')
        startRinkSide = request.form.get('startRinkSide')

        update_teams(id,game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide)

        return redirect(url_for('game_teams_stats'))

def create_teams_stats():
    if request.method == 'GET':
        return render_template('create_teams_stats.html')

    else:
        game_id = request.form.get('game_id')
        team_id = request.form.get('team_id')
        HoA = request.form.get('HoA')
        won = request.form.get('won')
        settled_in = request.form.get('settled_in')
        head_coach = request.form.get('head_coach')
        goals = request.form.get('goals')
        shots = request.form.get('shots')
        hits = request.form.get('hits')        
        pim = request.form.get('pim')
        powerPlayOpportunities = request.form.get('powerPlayOpportunities')
        powerPlayGoals = request.form.get('powerPlayGoals')
        faceOffWinPercentage = request.form.get('faceOffWinPercentage')
        giveaways = request.form.get('giveaways')
        takeaways = request.form.get('takeaways')
        blocked = request.form.get('blocked')
        startRinkSide = request.form.get('startRinkSide')

        create_teams(game_id,team_id,HoA,won,settled_in,head_coach,goals,shots,hits,pim,powerPlayOpportunities,powerPlayGoals,faceOffWinPercentage,giveaways,takeaways,blocked,startRinkSide)

        return redirect(url_for('game_teams_stats'))

def search_teams_by_game_id(game_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM game_teams_stats WHERE game_id LIKE %s", (str(game_id) + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def search_teams_stats():
    if request.method == 'POST':
        search_val = request.form.get('search')
        teams_stats = search_teams_by_game_id(search_val)
        player_info = get_player_info()
        return render_template("game_teams_stats.html", teams_stats=teams_stats, player_info=player_info)

    return render_template("game_teams_stats.html")