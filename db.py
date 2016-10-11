import sqlite3
DB = 'var/music.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

def delete_table():
  c.execute('DROP TABLE genre;')

def create_table():
  c.execute('CREATE TABLE IF NOT EXISTS genre(ID INT, genre TEXT);')

def data_entry():
  c.execute('INSERT INTO genre (ID, genre)  VALUES("1","Techno");')
  conn.commit()

delete_table()
create_table()
data_entry()

for row in c.execute("SELECT rowid, * FROM genre"):
  print row


