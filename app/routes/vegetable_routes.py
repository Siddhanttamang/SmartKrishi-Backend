import os
from flask import Blueprint, request, current_app
from flask_restful import Resource, reqparse, fields, marshal_with, Api, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app import db
from app.models.vegetable import VegetableModel
from app.models.user import UserModel
from uuid import uuid4

# Blueprint setup
vegetable_bp = Blueprint('vegetable_bp', __name__)
api = Api(vegetable_bp)

# Request parser
veg_args = reqparse.RequestParser()
veg_args.add_argument('name', type=str, required=True, help="Name is required")
veg_args.add_argument('quantity', type=float, required=True, help="Quantity is required")
veg_args.add_argument('price', type=float, required=True, help="Price is required")
veg_args.add_argument('image_url', type=str, help="Image URL or base64 string")
veg_args.add_argument('user_id', type=int, help="Optional: will be overridden by JWT")

# Response marshal fields
veg_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'quantity': fields.Float,
    'price': fields.Float,
    'image_url': fields.String(attribute=lambda x: request.host_url.rstrip('/') + x.image_url),
    'user_id': fields.Integer,
    'created_at': fields.String(attribute=lambda x: x.created_at.strftime('%d %b %Y, %I:%M %p') if x.created_at else None),
    'user_name': fields.String(attribute=lambda x: x.user.name if x.user else None),
    'user_address': fields.String(attribute=lambda x: x.user.address if x.user else None),
    'user_contact': fields.String(attribute=lambda x: x.user.contact if x.user else None)
}

# /api/vegetables/
class VegetablesResource(Resource):
    @marshal_with(veg_fields)
    def get(self):
        vegetables = VegetableModel.query.all()
        return vegetables


    @marshal_with(veg_fields)
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())

        # Get form fields (multipart/form-data)
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        image = request.files.get('image')

        # Validate required fields
        if not all([name, quantity, price, image]):
            abort(400, message="All fields including image are required")

        # Save image
        ext = os.path.splitext(secure_filename(image.filename))[1]
        unique_filename = f"{uuid4().hex}{ext}"

        # Save image
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        image.save(filepath)

        # Generate image URL
        image_url = f"/uploads/{unique_filename}"

        try:
            quantity = float(quantity)
            price = float(price)
        except ValueError:
            abort(400, message="Price and Quantity must be numbers")

        # Save to database
        veg = VegetableModel(
            name=name,
            quantity=quantity,
            price=price,
            image_url=image_url,
            user_id=user_id
        )

        db.session.add(veg)
        db.session.commit()

        return veg, 201


# /api/vegetables/<id>
class VegetableResource(Resource):
    @marshal_with(veg_fields)
    def get(self, id):
        veg = VegetableModel.query.get_or_404(id, description="Vegetable not found")
        return veg

    @marshal_with(veg_fields)
    @jwt_required()
    def patch(self, id):
        veg = VegetableModel.query.get_or_404(id, description="Vegetable not found")
        current_user_id = int(get_jwt_identity())

        if veg.user_id != current_user_id:
            abort(403, message="You can only update your own products.")

        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if name:
            veg.name = name
        if quantity:
            try:
                veg.quantity = float(quantity)
            except ValueError:
                abort(400, message="Invalid quantity")
        if price:
            try:
                veg.price = float(price)
            except ValueError:
                abort(400, message="Invalid price")

        db.session.commit()
        return veg



    @jwt_required()
    def delete(self, id):
        veg = VegetableModel.query.get_or_404(id, description="Vegetable not found")
        current_user_id = int(get_jwt_identity())

        if veg.user_id != current_user_id:
            abort(403, message="You can only delete your own products.")

        db.session.delete(veg)
        db.session.commit()
        return {'msg': 'Vegetable deleted'}, 204



# Register resources
api.add_resource(VegetablesResource, '/')
api.add_resource(VegetableResource, '/<int:id>')
