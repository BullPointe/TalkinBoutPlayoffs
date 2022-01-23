from flask import Flask, render_template, request, redirect, url_for    

app = Flask(__name__)

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
    return render_template("table.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")
    
    
if __name__ == "__main__":
    app.run(debug=True)