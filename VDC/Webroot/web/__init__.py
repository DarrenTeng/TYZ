"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import *

SECRET_KEY = '\x13E8\x9aT\xf0\x89\x1c\x86\x11 \x93\xba\x08E\xb8\x91\xc2\xecP\xa8\x83M\xa7'



app = Flask(__name__)
app.debug= True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@10.108.186.88:3306/vdc_db'
app.secret_key = SECRET_KEY
db=SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

import web.views



from .user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .vm import vm as vm_blueprint
app.register_blueprint(vm_blueprint, url_prefix='/vm')