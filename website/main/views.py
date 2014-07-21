from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Role, Cup, League, Team
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('ds/index.html',
        title = 'DS',
        description = 'Your source for the CONCACAF',
        page_id = 'homepage',
        data_page = 'homepage'
        )


# about
@main.route('/about')
def about_ds():
    return 'Started in edgars room 4 years ago now'


# privacy
@main.route('/privacy-policy')
def privacy_policy():
    return 'DS privacy policy'



@main.route('/u/<username>')
def view_profile():
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('ds/profile.html', user=user)
