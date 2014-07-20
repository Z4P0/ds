from flask import render_template
from . import teams

@teams.route('/')
def teams_index():
    return 'all teams in the CONCACAF'

@teams.route('/<team>')
def show_team(team):
    return 'all about %s' % team
