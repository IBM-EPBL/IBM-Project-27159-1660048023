
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)



@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/login')
def login():
     return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('signup.html')
        



if __name__=='__main__':
        app.run(debug=True)

       