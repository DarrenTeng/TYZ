from flask import Blueprint

vm = Blueprint('vm', __name__)

from . import views
