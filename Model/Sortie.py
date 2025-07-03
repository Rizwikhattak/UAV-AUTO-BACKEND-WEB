from config import db

class Sortie(db.Model):
    __tablename__ = "Sortie"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_planner_id = db.Column(db.Integer, db.ForeignKey("MissionPlanner.id"))
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    duration = db.Column(db.Float, nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)

    missionPlanner = db.relationship('MissionPlanner', back_populates='sorties')
