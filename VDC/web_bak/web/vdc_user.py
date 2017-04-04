from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import MySQLdb

app = Flask(__name__)

#######################
#   DATABASE CONFIG   #
#######################

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="vdc_db")
cur = db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('signin'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM users WHERE name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            row = cur.fetchone();
            if md5(password_form).hexdigest() == row[0]:
                session['username'] = request.form['username']
                return redirect(url_for('signup'))
            else:
                error = "Password is invalid!"
        else:
            error = "User name is not exist!"
    return render_template('SIGN_IN.html', error=error)


@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username_form  = request.form['VDC_createaccount_name']
        email_form = request.form['VDC_createaccount_email']
        password_form  = request.form['VDC_createaccount_newpassword']
        cur.execute("SELECT * FROM users;") # CHECKS IF USERNAME EXSIST
        row = cur.fetchone();
        for row in cur.fetchall():
            if username_form == row[1]:
                error = "User name already exist,please try another one!"
                return render_template('SIGN_UP.html', error=error)
            if email_form == row[2]:
                error = "Email already exist,please try another one!"
                return render_template('SIGN_UP.html', error=error)
        try:
            cur.execute("INSERT INTO users (name,email,password) values (%s,%s,%s);", [username_form,email_form,md5(password_form).hexdigest()]) # CHECKS IF USERNAME EXSIST
            db.commit()
        except MySQLdb.Error, e:
            error = "Error %d:%s" % (e.args[0], e.args[1])  
            return render_template('SIGN_UP.html', error=error)
        finally:
            note = "Signup success, please use your user name and password to signin.";
            return redirect(url_for('signin'))
    return render_template('SIGN_UP.html', error=error)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run()