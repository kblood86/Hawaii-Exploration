# import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

################################
session = Session(engine)

# find the last date in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date 1 year ago from the last data point in the database
yr_prior = dt.date(2017,8,23) - dt.timedelta(days=365)

session.close()
################################

# Create an app
app = Flask(__name__)

################################
# Flask Routes

@app.route("/")
def home():
     #List all routes that are available.
    return(
        f"Welcome to SQL Alchemy Hawaii Dataset!<br/> "
        f"Available Routes:<br/>"
        f"<br/>"  
        f"Precipitation:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Observed Temperatures from Most Active Station:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Minimum, maxiumum, and average temperatures for chosen date: (please use 'yyyy-mm-dd' format):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;<br/>"
        f"<br/>"
        f"Minimum, maxiumum, and average temperatures for chosen date range: (please use 'yyyy-mm-dd'/'yyyy-mm-dd' format for start and end values):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
        
    )
###########################################################

# `/api/v1.0/precipitation` -Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session link
    session = Session(engine)

    """Return the dictionary for date and precipitation info"""
    # Query precipitation and date values 
    results = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()
    
    # Create a dictionary as date the key and prcp as the value
    precipitation = []
    for date,prcp in results:
        precp_dict = {}
        precp_dict["date"] = date
        precp_dict["prcp"] = prcp
        precipitation.append(precp_dict)

    return jsonify(precipitation )

#################################################################
#Return a JSON list of stations from the dataset.
# create stations route    
@app.route("/api/v1.0/stations")
def stations():
    # Create the session link
    session = Session(engine)
    
    # Query data to get stations list
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Convert into list of dictionaries 
    station_list = []
    for result in results:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_list.append(r)
    
    # jsonify the list
    return jsonify(station_list)

##################################################################

#Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    # create session link
    session = Session(engine)
    
  #query all tobs for last observed year
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= yr_prior).filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

    # Convert into list of dictionaries for each observed temperature
    tobs = []
    for result in results:
        r = {}
        r["Date"] = result[1]
        r["Temprature"] = result[0]
        tobs.append(r)

    # jsonify the list
    return jsonify(tobs)

######################################################################

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
    # create session link
    session = Session(engine)

    #Convert entered to yyyy-mm-dd format for the query
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

    # query data for the start date value
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).all()

    session.close()

    # Create a list to hold results
    temp_list = []
    for result in results:
        r = {}
        r["Start Date"] = start_dt
        r["Minimum Temp"] = result[0]
        r["Average Temp"] = result[1]
        r["Maximum Temp"] = result[2]
        temp_list.append(r)

    # jsonify the result
    return jsonify(temp_list)

##################################################################
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/min_max_avg/<start>/<end>")
def start_end(start, end):
    # create session link
    session = Session(engine)

    # take start and end dates and convert to yyyy-mm-dd format for the query
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")

    # query data for the start date value
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).\
        filter(Measurement.date <= end_dt)

    session.close()

    # Create a list to hold results
    temp_list = []
    for result in results:
        r = {}
        r["Start Date"] = start_dt
        r["End Date"] = end_dt
        r["Minimum Temp"] = result[0]
        r["Average Temp"] = result[1]
        r["Maximum Temp"] = result[2]
        temp_list.append(r)

    # jsonify the result
    return jsonify(temp_list)

##########################################################

if __name__ == "__main__":
    app.run(debug=True)