from config import db

class DroneAvailabilityLog(db.Model):
    __tablename__ = "DroneAvailabilityLog"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drone_id = db.Column(db.Integer, db.ForeignKey("Drone.id"))
    mission_planner_id = db.Column(db.Integer, db.ForeignKey("MissionPlanner.id"))
    start_date = db.Column(db.Date, nullable=True)
    start_date_limit = db.Column(db.Date, nullable=True)
    start_time_limit = db.Column(db.Time, nullable=True)
    end_date_limit = db.Column(db.Date, nullable=True)
    end_time_limit = db.Column(db.Time, nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)

    drone = db.relationship('Drone', back_populates='droneAvailabilityLog')
    missionPlanner = db.relationship('MissionPlanner', back_populates='droneAvailabilityLog')
