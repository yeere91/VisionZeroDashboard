import os
import sqlite3
import json
import sqlalchemy

from flask import Flask, render_template, request, g, jsonify, Response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

DATABASE = 'vehicle.db'

class Collisions(db.Model):
    __tablename__ = "collisions"
    index = db.Column(db.BigInteger)
    borough = db.Column(db.Text)
    contributing_factor_vehicle_1 = db.Column(db.Text)
    contributing_factor_vehicle_2 = db.Column(db.Text)
    contributing_factor_vehicle_3 = db.Column(db.Text)
    contributing_factor_vehicle_4 = db.Column(db.Text)
    contributing_factor_vehicle_5 = db.Column(db.Text)
    cross_street_name = db.Column(db.Text)
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    number_of_cyclist_injured = db.Column(db.BigInteger)
    number_of_cyclist_killed = db.Column(db.BigInteger)
    number_of_motorist_injured = db.Column(db.BigInteger)
    number_of_motorist_killed = db.Column(db.BigInteger)
    number_of_pedestrians_injured = db.Column(db.BigInteger)
    number_of_pedestrians_killed = db.Column(db.BigInteger)
    number_of_persons_injured = db.Column(db.BigInteger)
    number_of_persons_killed = db.Column(db.BigInteger)
    off_street_name = db.Column(db.Text)
    on_street_name = db.Column(db.Text)
    time = db.Column(db.Text)
    unique_key = db.Column(db.BigInteger, primary_key=True)
    vehicle_type_code1 = db.Column(db.Text)
    vehicle_type_code2 = db.Column(db.Text)
    vehicle_type_code_3 = db.Column(db.Text)
    vehicle_type_code_4 = db.Column(db.Text)
    vehicle_type_code_5 = db.Column(db.Text)
    zip_code = db.Column(db.Float)

    def __init__(self, **kwargs):
            self.borough = kwargs['borough']
            self.contributing_factor_vehicle_1 = kwargs['contributing_factor_vehicle_1']
            self.contributing_factor_vehicle_2 = kwargs['contributing_factor_vehicle_2']
            self.contributing_factor_vehicle_3 = kwargs['contributing_factor_vehicle_3']
            self.contributing_factor_vehicle_4 = kwargs['contributing_factor_vehicle_4']
            self.contributing_factor_vehicle_5 = kwargs['contributing_factor_vehicle_5']
            self.cross_street_name = kwargs['cross_street_name']
            self.date = str(kwargs['date'])
            self.latitude = kwargs['latitude']
            self.longitude = kwargs['longitude']
            self.number_of_cyclist_injured = kwargs['number_of_cyclist_injured']
            self.number_of_cyclist_killed = kwargs['number_of_cyclist_killed']
            self.number_of_motorist_injured = kwargs['number_of_motorist_injured']
            self.number_of_motorist_killed = kwargs['number_of_motorist_killed']
            self.number_of_pedestrians_injured = kwargs['number_of_pedestrians_injured']
            self.number_of_pedestrians_killed = kwargs['number_of_pedestrians_killed']
            self.number_of_persons_injured = kwargs['number_of_persons_injured']
            self.number_of_persons_killed = kwargs['number_of_persons_killed']
            self.off_street_name = kwargs['off_street_name']
            self.on_street_name = kwargs['on_street_name']
            self.time= kwargs['time']
            self.unique_key = kwargs['unique_key']
            self.vehicle_type_code1 = kwargs['vehicle_type_code1']
            self.vehicle_type_code2 = kwargs['vehicle_type_code2']
            self.vehicle_type_code_3 = kwargs['vehicle_type_code3']
            self.vehicle_type_code_4 = kwargs['vehicle_type_code4']
            self.vehicle_type_code_5 = kwargs['vehicle_type_code5']
            self.zip_code = kwargs['zip_code']

    #def __repr__(self):
        #return '<collision {}'.format(self.unique_key)

    
row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

#res = Collisions.query.all()
#object_dict = [row2dict(ob) for ob in res]
#print object_dict[0]

##print res[0].__dict__
#print res[0].borough


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/dump/', methods = ['GET'])
def dump():
    res = Collisions.query.all()

    object_dict = [row2dict(ob) for ob in res]
    ##print object_dict
    return jsonify({'collision': object_dict})
    #return Response(json.dumps(res) , mimetype='application/json')    
    #return ','.join(str(object_dict) for object_dict in object_dict)
    #return jsonify({'collision': res})

@app.route('/dump/<int:number_of_persons_killed>/')
def dump2(number_of_persons_killed):
    res = Collisions.query.get(number_of_persons_killed)
    print res

    object_dict = [row2dict(ob) for ob in res]
    ##print object_dict
    return jsonify({'collision': object_dict})


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
        """SELECT date AS date, count(*) AS count FROM collisions where date > date(strftime('%Y-%m-%d', '2016-01-01')) GROUP BY date""")
    return Response(json.dumps(rows) , mimetype='application/json')

@app.route("/data2")
def print_data2():
    rows = execute_query2(
        """SELECT to_char(date, 'MM-DD-YYYY'), count(*) AS count FROM collisions where date >= to_date('2016-01-01', 'YYYY-MM-DD') GROUP BY date ORDER BY date""")
    for i in range(0,len(rows)):
        rows[i] = dict(zip(['date','count'],rows[i]))
    
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

def get_db2():
    engine = sqlalchemy.create_engine('postgres://tmfykgvqcxxiiy:b35d2c8219898eb3558d41f5f335142f55f74a39404edc57fc6b3c7061da843f@ec2-23-21-169-238.compute-1.amazonaws.com:5432/d64fq3p9ro085j', client_encoding='utf8')
    conn = engine.raw_connection()
    cur = conn.cursor()
    return cur


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

def execute_query2(query, one=False):
    engine = sqlalchemy.create_engine('postgresql://localhost/vehicle', client_encoding='utf8')
    conn = engine.raw_connection()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return (results[0] if results else None) if one else results


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
