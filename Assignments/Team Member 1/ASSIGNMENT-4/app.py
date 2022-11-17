from flask import Flask, render_template
from flask import request 
from flask import redirect
from flask import url_for
from flask import flash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

def init_db():
    db = sqlite3.connect('users.db')
    with open('schema.sql', 'r') as schema:
        db.executescript(schema.read())
    db.commit()

@app.cli.command('initdb')
def initdb_cmd():
    init_db()
    print("Initialised database.")

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/signin', methods=('GET', 'POST'))
def signin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT password FROM users WHERE username = ?', (username, )
        ).fetchone()
        
        if user is None:
            error = 'Incorrect Username/Password.'
        elif password != user['password']:
            print(user)
            error = 'Incorrect Password.'

        if error is None:
            return redirect(url_for('about'))
        flash(error)
        db.close()

    return render_template('signin.html', title='Sign In', error=error)


@app.route('/signup', methods=('POST', 'GET'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        db = get_db()
        curr = db.cursor()
        
        curr.execute(
            'INSERT INTO users (username, password, email, name) VALUES (?, ?, ?, ?);', (username, password, email, name)
        )
        db.commit()
        curr.close()
        db.close()
        return render_template('index.html', title="Home", succ="Registration Successfull!")
        

    return render_template('signup.html', title='Sign Up')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)    
