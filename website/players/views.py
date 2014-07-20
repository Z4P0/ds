from flask import render_template
from . import players

@players.route('/')
def players_index():
    return 'all players in the CONCACAF'

@players.route('/<player>')
def show_player(player):
    return 'all about %s' % player

