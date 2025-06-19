from app import db
from datetime import datetime, timezone

class ReportModel(db.Model):
    __tablename__ = 'reports'  

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    disease = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

   
    user = db.relationship('UserModel', backref=db.backref('reports', lazy=True))

    def __repr__(self):
        return f"<Report(crop_name={self.crop_name}, disease={self.disease})>"
