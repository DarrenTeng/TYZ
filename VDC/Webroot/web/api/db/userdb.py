from flask_login import UserMixin
from flask_sqlalchemy import *
from sqlalchemy import *

class User:
	
	def __init__(self, id, name, email, password, isAdmin):
		self.id = id
		self.name = name
		self.email = email
		self.password = password
		if (isAdmin):
			self.type = "admin"
		else:
			self.type = "user"

	def CheckPassword(password):
		return True


class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String)
	isAdmin = db.Column(db.boolen)

	@staticmethod
	def GetUserByName(username):
		dbRow = Users.query.filter_by(name=username).first()
		user = User(dbRow.id, dbRow.name, dbRow.email, dbRow.password, dbRow.isAdmin)
		return user
	
