from flask import render_template
from . import managers

@managers.route('/')
def managers_index():
    return 'all managers in the CONCACAF'

@managers.route('/<manager>')
def show_manager(manager):
    return 'all about %s' % manager
