from flask import Blueprint

vc = Blueprint('vc', __name__)

from . import views
