import os
from flask import Flask, render_template
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from config import config


moment = Moment()
csrf = CsrfProtect()
db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    # routes and error pages
    @csrf.error_handler
    def csrf_error(reason):
        return render_template('csrf_error.html', reason=reason), 400


    # users
    @app.route('/u/<user>')
    def view_profile(user):
        return render_template('ds/03-profile.html',
            title = user,
            description = 'Profile for user',
            data_page = 'profile',
            username = user
            )






    # articles
    @app.route('/articles/')
    def articles_index():
        return 'all articles'

    @app.route('/articles/<slug>')
    def read_article(slug):
        return 'article: %s' % slug




    # cups
    @app.route('/cups/')
    def cups_index():
        return 'all cups in the CONCACAF'

    @app.route('/cups/<cup>')
    def show_cup(cup):
        return 'all about the %s' % cup




    # leagues
    @app.route('/leagues/')
    @app.route('/ligas/')
    def leagues_index():
        return 'all leagues in the CONCACAF'

    @app.route('/leagues/<league>')
    @app.route('/ligas/<league>')
    def show_league(league):
        return 'all about %s' % league




    # teams
    @app.route('/teams/')
    def teams_index():
        return 'all teams in the CONCACAF'

    @app.route('/teams/<team>')
    def show_team(team):
        return 'all about %s' % team




    # players
    @app.route('/players/')
    def players_index():
        return 'all players in the CONCACAF'

    @app.route('/players/<player>')
    def show_player(player):
        return 'all about %s' % player




    # managers
    @app.route('/managers/')
    def managers_index():
        return 'all managers in the CONCACAF'

    @app.route('/managers/<manager>')
    def show_manager(manager):
        return 'all about %s' % manager




    # settings
    @app.route('/settings/')
    def change_settings():
        return 'cahnge site settings for user'




    # search
    @app.route('/search/')
    def search_ds():
        return 'Search'




    from main import main as main_blueprint
    from auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
