from config import db

class DroneStationMapping(db.Model):
    __tablename__ = "DroneStationMapping"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drone_id = db.Column(db.Integer, db.ForeignKey("Drone.id"))
    station_id = db.Column(db.Integer, db.ForeignKey("Station.id"))
    status = db.Column(db.String(100), nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)

    drone = db.relationship('Drone', back_populates='droneStationMapping')
    station = db.relationship('Station', back_populates='droneStationMapping')
