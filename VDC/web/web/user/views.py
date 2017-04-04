from web import app,db
from . import user
from ..modules import Users
import simplejson as json
from flask import render_template, redirect, request, url_for, session, escape
from web.tool.jsonHelper import RecursiveDumpObject,RecursiveEncoder,responseDataFormat
import time
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def GenPassword(length):
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])

def SendEmail(username, newpassword):
    sender = 'support@VDC.com'
    receivers = [user.email]

    message = MIMEText('User name:' + username + '/nNew password:' + newpassword, 'plain', 'utf-8')
    message['From'] = Header("Vitural Design Center", 'utf-8')
    message['To'] =  Header(username, 'utf-8')
    message['Subject'] = Header('Reset Password', 'utf-8')
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException:
        return False

@user.route('/', methods=['GET', 'POST'])
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        startTime = time.time()      
        error = ""
        data = ""

        username = request.json['username']
        password = request.json['password']
        
        user = Users.get_by_username(username)
        
        if user is not None:
           if user.check_password(password):
                session['username']=username
                
                result = True
                endTime = time.time()
                duration = endTime - startTime
                response = responseDataFormat(result,data,error,duration)
                return RecursiveDumpObject(response);
           else:
               error = "The password is not valid, please try another one!"
        else:
            error = "The user name doesn't exist, please try another one!"
        
        result = False 
        endTime = time.time()
        duration = endTime - startTime
        response = responseDataFormat(result,data,error,duration)
        return RecursiveDumpObject(response);

    else:
        if 'username' in session:
            return redirect('../static/Home.html')
        else:
            return render_template("signin.html")

@user.route('/signup', methods=['GET', 'POST'])
def sigup():
    if request.method == 'POST':
        startTime = time.time()      
        error = ""
        data = ""

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
            result = False
            endTime = time.time()
            duration = endTime - startTime
            response = responseDataFormat(result,data,error,duration)
            return RecursiveDumpObject(response);

        else:
            new_user = Users(name=new_username, email=new_email, passwordset=new_password)
            db.session.add(new_user)
            db.session.flush()
            db.session.commit()

            result = True
            endTime = time.time()
            duration = endTime - startTime
            response = responseDataFormat(result,data,error,duration)
            return RecursiveDumpObject(response);
 
    else:
        return render_template("signup.html")
@user.route('/signout')
def signout():
    session.pop('username', None)
    return redirect('../index')

@user.route('/changepassword', methods=['GET', 'POST'])
def changePW():
    if request.method == 'POST':
        startTime = time.time()      
        error = ""
        data = ""
        result = False

        if 'username' in session:
            oldPassword = request.json['oldpassword']
            newPassword = request.json['newpassword']
            curUserName = session['username']

            user = Users.get_by_username(curUserName)
        
            if user is not None:
                if user.check_password(oldPassword):
                    user.passwordset = newPassword
                    db.session.commit()
                    result = True
                else:
                    error = "The password is not valid, please try another one!"
            else:
                error = "The current user doesn't exist!"
        else:
            error = "There is no valid login user currentlly!"
                    
        endTime = time.time()
        duration = endTime - startTime
        response = responseDataFormat(result,data,error,duration)
        return RecursiveDumpObject(response);

@user.route('/forgetpassword', methods=['GET', 'POST'])
def forgetPW():
    if request.method == 'POST':
        startTime = time.time()      
        error = ""
        data = ""
        result = False

        emailAddress = request.json['email']
        user = Users.get_by_email(emailAddress)

        if user is not None:
            newPassword = GenPassword(10)
            user.passwordset = newPassword
            db.session.commit()
            data = newPassword
            result = True
            #if SendEmail(user.name, newPassword):
            #    result = True
            #else:
            #    error = "It is failed to send email!"
        else:
            error = "The email is not registered!"
                    
        endTime = time.time()
        duration = endTime - startTime
        response = responseDataFormat(result,data,error,duration)
        return RecursiveDumpObject(response);
    else:
        return render_template("forgetpassword.html")
