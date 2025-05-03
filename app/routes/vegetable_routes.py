from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal_with,Api, abort
from app.models.vegetable import VegetableModel
from app import db, api
from flask_jwt_extended import jwt_required, get_jwt_identity

vegetable_bp = Blueprint('vegetable_bp', __name__)
api = Api(vegetable_bp)

# Request parser
veg_args = reqparse.RequestParser()
veg_args.add_argument('name', type=str, required=True, help="Name is required")
veg_args.add_argument('quantity', type=float, required=True, help="Quantity is required")
veg_args.add_argument('price', type=float, required=True, help="Price is required")
veg_args.add_argument('image_url', type=str, help="Image URL or base64 string")
veg_args.add_argument('user_id', type=int, help="Optional: will be overridden by JWT")

# Response fields
veg_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'quantity': fields.Float,
    'price': fields.Float,
    'image_url': fields.String,
    'user_id': fields.Integer,
    'user_address': fields.String(attribute=lambda x: x.user.address if x.user else None),
    'user_contact': fields.String(attribute=lambda x: x.user.contact if x.user else None)

}

class VegetablesResource(Resource):
    @marshal_with(veg_fields)
    def get(self):
        return VegetableModel.query.all()

    @marshal_with(veg_fields)
    @jwt_required()
    def post(self):
        args = veg_args.parse_args()
        user_id = int(get_jwt_identity())

        veg = VegetableModel(
            name=args['name'],
            quantity=args['quantity'],
            price=args['price'],
            image_url=args.get('image_url'),
            user_id=user_id
        )

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
        veg.image_url = args.get('image_url')
        veg.user_id = args.get('user_id') or veg.user_id  # fallback to existing

        db.session.commit()
        return veg

    def delete(self, id):
        veg = VegetableModel.query.get(id)
        if not veg:
            abort(404, message="Vegetable not found")
        db.session.delete(veg)
        db.session.commit()
        return '', 204

# Resource registration
api.add_resource(VegetablesResource, '/')
api.add_resource(VegetableResource, '/<int:id>')