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
	sql = ('SELECT * FROM mixes WHERE favourite = 1')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql).fetchall()	
	connection.close()
	return render_template('favourites.html', rows = rows)
	

@app.route('/catalogue')
def catalogue():
	return render_template('catalogue.html'), 200

@app.route('/show_all')	
def show_all():
	sql = ('SELECT * FROM mixes')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql).fetchall()	
	connection.close()
	return render_template('showall.html', rows = rows)
	
	
@app.route('/search', methods=['GET', 'POST'])
def search():	
	if request.method == 'POST':
		search = request.form['search']
		sql = 'SELECT * FROM mixes WHERE artist LIKE "%'+search+'%" OR mix_name LIKE "%'+search+'%"'
		connection = sqlite3.connect(app.config['db_location'])
		connection.row_factory = sqlite3.Row     		
		rows = connection.cursor().execute(sql).fetchall()
		return render_template('search.html', rows = rows)
	else:
		search = 0
		return render_template('search.html', search = search), 200

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
@app.route('/track/<id>', methods=['GET'])
def track(id):	
	sql = ('SELECT * FROM mixes WHERE id = ?')
	connection = sqlite3.connect(app.config['db_location'])
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql, id).fetchall()
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
			session['admin'] = True			
			return redirect(url_for('admin'))
	return render_template('login.html', error=error)	

@app.route('/logout')
def logout():
    session.pop('admin', None)    
    return redirect(url_for('root'))

@app.route('/admin')
def admin():
	if not session.get('admin'):
		abort(401)
	else:
		sql = ('SELECT * FROM mixes')
		connection = sqlite3.connect(app.config['db_location'])
		connection.row_factory = sqlite3.Row     		
		rows = connection.cursor().execute(sql).fetchall()
		connection.close()
		return render_template('admin.html', rows = rows)

@app.route('/admin_edit')
def admin_edit():
	if not session.get('admin'):
		abort(401)
	else:
		get_id = request.args.get('id')
		sql = ('SELECT * FROM mixes WHERE id = ?')
		connection = sqlite3.connect(app.config['db_location'])
		connection.row_factory = sqlite3.Row     		
		rows = connection.cursor().execute(sql, get_id).fetchall()
		connection.close()
		return render_template('admin_edit.html', rows = rows)
	
@app.route('/update', methods=['GET', 'POST'])
def update():
	if request.method == 'POST':	
		sql = ('UPDATE mixes SET artist = ?, mix_name = ?, length = ?, genre = ?, rel_date = ?, desc = ? WHERE id = ?')		
		connection = sqlite3.connect(app.config['db_location'])
		connection.row_factory = sqlite3.Row     		
		connection.cursor().execute(sql, (request.form['artist'],request.form['mix_name'],request.form['length'],request.form['genre'],request.form['rel_date'],request.form['description'],request.form['id']))
		connection.commit()		
		connection.close()	
		return redirect(url_for('admin'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if not session.get('admin'):
		abort(401)
	else:
		get_id = request.args.get('id')	
		sql = ('DELETE FROM mixes WHERE id = ?')		
		connection = sqlite3.connect(app.config['db_location'])
		connection.row_factory = sqlite3.Row     		
		connection.cursor().execute(sql, get_id)
		connection.commit()	
		connection.close()	
		return redirect(url_for('admin'))
	
@app.route('/admin_add')
def admin_add():
	if not session.get('admin'):
		abort(401)
	else:
		return render_template('admin_add.html')
			
		
if __name__ == '__main__':
    init(app)
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']),
		threaded=True)