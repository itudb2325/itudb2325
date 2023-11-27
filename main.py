from flask import Flask

import views


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.index_page)
    app.add_url_rule("/game_plays", view_func=views.game_plays)
    app.add_url_rule("/game_goalie_stats", view_func=views.game_goalie_stats)
    app.add_url_rule("/game_skater_stats", view_func=views.game_skater_stats)
    app.add_url_rule("/game_teams_stats", view_func=views.game_teams_stats)


    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 3306)
    app.run(host="0.0.0.0", port=port)