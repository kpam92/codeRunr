"""
    codeRnr
    ~~~~~~~~
    A microblogging application written with Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import time
import pdb
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
import sys
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


# configuration
DATABASE = '/tmp/codernr.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('CODERNR_SETTINGS', silent=True)


def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    print(db)
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))
    code_menu = query_db('''
    select title, id from snippets where snippets.user_id = ?
    ''', [session['user_id']])
    return render_template('index.html', menu_items=code_menu)

@app.route('/getCode', methods=['GET'])
def get_code():
    url = request.url
    codeId = int(str(url.split("=")[1]))
    code = query_db('select * from snippets where snippets.id = ?', [codeId], one=True)
    return str(code['title'] + '/~=^md' + code['code'])

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where id = ?', [session['user_id']], one=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'], request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

def get_user_id(username):
    rv = query_db('select id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = get_db()
            db.execute('''insert into user (
              username, email, pw_hash) values (?, ?, ?)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password'])])
            db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/addCode', methods=['POST'])
def add_code():
    if 'user_id' not in session:
        abort(401)
    db = get_db()
    title = str('testing if code can be saved')
    db.execute('''insert into snippets (title, code, pub_date, user_id)
      values (?, ?, ?, ?)''', ('testing if code can be saved', str(request.form.get('value')), int(time.time()), session['user_id']))
    db.commit()
    flash('code was saved')
    return redirect(url_for('index'))


@app.route('/editCode', methods=['PATCH'])
def edit_code():
    if 'user_id' not in session:
        abort(401)
    db = get_db()
    title = str('testing if code can be saved')
    db.execute('''update snippets set code = ? where id = ?''', (str(request.form.get('title')), str(request.form.get('id'))))
    db.commit()
    flash('code was updated')
    return redirect(url_for('index'))

@app.route('/editTitle', methods=['PATCH'])
def edit_title():
    if 'user_id' not in session:
        abort(401)
    db = get_db()
    db.execute('update snippets set title = ? where id = ?', (str(request.form.get('title')), str(request.form.get('id'))))
    db.commit()
    flash('title was updated')
    return redirect(url_for('index'))
