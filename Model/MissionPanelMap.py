from config import db

class MissionPanelMap(db.Model):
    __tablename__ = "mission_panel_map"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_planner_id = db.Column(db.Integer, db.ForeignKey("MissionPlanner.id"))
    solar_row = db.Column(db.Integer, nullable=False)
    solar_column = db.Column(db.Integer, nullable=True)
    solar_watts = db.Column(db.Integer, nullable=True)
    solar_frame_no = db.Column(db.Integer, nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)
    missionPlanner = db.relationship('MissionPlanner', back_populates='missionPanelMap')
    efficiencyReport = db.relationship('EfficiencyReport', back_populates='missionPanelMap')

