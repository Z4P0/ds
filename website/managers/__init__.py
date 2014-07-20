from flask import Blueprint

managers = Blueprint('managers', __name__)

from . import views
