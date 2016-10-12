import ConfigParser
import sqlite3
import logging
import os

from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, session, g, redirect, url_for

app = Flask(__name__)

def init(app):
    config = ConfigParser.ConfigParser()
    config_location = "etc/config.cfg"
    try:
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
        app.secret_key  = config.get("config", "secret_key")
        app.config['username'] = config.get("config", "username")
        app.config['password'] = config.get("config", "password")
        app.config['database'] = config.get("config", "database")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")
    except:
        print ("Could not read config from: "), config_location

def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024*1024*10, backupCount=1024)
    file_handler.setLevel(app.config['log_level'])
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s |\
  %(funcName)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['log_level'])
    app.logger.addHandler(file_handler)

def connect_db():
    init(app)
    conn = sqlite3.connect(app.config['database'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root():
  return render_template('catalogue.html'), 200

@app.route('/favourites')
def favourites():
  return render_template('favourites.html'), 200

@app.route('/genre')
def genre():
  return render_template('genre.html'), 200    

if __name__ == "__main__":
  init(app)
  logs(app)
  app.run(
        host = app.config['ip_address'],
        port = int(app.config['port'])
    )

