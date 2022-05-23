import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd


from flask import Flask, jsonify

# database setup to pull the data

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
meas = Base.classes.measurements ######
stat = Base.classes.stations ######
# create session
session = Session(engine)

# flask set up
app = Flask(__name__)

#Flask routes
@app.route("/")
def home():
    list_to_routes = (f'<br><h2>Welcome to Hawaii Climate Analysis ….</h2>'
    f'<br>Here are the routes you can choose:'
    f'<br>/api/v1.0/precipitation'
    f'<br>/api/v1.0/stations'
    f'<br>/api/v1.0/tobs'
    # f'<br>/api/v1.0/<start> and /api/v1.0/<start>/<end>' 
    )
    return list_to_routes 

@app.route("/api/v1.0/precipitation")
def precipitation():
    date = #dt #call the date
    # pull query based on that date
        return

@app.route("/api/v1.0/stations")
def stations():
    return

@app.route("/api/v1.0/tobs")
def tobs():
    return

# @app.route("")
# @app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>")
# def startend():
#     return

# running app
if __name__ == "__main__":
    app.run(debug=True)