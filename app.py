from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import threading
import sqlite3

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

class Message():
    def __init__(self, msgtype='', text=''):
        self.type = msgtype
        self.text = text


@app.route("/", methods=['GET', 'POST'])
def login():
    msg = None
    if request.method == "POST":
        # CHECK WITH DATABASE
        rfid = 3930
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('test.db')

        getSQLData = conn.execute('''SELECT * FROM `users` WHERE user_name = '%s' ''' % username)
        array = getSQLData.fetchall()
        length = len(array)
        if length > 1:
            msg = Message("danger", "error: multiple users with this name")
        elif length == 0: 
            msg = Message("danger", "no user with this username")
        elif length == 1:
            for result in array:
                databasePassword = result[4]
                databaseSalt = result[3]
                databaserfid = result[5]
                role = result[1]
                locked = result[7]
                if locked == 1:
                    msg = Message("Danger", "This account is locked, please ask a system administration")
                else:
                    if databasePassword == password and rfid == databaserfid:
                        session['LoggedIn'] = 1
                        if role == '1':
                            session['LoggedIn'] = 1
                            return redirect('user')
                        elif role == '2':
                            session['LoggedIn'] = 2
                            return redirect('admin')
                    else:
                        msg = Message("Danger","invalid credentials")          
    return render_template('login.html', title='Login', msg=msg)

@app.route('/user')
def userdashboard():
    return render_template('user.html', title='Logged in' )

@app.route('/admin')
def admindashboard():
    role = session['LoggedIn']
    msg = None
    if(role == 2):
        return render_template('admin.html', title='Admin Dashboard', msg=msg)
    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session['LoggedIn'] = 0
    return redirect('/')


@app.route('/users')
def users():
    role = session['LoggedIn']
    if(role == 2):
        conn = sqlite3.connect('test.db')
        cursor = conn.execute('''SELECT * FROM `users`''')
        allusers = cursor.fetchall()
        return render_template('users.html', title='user Dashboard', users=allusers)
    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')

@app.route('/user_edit/<id>')
def user_edit(id):
    role = session['LoggedIn']
    if(role == 2):
        conn = sqlite3.connect('test.db')
        cursor = conn.execute('''SELECT * FROM `users` WHERE user_id = '%s' ''' % id)
        user = cursor.fetchone()
        return render_template('user_edit.html', title='user edit Dashboard', user = user)
    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)