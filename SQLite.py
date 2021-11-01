#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully");

conn.execute('''CREATE TABLE Users
         (ID INT PRIMARY KEY     NOT NULL,
         USERNAME           TEXT    NOT NULL UNIQUE,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);''')
print("Table created successfully");

conn.close()