from app import db

class UserModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user') 
    address = db.Column(db.String(100))
    contact = db.Column(db.String(15), unique=True, nullable=True)  # New contact field

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email},address={self.address},contact={self.contact})>"
