# Imports
from flask import Flask, render_template, request, redirect
import threading
app = Flask(__name__)

class Message():
    def __init__(self, msgtype='', text=''):
        self.type = msgtype
        self.text = text


@app.route("/", methods=['GET', 'POST'])
def login():
    msg = None
    if request.method == "POST":
        # CHECK WITH DATABASE
        username = request.form.get('username')
        password = request.form.get('password')
        rfid = input()
        # Log in with right 
        return redirect('admin')
        return redirect('user')
        # If incorrect login ->
        msg = Message('danger', 'Username/password/RFID incorrect')
    
    return render_template('login.html', title='Login', msg=msg)

@app.route('/user')
def userdashboard():
    return render_template('user.html', title='Logged in' )

@app.route('/admin')
def admindashboard():
    msg = None
    return render_template('admin.html', title='Admin Dashboard', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)