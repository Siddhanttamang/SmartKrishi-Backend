from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal_with, Api, abort
from app.models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from app import db

user_bp = Blueprint('user_bp', __name__)
api = Api(user_bp)

# Output structure
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'address': fields.String,
    'contact':fields.String
}

# Input parser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")
user_args.add_argument('address', type=str, help="Address of the user")
user_args.add_argument('password', type=str, help="Password of the user (required on creation)")
user_args.add_argument('contact', type=str, help="contact of the user ")

# List all users or create new one (admin only)
class UsersResource(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'msg': 'Only admin can view all users'}, 403

        return UserModel.query.all()

    @marshal_with(user_fields)
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'msg': 'Only admin can create users'}, 403

        args = user_args.parse_args()
        if not args['password']:
            return {'msg': 'Password is required'}, 400

        if UserModel.query.filter_by(email=args['email']).first():
            return {"msg": "User already exists with this email"}, 409

        hashed_password = generate_password_hash(args['password'])

        user = UserModel(
            name=args['name'],
            email=args['email'],
            password=hashed_password,
            address=args['address'],
            contact=args['contact']
        )

        db.session.add(user)
        db.session.commit()
        return user, 201

# Retrieve, update, or delete specific user
class UserResource(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    @jwt_required()
    def patch(self, id):
        claims = get_jwt()
        user_id = int(get_jwt_identity())

        if claims.get('role') != 'admin' and user_id != id:
            return {'msg': 'Access denied'}, 403

        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")

        # Email update: check for conflict
        if args['email'] and args['email'] != user.email:
            if UserModel.query.filter_by(email=args['email']).first():
                return {"msg": "Email already taken"}, 409
            user.email = args['email']

        if args['name']:
            user.name = args['name']

        if args['address']:
            user.address = args['address']

        if args['contact']:
            # Optional: Check for uniqueness
            if UserModel.query.filter_by(contact=args['contact']).first() and user.contact != args['contact']:
                return {"msg": "Contact already in use"}, 409
            user.contact = args['contact']

        # Optional: update password if provided
        if args['password']:
            user.password = generate_password_hash(args['password'])

        db.session.commit()
        return user

    

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'msg': 'Only admin can delete users'}, 403

        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

# Get current user's profile
class UserMeResource(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user

# Register routes
api.add_resource(UsersResource, '/')
api.add_resource(UserResource, '/<int:id>')
api.add_resource(UserMeResource, '/me')
