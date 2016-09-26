import time
import pdb
import os
import psycopg2
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
import sys
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

# create our little application :)
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


def get_db():
    return psycopg2.connect("dbname = 'codernr_dev' host='localhost'")


@app.teardown_appcontext
def close_database(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    db = get_db().cursor()
    with app.open_resource('schema.sql', mode='r') as f:
        db.execute(f.read())
    print(db)
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


def query_db(query, query_args=(), one=False):
    str_query_args = []
    for arg in query_args:
        str_query_args.append(str(arg))
    cur = get_db().cursor()
    cur.execute(query, str_query_args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/home', methods=['PATCH', 'GET'])
def index():
    if not g.user:
        return redirect(url_for('login'))
    code_menu = query_db('SELECT title, id FROM snippets WHERE snippets.user_id = %s', [session['user_id']])
    return render_template('index.html', menu_items=code_menu)

@app.route('/getCode', methods=['GET'])
def get_code():
    url = request.url
    codeId = int(str(url.split("=")[1]))
    code = query_db("SELECT * FROM snippets WHERE snippets.id = %s", [codeId], one=True)
    return str(code[1] + '/~=^md' + code[3])

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('SELECT * FROM users WHERE id = %s', [session['user_id']], one=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        user = query_db('''SELECT * FROM users WHERE username = %s''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user[3], request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user[0]
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

def get_user_id(username):
    rv = query_db("""SELECT id FROM users WHERE username = %s""",
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
            db.cursor().execute('''INSERT INTO users (username, email, pw_hash) values (%s, %s, %s)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password'])])
            db.commit()
            flash('You were successfully registered')
            user = query_db('''SELECT * FROM users WHERE username = %s''', [request.form['username']], one=True)
            session['user_id'] = user[0]
            return redirect(url_for('index'))
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
    db.cursor().execute('''INSERT INTO snippets (title, code, user_id)
      values (%s, %s, %s)''', (str(request.form.get('title')), str(request.form.get('value')), session['user_id']))
    db.commit()
    flash('code was saved')
    return redirect(url_for('index'))


@app.route('/editCode', methods=['PATCH'])
def edit_code():
    if 'user_id' not in session:
        abort(401)
    db = get_db()
    db.cursor().execute('''UPDATE snippets SET title = %s, code = %s WHERE id = %s''', (str(request.form.get('title')), str(request.form.get('value')), str(request.form.get('id'))))
    db.commit()
    flash('code was updated')
    return redirect(url_for('index'))
