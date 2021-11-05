import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.execute("SELECT * from `users`")
for row in cursor:
   print(row)
conn.commit()
conn.close()