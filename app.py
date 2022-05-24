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

    session.close()
    return

# @app.route("/api/v1.0/tobs")
# def tobs():
#      # create session
#     session = Session(engine)
    
#     session.close()
#     return

# # @app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>") # separate these routes
# # def startend():
#  # create session
#     # session = Session(engine)
    
#     # session.close()
# #     return

# running app
if __name__ == "__main__":
    app.run(debug=True)