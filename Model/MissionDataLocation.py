from config import db

class MissionDataLocation(db.Model):
    __tablename__ = "MissionDataLocation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_video_id = db.Column(db.Integer, db.ForeignKey("MissionVideo.id"))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    damage = db.Column(db.String(50), nullable=True)  # e.g., 'dust', 'broken'
    validity = db.Column(db.Integer, nullable=False, default=1)

    missionVideo = db.relationship('MissionVideo', back_populates='missionDataLocation')
    # missionDataImages = db.relationship('MissionDataImages', back_populates='missionDataLocation')
