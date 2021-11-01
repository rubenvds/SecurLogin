#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully");

conn.execute('''CREATE TABLE IF NOT EXISTS 'users' (
  'user_id' SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  'role' VARCHAR(50) NULL,
  'user_name' VARCHAR(50) NULL,
  'salt' VARCHAR(255) NULL,
  'password' VARCHAR(255) NULL,
  'RFID' INT NULL,
  'Failed_Login_Attempts' INT NULL,
  'locked' BOOL NULL,
  PRIMARY KEY ('user_id'))''')


print("Table created successfully");

conn.close()