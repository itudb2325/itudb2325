from flask import Flask, current_app, render_template, request, redirect, url_for, flash
import mysql.connector
import pandas as pd
from config import MYSQL_CONFIG  # Assuming you have a configuration file
from game_goalie_stats import delete_goalie_stats_by_id, delete_player_by_id, create_goalie_stats, update_goalie_stats, update_player, get_goalie_info, get_goalie_info_by_id
from game_teams_stats import delete_teams_stats_by_id, create_teams, update_teams
from game_skater_stats import update_game_skater , delete_skater_stats_by_id, create_skater
from game_plays import update_game, create_game, delete_game_plays_by_id
import os
import random



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

    image_folder = os.path.join(os.getcwd(), 'static/news')
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    num_images_in_carousel = min(3, len(image_files))
    carousel_images = random.sample(image_files, num_images_in_carousel)
    carousel_image_paths = [os.path.join('/static/news', img) for img in carousel_images]
    
    return {
        'icon': full_img_path1,
        'nhl_logo': full_img_path1,
        'youtube': full_img_path2,
        'x': full_img_path3,
        'instagram': full_img_path4,
        'facebook': full_img_path5,
        'carousel_images': carousel_image_paths
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
    game_plays_query = "SELECT play_id, game_id, team_id_for as team1, team_id_against as team2, date_time, event FROM game_plays ORDER BY date_time"
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

def create_game_plays():
    if request.method == 'GET':
        return render_template('create_game_plays.html')

    else:
        play_id = request.form.get('play_id')
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
        play_id =str(game_id) + '_' + play_id

        create_game(play_id, game_id, team_id_for, team_id_against, event, secondary_type,
                     x, y, period, period_type, period_time, period_time_remaining, date_time,
                     goals_away, goals_home, description, st_x, st_y)

        return redirect(url_for('game_plays'))

def delete_game_plays():
    if request.method == 'POST':
        play_id = request.form.get('play_id')
        delete_game_plays_by_id(play_id)

    return redirect(url_for('game_plays'))

def search_game_plays_by_game_id(game_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT play_id, game_id, team_id_for as team1, team_id_against as team2, date_time, event FROM game_plays WHERE game_id LIKE %s", (str(game_id) + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def search_game_plays():
    if request.method == 'POST':
        search_val = request.form.get('search')
        game_plays = search_game_plays_by_game_id(search_val)
        return render_template("game_plays.html", game_plays = game_plays)

    return render_template("game_plays.html")

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
    cursor.execute("SELECT * FROM game_skater_stats WHERE id = %s", (id,))
    results = cursor.fetchall()
    conn.close()
    return results


  


def game_skater_stats():

    skater_stats = get_skater_stats()
    return render_template("game_skater_stats.html", active_page= 'game_skater_stats' ,results=skater_stats)

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
        penaltyMinutes= request.form.get('penaltyMinutes')
        faceOffWins= request.form.get('faceOffWins')
        faceoffTaken= request.form.get('faceoffTaken')
        takeaways= request.form.get('takeaways')
        giveaways= request.form.get('giveaways')
        shortHandedGoals= request.form.get('shortHandedGoals')
        shortHandedAssists= request.form.get('shortHandedAssists')
        blocked= request.form.get('blocked')
        plusMinus= request.form.get('plusMinus')
        evenTimeOnIce= request.form.get('evenTimeOnIce')
        shortHandedTimeOnIce= request.form.get('shortHandedTimeOnIce')
        powerPlayTimeOnIce= request.form.get('powerPlayTimeOnIce')



        update_game_skater(id, game_id, player_id, team_id, timeOnIce, 
                            assists, goals, shots, hits, 
                            powerPlayGoals, powerPlayAssists,penaltyMinutes ,faceOffWins ,faceoffTaken ,takeaways ,giveaways ,shortHandedGoals , shortHandedAssists , blocked , plusMinus ,evenTimeOnIce , shortHandedTimeOnIce ,powerPlayTimeOnIce )

        return redirect(url_for('game_skater_stats'))

def delete_skater_stats():
    if request.method == 'POST':
        id = request.form.get('id')
        delete_skater_stats_by_id(id)

    return redirect(url_for('game_skater_stats'))



def search_skater_by_game_id(game_id):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT id, game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, powerPlayGoals, powerPlayAssists FROM game_skater_stats WHERE game_id LIKE %s", (str(game_id) + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def search_skater_stats():
    if request.method == 'POST':
        search_val = request.form.get('search')
        print("Search Value:", search_val)  # Add this line for debugging
        skater_stats = search_skater_by_game_id(search_val)
        
        return render_template("game_skater_stats.html", results=skater_stats)

    return render_template("game_skater_stats.html")

def create_skater_stats():
    if request.method == 'GET':
        return render_template('create_skater_stats.html')

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
        penaltyMinutes = request.form.get('penaltyMinutes')
        faceOffWins = request.form.get('faceOffWins')
        faceoffTaken = request.form.get('faceoffTaken')
        takeaways = request.form.get('takeaways')
        giveaways = request.form.get('giveaways')
        shortHandedGoals = request.form.get('shortHandedGoals')
        shortHandedAssists = request.form.get('shortHandedAssists')
        blocked = request.form.get('blocked')
        plusMinus = request.form.get('plusMinus')
        evenTimeOnIce = request.form.get('evenTimeOnIce')
        shortHandedTimeOnIce = request.form.get('shortHandedTimeOnIce')
        powerPlayTimeOnIce = request.form.get('powerPlayTimeOnIce')



        create_skater(game_id, player_id, team_id, timeOnIce, assists, goals, shots, hits, powerPlayGoals, powerPlayAssists, penaltyMinutes, faceOffWins, faceoffTaken, takeaways, giveaways, shortHandedGoals, shortHandedAssists, blocked, plusMinus, evenTimeOnIce, shortHandedTimeOnIce, powerPlayTimeOnIce)


        return redirect(url_for('game_skater_stats'))
    
#Game Goalie Stats Table
# Game Goalie Stats

def is_positive_integer(value):
    try:
        num = int(value)
        return num > 0
    except ValueError:
        return False

def is_positive_double(value):
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False

def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())

def is_single_char(value):
    return isinstance(value, str) and len(value) == 1

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
    player_info_results = cursor.fetchall()

    cursor.execute("SELECT DISTINCT player_id FROM game_goalie_stats")
    existing_player_ids = [row['player_id'] for row in cursor.fetchall()]

    results = [row for row in player_info_results if row['player_id'] in existing_player_ids]

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
    return render_template("game_goalie_stats.html", goalie_stats=goalie_stats, 
                           player_info=player_info, active_page = 'game_goalie_stats', 
                           get_goalie_info_by_id=get_goalie_info_by_id,
                           get_goalie_stats_by_id=get_goalie_stats_by_id,
                           get_player_info_by_id=get_player_info_by_id)

def delete_goalie_stats():
    if request.method == 'POST':
        id = request.form.get('id')
        delete_goalie_stats_by_id(id)
        flash("Successfully deleted Goalie!", category="success")

    return redirect(url_for('game_goalie_stats'))

def delete_player():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        delete_player_by_id(player_id)
        flash("Successfully deleted Player!", category="success")

    return redirect(url_for('game_goalie_stats'))

def update_goalie(id):
    if request.method == 'GET':
        goalie_stats = get_goalie_stats_by_id(id)
        return render_template('update_goalie.html', id=id, goalie_stats=goalie_stats)

    else:
        timeOnIce = request.form.get('timeOnIce')
        shots = request.form.get('shots')
        saves = request.form.get('saves')
        powerPlaySaves = request.form.get('powerPlaySaves')
        evenSaves = request.form.get('evenSaves')
        evenShotsAgainst = request.form.get('evenShotsAgainst')
        powerPlayShotsAgainst = request.form.get('powerPlayShotsAgainst')
        
        if not all([
            is_positive_integer(shots),
            is_positive_integer(timeOnIce),
            is_positive_integer(saves),
            is_positive_integer(powerPlaySaves),
            is_positive_integer(evenSaves),
            is_positive_integer(evenShotsAgainst),
            is_positive_integer(powerPlayShotsAgainst)
        ]):
            flash("Couldn't Update Goalie. Please make sure that the fields in Update Goalie are all positive numbers!", category="error")
        else:
            update_goalie_stats(id, timeOnIce, 
                            shots, saves, powerPlaySaves, evenSaves, 
                            evenShotsAgainst, powerPlayShotsAgainst)
            flash("Successfully Updated Goalie!", category="success")
            

        return redirect(url_for('game_goalie_stats'))
    
def update_player_info(player_id):
    if request.method == 'GET':
        player_info = get_player_info_by_id(player_id)
        return render_template('update_player_info.html', player_id=player_id, player_info=player_info, get_goalie_stats_by_id=get_goalie_stats_by_id)

    else:
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        nationality = request.form.get('nationality')
        birthCity = request.form.get('birthCity')
        primaryPosition = request.form.get('primaryPosition')
        height_cm = request.form.get('height_cm')
        shootsCatches = request.form.get('shootsCatches')
        
        if not all([
            is_non_empty_string(firstName),
            is_non_empty_string(lastName),
            is_non_empty_string(nationality),
            is_non_empty_string(birthCity),
            is_non_empty_string(primaryPosition),
            is_positive_double(height_cm),
            is_single_char(shootsCatches)
        ]):            
            flash("Couldn't Update Player. Please make sure you're providing the correct input types", category="error")
        else:
            update_player(player_id, firstName, lastName, nationality, birthCity, 
                        primaryPosition, height_cm, shootsCatches)
            flash("Successfully Updated Player!", category="success")
        
            

        return redirect(url_for('game_goalie_stats'))




def create_goalie():
    if request.method == 'GET':
        return render_template('create_goalie.html')

    else:
        selected_game_id = request.form.get('game_id')
        selected_player_id = request.form.get('player_id')
        selected_team_id = request.form.get('team_id')
        timeOnIce = request.form.get('timeOnIce')
        shots = request.form.get('shots')
        saves = request.form.get('saves')
        powerPlaySaves = request.form.get('powerPlaySaves')
        evenSaves = request.form.get('evenSaves')
        evenShotsAgainst = request.form.get('evenShotsAgainst')
        powerPlayShotsAgainst = request.form.get('powerPlayShotsAgainst')

        if not all([
            is_positive_integer(shots),
            is_positive_integer(timeOnIce),
            is_positive_integer(saves),
            is_positive_integer(powerPlaySaves),
            is_positive_integer(evenSaves),
            is_positive_integer(evenShotsAgainst),
            is_positive_integer(powerPlayShotsAgainst)
        ]):
            flash("Couldn't create Goalie. Please make sure that all fields in Create Goalie form are positive numbers!", category="error")
        else:
            create_goalie_stats(selected_game_id, selected_player_id, selected_team_id, timeOnIce, 
                            shots, saves, powerPlaySaves, evenSaves, 
                            evenShotsAgainst, powerPlayShotsAgainst)
            flash("Successfully Created Goalie!", category="success")
        
            
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
        return render_template("game_goalie_stats.html", goalie_stats=goalie_stats, 
                               player_info=player_info,
                               get_goalie_stats_by_id=get_goalie_stats_by_id,
                               get_goalie_info_by_id=get_goalie_info_by_id,
                               get_player_info_by_id=get_player_info_by_id)

    return redirect(url_for('game_goalie_stats'))

def search_by_player_name(player_name):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("""
        SELECT DISTINCT p.*
        FROM player_info p
        JOIN game_goalie_stats ggs ON p.player_id = ggs.player_id
        WHERE p.firstName LIKE %s
    """, ('%' + str(player_name) + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def search_player_stats():
    if request.method == 'POST':
        player_name = request.form.get('search')
        goalie_stats = get_goalie_stats()
        player_info = search_by_player_name(player_name)
        return render_template("game_goalie_stats.html", goalie_stats=goalie_stats, 
                               player_info=player_info,
                               get_goalie_stats_by_id=get_goalie_stats_by_id,
                               get_goalie_info_by_id=get_goalie_info_by_id,
                               get_player_info_by_id=get_player_info_by_id)

    return render_template("game_goalie_stats.html")

    

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
    return render_template("game_teams_stats.html", active_page="game_teams_stats", teams_stats=teams_stats)

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