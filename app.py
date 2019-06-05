from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

#get the folder that this file runs in
basedir = os.path.abspath(os.path.dirname(__file__))

#configuration
DATABASE = 'flaskr.db'
DEBUG = 'True'
SECRET_KEY = 'tasty'
USERNAME = 'admin'
PASSWORD = 'admin'

#define full path for database
DATABASE_PATH = os.path.join(basedir, DATABASE)

#database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

#create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models

#close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    #search database for entries and display them
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)

@app.route('/add', methods = ['POST'])
def add_entry():
    #adding a new post to the DATABASE
    if not session.get('logged_in'):
        about(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('index'))

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

@app.route('/delete/<post_id>', methods=['GET'])
def delete_entry(post_id):
    #this is to delete a post from the DATABASE
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status':1, 'message': 'Post Deleted'}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)

@app.route('/search/', methods = ['GET'])
def search():
    query = request.args.get('query')
    entries = db.session.query(models.Flaskr)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
