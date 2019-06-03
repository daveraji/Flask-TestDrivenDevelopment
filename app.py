import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

#configuration
DATABASE = 'flaskr.db'
DEBUG = 'True'
SECRET_KEY = 'tasty'
USERNAME = 'admin'
PASSWORD = 'admin'

#create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)

#connect to the DATABASE
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#open the database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    db=get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/login', methods=['GET', 'POST']) #get is accessing the webpage and post sends info to the server
def login(): #the get is default (seeing the webpage), post is when the user sends info from logging in
    error=None
    if request.method =='POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    #user logout/authentication/session management
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/add', methods = ['POST'])
def add_entry():
    #adding a new post to the DATABASE
    if not session.get('logged_in'):
        about(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run()
