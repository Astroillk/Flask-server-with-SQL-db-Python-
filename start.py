import pyodbc as pyodbc
from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)

app.secret_key = 'My secret key.'


@app.route('/')
def index():
    if 'login' in session:
        session.pop('login', None)
        session.pop('password', None)
        session.pop('employee_id', None)
    return render_template('index.html')

@app.route('/actions', methods=['GET', 'POST'])
def actions():
    if 'login' in session:
        cnxn = pyodbc.connect(
            'driver={SQL Server};' +
            'server=localhost\SQLEXPRESS;' +
            'DATABASE=ServerDatabase;' +
            'UID=' + session["login"] + ';PWD=' + session["password"]
        )
        cursor = cnxn.cursor()
        cursor.execute('SELECT roleid FROM Crew WHERE id=' + session["employee_id"])
        row = cursor.fetchone()
        if row[0] == 2:
            return render_template('ca_actions.html')
        else:
            return render_template('index.html')
    else:
        session["login"] = request.form['log']
        session["password"] = request.form['pwd']
        session["employee_id"] = request.form['id']
    return redirect(url_for('actions'))