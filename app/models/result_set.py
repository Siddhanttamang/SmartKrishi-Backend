from app import db
from datetime import datetime, timezone

class ResultSetModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    report = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

    user = db.relationship('UserModel', backref=db.backref('resultsets', lazy=True))

    def __repr__(self):
        return f"<ResultSet(class_name={self.class_name}, report={self.report})>"

