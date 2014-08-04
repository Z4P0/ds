import os
from flask import Flask, render_template, g
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from config import config
import flask.ext.whooshalchemy as whooshalchemy


pagedown = PageDown()
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

    pagedown.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # routes and error pages
    @csrf.error_handler
    def csrf_error(reason):
        return render_template('csrf_error.html', reason=reason), 400



    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .articles import articles as articles_blueprint
    from .cups import cups as cups_blueprint
    from .leagues import leagues as leagues_blueprint
    from .teams import teams as teams_blueprint
    from .players import players as players_blueprint
    from .managers import managers as managers_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(articles_blueprint, url_prefix='/articles')
    app.register_blueprint(cups_blueprint, url_prefix='/cups')
    app.register_blueprint(leagues_blueprint, url_prefix='/leagues')
    app.register_blueprint(teams_blueprint, url_prefix='/teams')
    app.register_blueprint(players_blueprint, url_prefix='/players')
    app.register_blueprint(managers_blueprint, url_prefix='/managers')



    from .models import User, Article, Topic, Category, Tag, Cup, League, Team, Player, Manager, Association, Country

    whooshalchemy.whoosh_index(app, User)
    whooshalchemy.whoosh_index(app, Article)
    whooshalchemy.whoosh_index(app, Topic)
    whooshalchemy.whoosh_index(app, Category)
    whooshalchemy.whoosh_index(app, Tag)
    whooshalchemy.whoosh_index(app, Cup)
    whooshalchemy.whoosh_index(app, League)
    whooshalchemy.whoosh_index(app, Team)
    whooshalchemy.whoosh_index(app, Player)
    whooshalchemy.whoosh_index(app, Manager)
    whooshalchemy.whoosh_index(app, Association)
    whooshalchemy.whoosh_index(app, Country)



    from .main.forms import SearchForm
    @app.before_request
    def before_request():
        g.search_form = SearchForm()

    return app
