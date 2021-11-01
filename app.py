from flask import Flask, render_template, request
import threading
app = Flask(__name__)

class Message():
    def __init__(self, msgtype='', text=''):
        self.type = msgtype
        self.text = text


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # CHECK WITH DATABASE
        rfid = input()
        user = 'admin'
        if user == 'admin':
            return redirect('admindashboard')
        return redirect('userdashboard')
    msg = None
    return render_template('login.html', title='Login', msg=msg)

@app.route('/user')
def userdashboard():
    return render_template('user.html', title='Logged in' )

@app.route('/admin')
def admindashboard():
    return render_template('admin.html', title='Admin Dashboard')

if __name__ == "__main__":
    app.run(debug=True)