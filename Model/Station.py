from config import db

class Station(db.Model):
    __tablename__ = "Station"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    number_of_drones = db.Column(db.Integer, nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)

    drone = db.relationship('Drone', back_populates='station')
    routes = db.relationship('Route', back_populates='station')
    droneStationMapping = db.relationship('DroneStationMapping', back_populates='station')
