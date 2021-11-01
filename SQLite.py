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
  'RFID' INT NULL,
  'Failed_Login_Attempts' INT NULL,
  'locked' BOOL NULL
  )''')

conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
	VALUES ('2','rubenvds', 'somesalt','mypassword',003930, 0, 0)''')

cursor = conn.execute("SELECT * from `users`")
for row in cursor:
   print(row)
print("Table created successfully");
conn.commit()
conn.close()