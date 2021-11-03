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
	VALUES ('2','ruben', 'f90ef695a0cb3ad974dc1252fecf49c3d60b4e904822f86e008d48c8eeb86b24','524feab1a387e283b326e596afcbe2a88ea885f97ad989aea4d1dd20fb5ef15ec9d33f2cc2be839df360c706c75f1171e4d17bcf3aa8db364c4d31c9272bf104','CA 88 F6 80', 0, 0)''')
#conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
#  VALUES ('1','richard', 'somesalt','mypassword','CA 18 EC 75', 3, 1)''')
#conn.execute('''INSERT INTO 'users' ('role', 'user_name', 'salt', 'password', 'rfid', 'Failed_Login_Attempts', 'locked' )
#  VALUES ('1','daniel', 'somesalt','mypassword','CA 88 F6 80', 0, 0)''')



cursor = conn.execute("SELECT * from `users`")
for row in cursor:
   print(row)
print("Table created successfully");
conn.commit()
conn.close()