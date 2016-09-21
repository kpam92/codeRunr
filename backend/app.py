import os
import crypt
import secrets, crypt
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('CODERNR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# DATA CALLS FROM FRONTEND

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/')
def show_snippets():
    db = get_db()
    cur = db.execute('select title from snippets order by id desc')
    snippets = cur.fetchall()
    return render_template('index.html', snippets=snippets)


@app.route('/add', methods=['POST'])
def add_snippet():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into snippets (title) values (?)',
               [request.form['code']])
    db.commit()
    flash('New snippet was successfully posted')
    return redirect(url_for('index'))
    return render_template('show_snippets.html', snippets=snippets)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into snippets (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_snippets'))

def get_users():
    db = get_db()
    cur = db.execute('select * from users')
    users = cur.fetchall()
    return users

@app.route('/signup', methods=['GET', 'POST'])
def signup():
def create_session_token():
    token = secret.token_urlsave(32)
    return token

def crypt(password):
    return crypt.crypt(password)

@app.route('/signup', methods=['GET', 'POST'])
def signup:
    error = None
    if request.method == 'POST':
        users = get_users()
        for user in users:
            if request.form['username'] == user.username:
                error = 'Username has already been taken'
            elif request.form['password'].len() < 6:
                error = 'Password too short'
            else:
                session['username'] = user.username
            else
                session['token'] = user.session_token
                flash('You were logged in')
                db = get_db()
                username = request.form['username']
                password_digest = crypt(request.form['password'])
                full_name = request.form['full_name']
                db.execute('insert into users (username, password_digest, full_name) values (?, ?, ?)',
                           [username, password_digest, full_name])
                db.commit()
                flash('New entry was successfully posted')
                return redirect(url_for('index'))
    return render_template('index.html', error=error)
                return redirect(url_for('show_snippets'))
    return render_template('login.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        users = get_users()
        for user in users:
            if request.form['username'] != user.username:
                error = 'Invalid username'
            elif crypt(request.form['password']) != user.password_digest:
                error = 'Invalid password'
            else:
                session['username'] = user.username
                flash('You were logged in')
                return redirect(url_for('index'))
    return render_template('index.html', error=error)
            else
                session['token'] = user.session_token
                flash('You were logged in')
                return redirect(url_for('show_snippets'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
