from flask import * 
import sqlite3
import ConfigParser
import os

app = Flask(__name__)


def init(app):
	config = ConfigParser.ConfigParser()
	try:
		config_location = "etc/config.cfg"
		config.read(config_location)
		
		app.config['DEBUG'] = config.get("config", "debug")
		app.config['ip_address'] = config.get("config", "ip_address")
		app.config['port'] = config.get("config", "port")
		app.config['url'] = config.get("config", "url")
		app.config['username'] = config.get("config", "username")
		app.config['password'] = config.get("config", "password")
		app.config['db_location'] = 'db/music.db'
		app.secret_key  = config.get("config", "secret_key")
	except:
		print "Could not read configs from: ", config_location



@app.route('/')
def root():	
	return render_template('catalogue.html'), 200

@app.route('/favourites')
def favourites():
	sql = ('SELECT * FROM mixes WHERE favourite = 1')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql).fetchall()	
	connection.close()
	return render_template('favourites.html', rows = rows)

@app.route('/removefav', methods=['GET'])	
def removefav():
	get_id = request.args.get('id')	
	sql = ('UPDATE mixes SET favourite = 0 WHERE id = ?')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	connection.cursor().execute(sql, get_id)
	connection.commit()
	connection.close()
	return redirect(url_for('track', id=get_id))

@app.route('/addfav', methods=['GET'])	
def addfav():
	get_id = request.args.get('id')	
	sql = ('UPDATE mixes SET favourite = 1 WHERE id = ?')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	connection.cursor().execute(sql, get_id)
	connection.commit()
	connection.close()
	return redirect(url_for('track', id=get_id))
	
@app.route('/track', methods=['GET'])
def track():
	get_id = request.args.get('id')
	sql = ('SELECT * FROM mixes WHERE id = ?')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql, get_id).fetchall()
	connection.close()	
	return render_template('track.html', rows = rows)

@app.route('/genre')
@app.route('/genre/<type>')
def genre(type):
	sql = ('SELECT * FROM mixes WHERE genre = ?')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql, [type]).fetchall()
	connection.close()
	return render_template('genre.html', rows = rows, type=type)

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['username']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['password']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You are logged in')
			return redirect(url_for('root'))
	return render_template('login.html', error=error)	

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('root'))
    
if __name__ == '__main__':
    init(app)
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']),
		threaded=True)