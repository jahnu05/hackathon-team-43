import sqlite3

conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS Groups")
conn.commit()

conn.close()
