
from config import db

class MaintenancePersonal(db.Model):
    __tablename__ = 'MaintenancePersonal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    validity = db.Column(db.Integer, default=1, nullable=False)




