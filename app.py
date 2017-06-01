import os
import sqlite3
import csv
import json

from flask import Flask, render_template, request, g, jsonify, Response

app = Flask(__name__)
app.config.from_object(__name__)

DATABASE = '/Users/waihamyee/Documents/Project/SODA Python Example/vehicle.db'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/viewdb")
def viewdb():
    rows = execute_query(
        """SELECT date, count(*) FROM collisions GROUP BY date""")
    return '<br>'.join(str(row) for row in rows)


@app.route("/count_fatalities/<num>")
def countcollisions(num):
    rows = execute_query(
        """SELECT date, borough, number_of_persons_killed, count(*) FROM collisions where number_of_persons_killed >= ? GROUP BY date""", [num])
    return '<br>'.join(str(row) for row in rows)

@app.route("/data")
## datetime(strftime('%Y-%m-%dT%H:00:00', 'now'));
def print_data():
    rows = execute_query(
        """SELECT date, count(*) AS count FROM collisions where date > date(strftime('%Y-%m-%d', '2016-01-01')) GROUP BY date""")
    return Response(json.dumps(rows) , mimetype='application/json')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    ##db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def execute_query(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
