import sqlite3
DB = 'db/music.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

def delete_table():
  c.execute('DROP TABLE mixes;')

def create_table():
  c.execute('CREATE TABLE IF NOT EXISTS mixes(ID INTEGER PRIMARY KEY AUTOINCREMENT, artist VARCHAR(255), favourite INT, lenght VARCHAR(255),genre VARCHAR(255), rel_date VARCHAR(255), alb_img VARCHAR(255), mix_name VARCHAR(255), mp3_name VARCHAR(255), desc VARCHAR(255));')

def data_entry():
  c.execute('INSERT INTO mixes (artist, favourite, lenght, genre, rel_date, alb_img, mix_name, mp3_name, desc)  VALUES("Ace Ventura","1", "3:29", "psy", "2014.06.17", "ff.png", "Million Little Peaces", "million.mp3", "A sample of my remix for Million little pieces, bundled with a killer Outsiders remix on HOMmega productions.");')
  conn.commit()

#delete_table()
create_table()
data_entry()

for row in c.execute("SELECT rowid, * FROM mixes"):
  print row


