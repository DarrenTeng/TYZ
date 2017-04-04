from flask_login import UserMixin
from flask_sqlalchemy import *
from sqlalchemy import *
from werkzeug.security import check_password_hash, generate_password_hash
from web import db
from sqlalchemy.ext.declarative import declarative_base

# define a new class (call "Model" or whatever) with an as_dict() method defined
class Base(object):
    def as_dict(self):
        return dict((c.name,
                     getattr(self, c.name))
                     for c in self.__table__.columns)


#Base = declarative_base(cls=Base)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)

    @property
    def passwordset(self):
        raise AttributeError('password: write-only field')

    @passwordset.setter
    def passwordset(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_username(username):
        return Users.query.filter_by(name=username).first()

    @staticmethod
    def get_by_email(emailAddress):
        return Users.query.filter_by(email=emailAddress).first()

    @staticmethod
    def get_by_useremail(useremail):
        return Users.query.filter_by(email=useremail).first()

    @staticmethod
    def validate_email(email):
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return 1
        return 0

    def __repr__(self):
        return "<User '{}'>".format(self.username)

class VMList(db.Model,Base):
    __tablename__ = 'vmlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True) # The virtual machine name and guest system name
    status = db.Column(db.String(80)) # The virtual machine running status, such as Powered-On or Powered-off
    owner = db.Column(db.String(80)) # The owner of virtual machine
    uuid = db.Column(db.String(80)) # The uuid of virtual machine
    hostname = db.Column(db.String(80)) # The host name for virtual machine, such as 10.224.104.32
    ip = db.Column(db.String(80)) # The historical ip address for virtual machine
    account = db.Column(db.String(80)) # The user name in guest system
    dnsname = db.Column(db.String(80)) # The dns name for virtual machin
    description = db.Column(db.String(180))
    def __init__(self,name,status,owner,uuid,hostname,ip,account,dnsname,description):
        self.name = name
        self.status = status
        self.owner= owner
        self.uuid = uuid
        self.hostname = hostname
        self.ip= ip
        self.account= account
        self.dnsname= dnsname
        self.description= description
    @staticmethod
    def get_vm_all():
        return VMList.query.all()
    @staticmethod
    def get_by_owner(owner):
        return VMList.query.filter_by(owner=owner)
    @staticmethod
    def add_vm_item(vmitem):
        db.session.add(vmitem)
        db.session.commit()
        return True
    @staticmethod
    def delete_vm_byname(uuid):
        item = VMList.query.filter_by(uuid=uuid)
        item.delete();
        db.session.commit()
        return True
    @staticmethod
    def update_vm_byname(uuid,owner):
        item = VMList.query.filter_by(uuid=uuid)
        item[0].owner=owner
        db.session.commit()
        return True
    def __repr__(self):
        return '<VMList %r>' % (self.name)
    @staticmethod
    def get_by_name(vmname):
        return VMList.query.filter_by(name=vmname).first()
