from config import db

class MaintenanceSchedule(db.Model):
    __tablename__ = "MaintenanceSchedule"

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_planner_id= db.Column(
                           db.Integer,
                           db.ForeignKey("MissionPlanner.id"),
                           )
    dateFrom = db.Column(db.Date,    nullable=False)
    dateTo= db.Column(db.Date,    nullable=False)
    validity = db.Column(db.Integer, default=1, nullable=False)
    label= db.Column(db.String(200), nullable=True)

    missionPlanner = db.relationship(
                           'MissionPlanner',
                           back_populates='maintenanceSchedules'
                        )