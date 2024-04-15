from app import db

class Permit(db.Model):
    __tablename__ = "permits"
 
    locationId = db.Column(db.Integer, primary_key=True)
    applicant = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
