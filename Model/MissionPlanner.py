from config import db

class MissionPlanner(db.Model):
    __tablename__ = "MissionPlanner"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    drone_id = db.Column(db.Integer, db.ForeignKey("Drone.id"))
    route_id = db.Column(db.Integer, db.ForeignKey("Route.id"))
    status = db.Column(db.String(100), nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)

    drone = db.relationship('Drone', back_populates='missionPlanner')
    route = db.relationship('Route', back_populates='missionPlanner')
    droneAvailabilityLog = db.relationship('DroneAvailabilityLog', back_populates='missionPlanner')
    sorties = db.relationship('Sortie', back_populates='missionPlanner')
    missionVideo = db.relationship('MissionVideo', back_populates='missionPlanner')
