from web import app,db
from . import user
from ..modules import Users
import simplejson as json
from flask import render_template, redirect, request, url_for, session, escape

@user.route('/', methods=['GET', 'POST'])
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        
        user = Users.get_by_username(username)
        error = None
        if user is not None:
           if user.check_password(password):
                session['username']=username
                return json.dumps({'succeed':True, 'errorMsg':''})
           else:
               error = "The password is not valid, please try another one!"
        else:
            error = "The user name doesn't exist, please try another one!"
        
        return json.dumps({'succeed':False, 'errorMsg':error})
    else:
        if 'username' in session:
            return render_template('index.html')
        else:
            return render_template("signin.html")

@user.route('/signup', methods=['GET', 'POST'])
def sigup():
    if request.method == 'POST':
        new_username = request.json['username']
        new_email = request.json['email']
        new_password = request.json['password']

        error = None;
        if Users.get_by_username(new_username):
            error = "The user name already exists, please try another one!"
        else:
            if Users.validate_email(new_email) == 0:
                error = "The email address is not valid, please try another one!"
            else:
                if Users.get_by_useremail(new_email):
                    error = "The email address already exists, please try another one!"
       
        if error is not None:
            return json.dumps({'succeed':False, 'errorMsg':error})
        else:
            new_user = Users(name=new_username, email=new_email, passwordset=new_password)
            db.session.add(new_user)
            db.session.flush()
            db.session.commit()
            return json.dumps({'succeed':True, 'errorMsg':''})
    else:
        return render_template("signup.html")
@user.route('/signout')
def signout():
    session.pop('username', None)
    return redirect('../index')