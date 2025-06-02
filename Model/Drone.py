from config import db

class Drone(db.Model):
    __tablename__ = "Drone"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    ceiling = db.Column(db.Float, nullable=False)
    fps = db.Column(db.Integer, nullable=False)
    flight_duration = db.Column(db.Float, nullable=False, default=1)
    speed = db.Column(db.Float, nullable=False, default=70)
    image_path = db.Column(db.String(255), nullable=True)
    station_id = db.Column(db.Integer, db.ForeignKey("Station.id"))
    validity = db.Column(db.Integer, nullable=False, default=1)

    droneAvailabilityLog = db.relationship('DroneAvailabilityLog', back_populates='drone')
    droneStationMapping = db.relationship('DroneStationMapping', back_populates='drone')
    missionPlanner = db.relationship('MissionPlanner', back_populates='drone')
