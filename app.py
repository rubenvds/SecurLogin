from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import threading
import sqlite3
import serial
import random
import hashlib, binascii, os

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
haskey = "ABdOICG11mddufEP"
class Message():
    def __init__(self, msgtype='', text=''):
        self.type = msgtype
        self.text = text


def Read_Card():
    key=170
    cyphertext = []
    bin =[]
    plain_bin=[]
    UID= ""
    print("Wait for the card ")
    ser = serial.Serial("COM3", 9600)
    k = 0  # check which port was really used
    while k < 8:
        x = ser.readline()
        string_ = x.decode()
        if string_[0].isdigit()==True:
            cyphertext.append(string_.split("\r\n")[0])
            k = k + 1
    ser.close()
    print(cyphertext)
    for i in cyphertext :
        x = int (i) #the incripted cyphertext
        y=x^key
        UID=UID+chr(y)
    print(UID)
    return UID



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
        rfid = Read_Card()
        #rfid = "ca88f680"

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
                databaseLoginAttempts = result[6]
                role = result[1]
                locked = result[7]
                if locked == 1:
                    msg = Message("danger", "This account is locked, please ask a system administration")
                else:
                    password = password + haskey
                    passwordhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), databaseSalt.encode('ascii'), 100000)
                    passwordhash = binascii.hexlify(passwordhash).decode('ascii')
                    checkpassword =  passwordhash == databasePassword
                    
                    rfid = rfid + haskey
                    rfidhash = hashlib.pbkdf2_hmac('sha512', rfid.encode('utf-8'), databaseSalt.encode('ascii'), 100000)
                    rfidhash = binascii.hexlify(rfidhash).decode('ascii')
                    
                    checkrfid = rfidhash == databaserfid
                    if checkpassword and checkrfid:
                        conn.execute(''' UPDATE `users` SET Failed_Login_Attempts = 0 WHERE user_name = '%s'  ''' % username)
                        conn.commit()
                        if role == '1':
                            session['LoggedIn'] = 1
                            return redirect('user')
                        elif role == '2':
                            session['LoggedIn'] = 2
                            return redirect('admin')
                    else:
                        if checkpassword == False or checkrfid == False:
                            if databaseLoginAttempts >= 2:
                                conn.execute(''' UPDATE `users` SET Failed_Login_Attempts = Failed_Login_Attempts + 1, locked = 1 WHERE user_name = '%s'  ''' % username)
                                conn.commit()
                                print("blocked account")
                            else:
                                print("increment")
                                conn.execute(''' UPDATE `users` SET Failed_Login_Attempts = Failed_Login_Attempts + 1 WHERE user_name = '%s'  ''' % username)
                                conn.commit()
                        msg = Message("danger","invalid credentials")         
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
            msg = Message("success", "updated the user profile")
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
        cursor = conn.execute('''SELECT * FROM `users` WHERE user_id = '%s' ''' % id)
        user = cursor.fetchone()
        msg = Message("success", "unlocked the user")
        return render_template('user_edit.html', title='user edit Dashboard', user = user, msg=msg)

    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')

@app.route('/connect/<id>')
def connect(id):
    role = session.get('LoggedIn',0)
    if(role == 2):
        conn = sqlite3.connect('test.db')
        rfid = Read_Card()
        #rfid = "CA 18 EC 75"
        
        rfid = rfid + haskey
        rfidhash = hashlib.pbkdf2_hmac('sha512', rfid.encode('utf-8'), databaseSalt.encode('ascii'), 100000)
        rfidhash = binascii.hexlify(rfidhash).decode('ascii')

        
        conn.execute(''' UPDATE `users` SET RFID='%s' WHERE user_id='%s';''' % (rfidhash,id))
        conn.commit()
        cursor = conn.execute('''SELECT * FROM `users` WHERE user_id = '%s' ''' % id)
        user = cursor.fetchone()
        msg = Message("success", "connected the card to the user")
        return render_template('user_edit.html', title='user edit Dashboard', user = user, msg=msg)

    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    role = session.get('LoggedIn',0)
    if(role == 2):
        if request.method == "POST":
            username = request.form.get('username')
            conn = sqlite3.connect('test.db')
            cursor = conn.execute('''SELECT user_name FROM `users` WHERE user_name = '%s' ''' % username)
            conn.commit()
            array = cursor.fetchall()
            length = len(array)
            if length > 0:
                msg = Message("danger","This username already exist")
                return render_template('add_user.html', title='user edit Dashboard', msg=msg)


            password = request.form.get('password')
            role = request.form.get('role')

            rfid = Read_Card()
            #rfid = "CA 88 F6 80"
            
            rfid = rfid + haskey
            rfidhash = hashlib.pbkdf2_hmac('sha512', rfid.encode('utf-8'), databaseSalt.encode('ascii'), 100000)
            rfidhash = binascii.hexlify(rfidhash).decode('ascii')
                    
                    
            conn = sqlite3.connect('test.db')

            #generate salt
            password = password + haskey
            salt = salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            hashedpassword = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
            hashedpassword = binascii.hexlify(hashedpassword)
            salt = salt.decode('ascii')
            hashedpassword = hashedpassword.decode('ascii')
            print('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
                            VALUES (%s,'%s', '%s','%s','%s', 0, 0)''' % (role, username, salt, hashedpassword, rfidhash))
            
            conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
                            VALUES (%s,'%s', '%s','%s','%s', 0, 0)''' % (role, username, salt, hashedpassword, rfidhash))
            conn.commit()
            msg = Message("success", "Sucessfully added user with username %s" % username)
            return render_template('add_user.html', title='user edit Dashboard', msg=msg)

        conn = sqlite3.connect('test.db')
        rfid = Read_Card()
        
        rfid = rfid + haskey
        rfidhash = hashlib.pbkdf2_hmac('sha512', rfid.encode('utf-8'), databaseSalt.encode('ascii'), 100000)
        rfidhash = binascii.hexlify(rfidhash).decode('ascii')
                
                
        conn.execute(''' UPDATE `users` SET RFID='%s' WHERE user_id='%s';''' % (rfidhash,id))
        conn.commit()
        cursor = conn.execute('''SELECT * FROM `users` WHERE user_id = '%s' ''' % id)
        user = cursor.fetchone()
        msg = None
        return render_template('add_user.html', title='user edit Dashboard', user = user, msg=msg)

    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')



@app.route('/delete_user/<id>')
def delete_user(id):
    role = session.get('LoggedIn',0)
    if(role == 2):
        conn = sqlite3.connect('test.db')
        conn.execute(''' DELETE FROM `users` WHERE user_id='%s';''' % (id))
        conn.commit()
        msg = Message("success", "Deleted user")
        cursor = conn.execute('''SELECT * FROM `users`''')
        allusers = cursor.fetchall()
        return render_template('users.html', title='users Dashboard', users = allusers, msg=msg)

    elif(role == 1):
        return redirect('user')
    else:
        return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)



