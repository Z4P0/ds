from flask import render_template
from . import leagues


@leagues.route('/')
def leagues_index():
    return 'all leagues in the CONCACAF'

@leagues.route('/<league>')
def show_league(league):
    return 'all about %s' % league
