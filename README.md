# SecurLogin
MOD1 Project @ TCS University of Twente

Needed Libraries:
- SQLite (Integrated in python3)
- Flask
- Flask-session

Setup instructions:

1. Edit the COM port on line 25 from app.py (look for the arduino: https://help.fleetmon.com/en/articles/2010900-how-do-i-get-my-com-port-number-windows)

2. Create virtualenv  
`python3 -m venv venv`  
`venv/scripts/activate`  

3. Install dependencies  
`pip3 install -r requirements.txt`  or `python3 -m pip install -r requirements.txt`

4. Run flask app  
`python3 app.py`  

5. Login with username `ruben` and password `mypassword` and as RFID the blue tag.

In some cases it gives an access denied error on the COM port, then please restart app.py (this happens when you click twice on a button).




https://github.com/rubenvds/SecurLogin
