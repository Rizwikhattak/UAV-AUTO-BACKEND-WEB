from config import db

class MissionVideo(db.Model):
    __tablename__ = "MissionVideo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_planner_id = db.Column(db.Integer, db.ForeignKey("MissionPlanner.id"))
    file_path = db.Column(db.String(300), nullable=False)
    validity = db.Column(db.Integer, nullable=False, default=1)

    missionPlanner = db.relationship('MissionPlanner', back_populates='missionVideo')
    missionDataLocation = db.relationship('MissionDataLocation', back_populates='missionVideo')
    missionDataImages = db.relationship('MissionDataImages', back_populates='missionVideo')
