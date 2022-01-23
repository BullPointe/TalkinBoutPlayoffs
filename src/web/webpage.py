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
    # INSERT INTO roster SELECT 'Joe Burrow' AS player, 0 AS teamID UNION ALL SELECT 'Derrick Henry', 0 UNION ALL SELECT 'Deebo Samuel', 1 UNION ALL SELECT 'Ryan Tannehill', 1
    #db.execute_statement("INSERT INTO roster SELECT 'Jalen Hurts' AS player, 0 AS teamID UNION ALL SELECT 'Julio Jones', 0 UNION ALL SELECT 'Kyler Murray', 1 UNION ALL SELECT 'Tee Higgins', 1")
    #db.execute_statement("INSERT INTO roster SELECT 'Aaron Jones' AS player, 0 AS teamID UNION ALL SELECT 'George Kittle', 0 UNION ALL SELECT 'Tom Brady', 1 UNION ALL SELECT 'Mike Evans', 1")
    #db.execute_statement("INSERT INTO roster SELECT 'Joe Mixon' AS player, 2 AS teamID UNION ALL SELECT 'Cooper Kupp', 2 UNION ALL SELECT 'BUF', 3 UNION ALL SELECT 'Darren Waller', 3")
    #db.execute_statement("INSERT INTO roster SELECT 'Eli Mitchell' AS player, 2 AS teamID UNION ALL SELECT 'Josh Jacobs', 2 UNION ALL SELECT 'TB', 3 UNION ALL SELECT 'Stefon Diggs', 3")
    #db.execute_statement("INSERT INTO roster SELECT 'Travis Kelce' AS player, 2 AS teamID UNION ALL SELECT 'CIN', 2 UNION ALL SELECT 'Rondale Moore', 3 UNION ALL SELECT 'Rob Gronkowski', 3")
    #db.execute_statement("SELECT * FROM roster")
    #print(db.result)
    db.close_connection()
    return render_template("table.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")
    

    
if __name__ == "__main__":
    app.run(debug=True)