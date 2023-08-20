# Import required packages
import hashlib
import pickle
import MySQLdb.cursors

from flask import Flask, redirect, render_template, request, url_for,session
from flask_sqlalchemy import SQLAlchemy
import sklearn 
import numpy as np 
 

# Initialize the app
app = Flask(__name__, template_folder="templates")
app.secret_key = '1234'
model = pickle.load(open("E:\Data-science-Assignment-Great-Learning\Python-for-DS-Graded-Project-3\model.pkl", "rb"))

ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Rohit2798@localhost:3306/loan"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:password@localhost:3306/loan"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)

    Username = db.Column(db.String(200))
    Password = db.Column(db.String(200))

    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password


db.create_all()


# Adding a route for the homepage
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Route for the page where the button is clicked
@app.route('/login', methods=["GET"])
def loginPage():
    return render_template('login.html')

@app.route('/register',methods=["GET"])
def registerPage():
    return render_template("register.html")

@app.route('/register/userRegistered',methods=["POST"])
def register():
    # Output message if something goes wrong...
    msg = 'you are registed succesfully!!!'
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form :
        # Create variables for easy access
        Username = request.form['username']
        Password = request.form['password']
         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE username = %s', (Username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not Username or not password:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = Password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s)', (Username, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



if __name__ == "__main__":
    app.run()
