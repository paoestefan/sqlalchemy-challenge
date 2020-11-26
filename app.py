from flask import Flask
app=Flask(__name__)
@app.route("/")
def index():
    """List all api routes that are available."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    maxDate = dt.date(2017, 8 ,23)
    year_ago = maxDate - dt.timedelta(days=365)

    past_temp = (session.query(m_t.date, m_t.prcp)
                .filter(m_t.date <= maxDate)
                .filter(m_t.date >= year_ago)
                .order_by(m_t.date).all())
    
    precip = {date: prcp for date, prcp in past_temp}
    
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():

    stations_all = session.query(s_t.station).all()

    return jsonify(stations_all)

@app.route('/api/v1.0/tobs') 
def tobs():  
    maxDate = dt.date(2017, 8 ,23)
    year_ago = maxDate - dt.timedelta(days=365)

    ly = (session.query(m_t.tobs)
                .filter(m_t.station == most_active_station)
                .filter(m_t.date <= maxDate)
                .filter(m_t.date >= year_ago)
                .order_by(m_t.tobs).all())
    
    return jsonify(ly)

@app.route('/api/v1.0/<start>') 
def start(start=None):
    maxDate = dt.date(2017, 8 ,23)
    tobs_only = (session.query(m_t.tobs).filter(m_t.date.between(start, maxDate)).all())
    
    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

@app.route('/api/v1.0/<start>/<end>') 
def se(start=None, end=None):

    tobs_only = (session.query(m_t.tobs).filter(m_t.date.between(start, end)).all())
    
    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

if __name__ == '__main__':
    app.run(debug=True)