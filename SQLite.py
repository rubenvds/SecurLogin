#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully");

conn.execute('''DROP TABLE IF EXISTS 'users' ''')
conn.execute('''CREATE TABLE 'users' (
  'user_id' INTEGER PRIMARY KEY,
  'role' VARCHAR(50) NULL,
  'user_name' VARCHAR(50) NULL,
  'salt' VARCHAR(255) NULL,
  'password' VARCHAR(255) NULL,
  'RFID' VARCHAR(15) NULL,
  'Failed_Login_Attempts' INT NULL,
  'locked' BOOL NULL
  )''')

conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
	VALUES ('2','ruben', 'somesalt','mypassword','CA 88 F6 80', 0, 0)''')
conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
  VALUES ('1','richard', 'somesalt','mypassword','CA 18 EC 75', 0, 0)''')
conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
  VALUES ('1','daniel', 'somesalt','mypassword','CA 88 F6 80', 0, 0)''')




cursor = conn.execute("SELECT * from `users`")
for row in cursor:
   print(row)
print("Table created successfully");
conn.commit()
conn.close()