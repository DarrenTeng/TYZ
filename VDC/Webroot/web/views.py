"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import redirect, request, url_for, session, escape
from web import app

@app.route('/')
def index():
	return redirect('/static/index.html')
