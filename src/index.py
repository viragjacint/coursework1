from flask import *
from werkzeug import secure_filename
import sqlite3
import ConfigParser
import os
import logging
from logging.handlers import RotatingFileHandler

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
		
		app.config['log_file'] = config.get("logging", "name")
		app.config['log_location'] = config.get("logging", "location")
		app.config['log_level'] = config.get("logging", "level")		
	except:
		print "Could not read configs from: ", config_location


		
def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024* 1024 * 10 , backupCount=1024)
    file_handler.setLevel( app.config['log_level'] )
    formatter = logging.Formatter("%(levelname)s | %(asctime)s |  %(module)s | %(funcName)s | %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.setLevel( app.config['log_level'] )
    app.logger.addHandler(file_handler)
		
		
@app.route('/')
def root():
	this_route = url_for('.root')
	app.logger.info("Logging a test message from "+this_route)
	return render_template('home.html')
	
@app.route('/favourite')
def favourite():
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
		connection.close()
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
			
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
	if not session.get('admin'):
		abort(401)
	else:
		if request.method == 'POST':
			img = request.files['img']
			mp3 = request.files['mp3']			
			img.save('static/img/album/'+img.filename)
			mp3.save('static/mp3/'+mp3.filename)
			sql = ('INSERT INTO mixes (artist,favourite,length,genre,rel_date,alb_img,mix_name,mp3_name,desc) VALUES (?,?,?,?,?,?,?,?,?)')		
			connection = sqlite3.connect(app.config['db_location'])
			connection.row_factory = sqlite3.Row     		
			connection.cursor().execute(sql, (request.form['artist'],request.form['favourite'],request.form['length'],request.form['genre'],request.form['rel_date'],img.filename,request.form['mix_name'],mp3.filename,request.form['description']))
			connection.commit()		
			connection.close()			
			return redirect(url_for('admin'))
		
			
if __name__ == '__main__':
	init(app)
	logs(app)
	app.run(
		host=app.config['ip_address'], 
		port=int(app.config['port']),
		threaded=True)