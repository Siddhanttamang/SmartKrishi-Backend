from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal_with,Api, abort
from app.models.vegetable import VegetableModel
from app import db, api

vegetable_bp = Blueprint('vegetable_bp', __name__)
api = Api(vegetable_bp) 
veg_args = reqparse.RequestParser()
veg_args.add_argument('name', type=str, required=True, help="Name is required")
veg_args.add_argument('quantity', type=float, required=True, help="Quantity is required")
veg_args.add_argument('price', type=float, required=True, help="Price is required")

veg_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'quantity': fields.Float,
    'price': fields.Float
}

class VegetablesResource(Resource):
    @marshal_with(veg_fields)
    def get(self):
        return VegetableModel.query.all()

    @marshal_with(veg_fields)
    def post(self):
        args = veg_args.parse_args()
        veg = VegetableModel(name=args['name'], quantity=args['quantity'], price=args['price'])
        db.session.add(veg)
        db.session.commit()
        return veg, 201

class VegetableResource(Resource):
    @marshal_with(veg_fields)
    def get(self, id):
        veg = VegetableModel.query.get(id)
        if not veg:
            abort(404, message="Vegetable not found")
        return veg

    @marshal_with(veg_fields)
    def patch(self, id):
        args = veg_args.parse_args()
        veg = VegetableModel.query.get(id)
        if not veg:
            abort(404, message="Vegetable not found")
        veg.name = args['name']
        veg.quantity = args['quantity']
        veg.price = args['price']
        db.session.commit()
        return veg

    def delete(self, id):
        veg = VegetableModel.query.get(id)
        if not veg:
            abort(404, message="Vegetable not found")
        db.session.delete(veg)
        db.session.commit()
        return '', 204

api.add_resource(VegetablesResource, '/')
api.add_resource(VegetableResource, '/<int:id>')
