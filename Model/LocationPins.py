from config import db

class LocationPins(db.Model):
    __tablename__ = "LocationPins"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer, db.ForeignKey("Route.id"))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    validity = db.Column(db.Integer, nullable=False, default=1)

    route = db.relationship('Route', back_populates='locationPins')
