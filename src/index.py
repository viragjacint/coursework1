from flask import * 
import sqlite3



app = Flask(__name__)
db_location = 'db/music.db'



@app.route('/')
def root():
  return render_template('catalogue.html'), 200

@app.route('/favourites')
def favourites():
	sql = ('SELECT * FROM mixes WHERE favourite = 1')
	connection = sqlite3.connect(db_location)
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql).fetchall()	
	return render_template('favourites.html', rows = rows)

@app.route('/removefav', methods=['GET'])	
def removefav():
	get_id = request.args.get('id')	
	sql = ('UPDATE mixes SET favourite = 0 WHERE id = ?')
	connection = sqlite3.connect(db_location)
	connection.row_factory = sqlite3.Row     		
	connection.cursor().execute(sql, get_id)
	connection.commit()
	return redirect(url_for('track', id=get_id))

@app.route('/addfav', methods=['GET'])	
def addfav():
	get_id = request.args.get('id')	
	sql = ('UPDATE mixes SET favourite = 1 WHERE id = ?')
	connection = sqlite3.connect(db_location)
	connection.row_factory = sqlite3.Row     		
	connection.cursor().execute(sql, get_id)
	connection.commit()
	return redirect(url_for('track', id=get_id))
	
@app.route('/track', methods=['GET'])
def track():
	get_id = request.args.get('id')
	sql = ('SELECT * FROM mixes WHERE id = ?')
	connection = sqlite3.connect(db_location)
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql, get_id).fetchall()	
	return render_template('track.html', rows = rows)

@app.route('/genre')
@app.route('/genre/<type>')
def genre(type):
	sql = ('SELECT * FROM mixes WHERE genre = ?')
	connection = sqlite3.connect(db_location)
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql, [type]).fetchall()
	return render_template('genre.html', rows = rows, type=type)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		
		username = request.form['username']
		password = request.form['password']
		return username, password

	else:
		return render_template('login.html')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)