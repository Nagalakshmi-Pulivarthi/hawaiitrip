import datetime as dt
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from flask import Flask, jsonify
from sqlalchemy import extract  



#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///hawaii1.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement=Base.classes.Measurement
Station=Base.classes.Station

# Create our session (link) from Python to the DB
session = Session(engine)

################################################
#Flask Setup
################################################
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
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start</br>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
   # "" "Return a list of all tobs and dates of last year ""
    date_object = session.query(func.max(Measurement.date)).scalar()
    datetime_object =datetime.strptime(date_object, '%Y-%m-%d')
    startdate =datetime_object - relativedelta(months=12)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date.between( startdate,date_object )).all()
    #all_names = list(np.ravel(results))
    #all_tobs = []
    # for tob  in results:
    #    #print(tob.station)
    #    tob_dict = {}
    #    tob_dict[tob.date] = tob.tobs
    #    #tob_dict["tobs"]=tob.tobs
    #    all_tobs.append(tob_dict)
    #
    #all_tobs={k:v for k ,v in results}
    all_tobs=dict(results)
    return jsonify(all_tobs)

@app.route("/api/v1.0/stations")    
def stations():
     # "" " Return all stations""
      results1=session.query(Station.station).all()
      all_stations=list(np.ravel(results1))  
      return  jsonify(all_stations) 
    
@app.route("/api/v1.0/tobs")
def previous_tobs():
    current_date=datetime.today()
    previous_year=current_date.year-1
    results2=session.query(Measurement.tobs).filter(extract('year',Measurement.date)==previous_year).all()
    previous_tobs= np.unique(np.ravel(results2)).tolist()
    return  jsonify(previous_tobs) 

@app.route('/api/v1.0/<start>')
@app.route("/api/v1.0/<start>/<end>")
def start_temp(start,end=''):
    start = datetime.strptime(start,'%Y-%m-%d')
    if(end=='') :
        end= datetime.today()
    else : 
        end = datetime.strptime(end,'%Y-%m-%d')
    results3=session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
                    filter(Measurement.date>=start).\
                    filter(Measurement.date<=end).\
                    all()
    temp_dict={}
    temp_dict["max"]= results3[0][0]
    temp_dict["min"]=results3[0][1]
    temp_dict["avg"]=results3[0][2]

    
    return  jsonify(temp_dict) 
if __name__ == '__main__':
    app.run(debug=True)

