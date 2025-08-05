from app import db
from flask_login import UserMixin


class UserModel(db.Model,UserMixin):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user') 
    address = db.Column(db.String(100))
    contact = db.Column(db.String(15), unique=True, nullable=True)

    vegetables = db.relationship(
        'VegetableModel',
        backref='user',
        cascade="all, delete-orphan",  
        lazy=True
    )

    reports = db.relationship(
        'ReportModel',
        backref='user',
        cascade="all, delete-orphan",  
        lazy=True
    )

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, address={self.address}, contact={self.contact})>"
