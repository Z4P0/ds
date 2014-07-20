import os
from flask import Flask, render_template
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask.ext.login import LoginManager
from config import config


moment = Moment()
csrf = CsrfProtect()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

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
    from articles import articles as articles_blueprint
    from cups import cups as cups_blueprint
    from leagues import leagues as leagues_blueprint
    from teams import teams as teams_blueprint
    from players import players as players_blueprint
    from managers import managers as managers_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(articles_blueprint, url_prefix='/articles')
    app.register_blueprint(cups_blueprint, url_prefix='/cups')
    app.register_blueprint(leagues_blueprint, url_prefix='/leagues')
    app.register_blueprint(teams_blueprint, url_prefix='/teams')
    app.register_blueprint(players_blueprint, url_prefix='/players')
    app.register_blueprint(managers_blueprint, url_prefix='/managers')

    return app
