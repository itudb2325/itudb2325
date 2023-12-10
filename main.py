from flask import Flask

import views
from views import index_page, configure_app


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    configure_app(app)
    app.add_url_rule("/", view_func=views.index_page, methods=['GET'])
    app.add_url_rule("/game_plays", view_func=views.game_plays)
    app.add_url_rule("/game_goalie_stats", view_func=views.game_goalie_stats)
    app.add_url_rule("/game_skater_stats", view_func=views.game_skater_stats)
    app.add_url_rule("/game_teams_stats", view_func=views.game_teams_stats)

    
    app.add_url_rule("/update_goalie/<int:id>", view_func=views.update_goalie, methods=['POST', 'GET'])
    app.add_url_rule("/update_player_info/<int:player_id>", view_func=views.update_player_info, methods=['POST', 'GET'])
    app.add_url_rule("/delete_goalie_stats", view_func=views.delete_goalie_stats, methods=['POST'])
    app.add_url_rule("/delete_player", view_func=views.delete_player, methods=['POST'])
    app.add_url_rule("/search_goalie_stats", view_func=views.search_goalie_stats, methods=['POST', 'GET'])
    app.add_url_rule("/create_goalie", view_func=views.create_goalie, methods=['POST', 'GET'])

    app.add_url_rule("/update_teams_stats/<int:id>", view_func=views.update_teams_stats, methods=['POST', 'GET'])
    app.add_url_rule("/delete_teams_stats", view_func=views.delete_teams_stats, methods=['POST'])
    app.add_url_rule("/create_teams_stats", view_func=views.create_teams_stats, methods=['POST', 'GET'])



    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 3306)
    app.run(host="0.0.0.0", port=port)