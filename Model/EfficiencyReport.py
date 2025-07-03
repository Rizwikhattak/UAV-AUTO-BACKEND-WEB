from config import db

class EfficiencyReport(db.Model):
    __tablename__ = "efficiency_report"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_planner_id = db.Column(db.Integer, db.ForeignKey("MissionPlanner.id"))
    mission_panel_map_id = db.Column(db.Integer, db.ForeignKey("mission_panel_map.id"))
    label = db.Column(db.String(200), nullable=False)
    calculated_efficiency = db.Column(db.Float, nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)
    missionPlanner = db.relationship('MissionPlanner', back_populates='efficiencyReport')
    missionPanelMap = db.relationship('MissionPanelMap', back_populates='efficiencyReport')

