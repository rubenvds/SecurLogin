from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import threading
import sqlite3
import serial


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

class Message():
    def __init__(self, msgtype='', text=''):
        self.type = msgtype
        self.text = text


def Read_Card():
    print("Wait for the card ")
    ser = serial.Serial("COM3", 9600)
    k = 0;  # check which port was really used
    while k == 0:
        x = ser.readline()
        str = x.decode()
        if str.find("UID") != -1:
            k = 1 
    ser.close()

    return str[10:]



@app.route("/", methods=['GET', 'POST'])
def login():
    msg = None
    role = session.get('LoggedIn',0)
    if(role == 2):
        return redirect('admin')
    elif(role == 1):
        return redirect('user')

    if request.method == "POST":
        # CHECK WITH DATABASE
        username = request.form.get('username')
        password = request.form.get('password')
        #rfid = Read_Card()
        rfid = "CA 88 F6 80"
        print(rfid)

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
                    print(databaserfid.strip())
                    print(rfid.strip())
                    print(rfid.strip() == databaserfid.strip())
                    if databasePassword == password and rfid.strip() == databaserfid.strip():
                        if role == '1':
                            session['LoggedIn'] = 1
                            return redirect('user')
                        elif role == '2':
                            session['LoggedIn'] = 2
                            return redirect('admin')
                    else:
                        msg = Message("Danger","invalid credentials")   
    #rfid = Read_Card().apply_async();       
    return render_template('login.html', title='Login', msg=msg)

@app.route('/user')
def userdashboard():
    msg = None
    return render_template('user.html', title='Logged in', msg=msg)

@app.route('/admin')
def admindashboard():
    msg = None
    role = session.get('LoggedIn',0)
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
    msg = None
    role = session.get('LoggedIn',0)
    if(role == 2):
        conn = sqlite3.connect('test.db')
        cursor = conn.execute('''SELECT * FROM `users`''')
        allusers = cursor.fetchall()
        return render_template('users.html', title='user Dashboard', users=allusers, msg=msg)
    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')

@app.route('/user_edit/<id>', methods=['GET', 'POST'])
def user_edit(id):
    role = session.get('LoggedIn',0)
    if(role == 2):
        conn = sqlite3.connect('test.db')
        conn = sqlite3.connect('test.db')
        cursor = conn.execute('''SELECT * FROM `users` WHERE user_id = '%s' ''' % id)
        user = cursor.fetchone()
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')
            rfid = request.form.get('rfid')
            if password == '':
                cursor = conn.execute('''UPDATE `users` SET role = '%s',user_name='%s', RFID='%s' WHERE user_id = '%s' ''' % (role, username, rfid, id))
            else:
                cursor = conn.execute('''UPDATE `users` SET role = '%s',user_name='%s',password='%s', RFID='%s' WHERE user_id = '%s' ''' % (role, username, password, rfid, id))
            conn.commit()
            msg = Message("Success", "updated the user profile")
            return render_template('user_edit.html', title='user edit Dashboard', user = user, msg=msg)
        msg = None
        return render_template('user_edit.html', title='user edit Dashboard', user = user, msg=msg)
    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')

@app.route('/unlock/<id>')
def unlock(id):
    role = session.get('LoggedIn',0)
    if(role == 2):
        conn = sqlite3.connect('test.db')
        conn.execute(''' UPDATE `users` SET locked=0, Failed_Login_Attempts=0 WHERE user_id='%s';''' % id)
        conn.commit()
        msg = Message("Success", "unlocked the user")
        return render_template('user_edit.html', title='user edit Dashboard', user = user, msg=msg)

    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)



