from app import db

class VegetableModel(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))  # URL or path to the image

    # Foreign key to UserModel
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    
    user = db.relationship('UserModel', backref=db.backref('vegetables', lazy=True))

    def __repr__(self):
        return f"<Vegetable(name={self.name}, quantity={self.quantity}, price={self.price}, user_id={self.user_id})>"
