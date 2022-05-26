import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd

from flask import Flask, jsonify

# database setup to pull the data

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
meas = Base.classes.measurement ######
stat = Base.classes.station ######

# flask set up
app = Flask(__name__)

#Flask routes
@app.route("/")
def home():
    list_to_routes = (f'<br><h2>Welcome to Hawaii Climate Analysis!</h2>'
    f'<br>Here are the routes you can choose:'
    f'<br><a href="/api/v1.0/precipitation">Precipitation Page</a>'
    f'<br><a href="/api/v1.0/stations">Stations Page</a>'
    f'<br><a href="/api/v1.0/tobs">TOBS Page</a>'
    f'<br>For Start Date Page enter start date at end of web address as YYYY-M-D'
    f'<br>/api/v1.0/&lt;start&gt;'
    f'<br>For Start & End Date Page enter a start date, then / and an end date at the end of the web address as YYYY-M-D'
    f'<br>/api/v1.0/&lt;start&gt;/&lt;end&gt;'
    )
    return list_to_routes 

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session
    session = Session(engine)
    results = session.query(meas.date, meas.prcp)
    session.close()
    dict_results = {}
    #loop thru the results
    for entry in results:
        dict_results[entry[0]]=entry[1]
    return jsonify(dict_results)

@app.route("/api/v1.0/stations")
def stations():
    # create session
    session = Session(engine)
    results = session.query(stat.station).all()
    session.close()
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
     # create session
    session = Session(engine)

    # Starting from the most recent data point in the database. 
    recent_date = session.query(meas.date).order_by(meas.date.desc()).first() 
    # put recent_date into date format
    last_date = dt.datetime.strptime(recent_date.date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.
    year_ago = last_date - dt.timedelta(days=365)
    #retrieve most active station
    station_list = [meas.station, func.count(meas.station)] 
    most_active_station = session.query(*station_list).group_by(meas.station).order_by(func.count(meas.station).desc())\
                        .first().station
    sel = [meas.date, meas.tobs]
    results = session.query(*sel).filter(meas.date > year_ago).filter(meas.station==most_active_station).all()
    print(results)
    session.close()

    tobs_results = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start_date(start):
 # create session
    session = Session(engine)
    sel_tobs_stats = [func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)]
    tobs_stat_query = session.query(*sel_tobs_stats).filter(meas.date >= start)
    start_results_dict = {"Temp_Min" : tobs_stat_query[0][0], "Temp_Avg" : tobs_stat_query[0][1], "Temp_Max" : tobs_stat_query[0][2]}
    session.close()
    return jsonify(start_results_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
 # create session
    session = Session(engine)
    sel_tobs_stats = [func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)]
    tobs_stat_query = session.query(*sel_tobs_stats).filter(meas.date >= start).filter(meas.date <= end)
    results_dict = {"Temp_Min" : tobs_stat_query[0][0], "Temp_Avg" : tobs_stat_query[0][1], "Temp_Max" : tobs_stat_query[0][2]}
    session.close()
    return jsonify(results_dict)

# running app
if __name__ == "__main__":
    app.run(debug=True)