from flask import Blueprint

cups = Blueprint('cups', __name__)

from . import views
