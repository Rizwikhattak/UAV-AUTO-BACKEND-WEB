from config import db

class SolarPanelEfficiency(db.Model):
    __tablename__ = "solar_panel_efficiency"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(200), nullable=False)
    efficiency_pct = db.Column(db.Float, nullable=True)
    validity = db.Column(db.Integer, nullable=False, default=1)
