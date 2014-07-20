from flask import render_template
from . import cups

# cups
@cups.route('/')
def cups_index():
    return 'all cups in the CONCACAF'

@cups.route('/<cup>')
def show_cup(cup):
    return 'all about the %s' % cup
