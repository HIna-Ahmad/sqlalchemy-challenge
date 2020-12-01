from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
import numpy as np
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temperature/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurement"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(station.station).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    test = session.query(measurement.date).all()
    last_date = max(test)[0]

    # convert last_date from string to datetime to subtract
    last_date_obj = dt.datetime.strptime(last_date, '%Y-%M-%d')

    # to stubtract use time delft:- dt.timedelta(days=365)
    last_date_obj - dt.timedelta(days=365)

    # put in variable

    answer = last_date_obj - dt.timedelta(days=365)
    """Return a list of all tobs"""
    results = session.query(measurement.tobs).filter(
        measurement.date >= answer).all()

    # Query all passengers

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/temperature/<start>/<end>")
def temperature(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(func.min(
        measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
