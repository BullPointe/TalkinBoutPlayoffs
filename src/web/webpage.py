from flask import Flask, render_template, request, redirect, url_for
import sqlite3
#from .. import connect_to_db
import sys 
sys.path.append('..')
from connect_to_db import DatabaseConnection

app = Flask(__name__)
db = DatabaseConnection()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('action1') == 'League Leaderboard':
            return redirect(url_for('table'))
        elif  request.form.get('action2') == 'Player Statistics':
            return redirect(url_for('stats'))
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('home.html')
    return render_template("home.html")

@app.route("/table")
def table():
    db.create_connection()
    # useful commands: SELECT name FROM sqlite_master WHERE type='table';
    # CREATE TABLE IF NOT EXISTS roster (player TEXT PRIMARY KEY, teamID INTEGER NOT NULL);
    # INSERT INTO roster SELECT 'Joe Burrow' AS 'player', 0 AS 'teamID' UNION ALL SELECT 'Derrick Henry', 0 UNION ALL SELECT 'Deebo Samuel', 1 UNION ALL SELECT 'Ryan Tannehill', 1
    db.execute_statement("SELECT name FROM sqlite_master WHERE type='table';")
    print(db.result)
    db.close_connection()
    return render_template("table.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")
    

    
if __name__ == "__main__":
    app.run(debug=True)