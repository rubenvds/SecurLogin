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
	VALUES ('2','ruben', 'a9d9c14ba32d047c3401e88d6b6d1bb2e85a240cdcf8765aace4272e8ea40bdc','613cd9e45f7bbec6fc0ea7ca8e838e7d2c439934ee6fc5544cae4f817336efaadaec1052cd4bbd6b22d62a432a16adf3b85f042d7a65b61bdd8508e9797caa94','605bcecefb74cb53bf98f650a7599cf01a27bab1787e75ad753d8499a7aa502861b5d9860d33565c40c29067a16e606dca3c6567058abb984f94f9e972f9ad5c', 0, 0)''')
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
