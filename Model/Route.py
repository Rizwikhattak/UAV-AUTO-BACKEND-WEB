from config import db

class Route(db.Model):
    __tablename__ = "Route"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    validity = db.Column(db.Integer, nullable=False, default=1)
    rows = db.Column(db.Integer, nullable=False)
    columns = db.Column(db.Integer, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey("Station.id"))

    locationPins = db.relationship('LocationPins', back_populates='route')
    missionPlanner = db.relationship('MissionPlanner', back_populates='route')
