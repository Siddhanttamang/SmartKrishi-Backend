from app import db

class VegetableModel(db.Model):
    __tablename__ = 'vegetables'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Vegetable(name={self.name}, quantity={self.quantity}, price={self.price})>"
