from flask import * 
import sqlite3



app = Flask(__name__)
db_location = 'db/music.db'



@app.route('/')
def root():
  return render_template('catalogue.html'), 200

@app.route('/favourites')
def favourites():
  return render_template('favourites.html'), 200
  
@app.route('/track')
def track():
  return render_template('track.html'), 200

@app.route('/genre')
@app.route('/genre/<type>')
def genre(type):
	sql = ('SELECT * FROM mixes WHERE genre = ?')
	connection = sqlite3.connect(db_location)
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql, [type]).fetchall()
	return render_template('genre.html', rows = rows, type=type)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)