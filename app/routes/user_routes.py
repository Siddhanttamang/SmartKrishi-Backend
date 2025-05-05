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
    'contact': fields.String
}

# Input parser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")
user_args.add_argument('address', type=str)
user_args.add_argument('password', type=str)
user_args.add_argument('contact', type=str)


# Helper function
def update_user_fields(user, args, allow_email_change=True):
    if args['email'] and args['email'] != user.email:
        if allow_email_change:
            existing_email = UserModel.query.filter(UserModel.email == args['email'], UserModel.id != user.id).first()
            if existing_email:
                return {"status": "error", "message": "Email already taken"}, 409
            user.email = args['email']

    if args['contact'] and args['contact'] != user.contact:
        existing_contact = UserModel.query.filter(UserModel.contact == args['contact'], UserModel.id != user.id).first()
        if existing_contact:
            return {"status": "error", "message": "Contact already in use"}, 409
        user.contact = args['contact']

    if args['name']:
        user.name = args['name']
    if args['address']:
        user.address = args['address']
    if args['password']:
        if len(args['password']) < 6:
            return {"status": "error", "message": "Password must be at least 6 characters"}, 400
        user.password = generate_password_hash(args['password'])

    return None


# List all users or create new one (admin only)
class UsersResource(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'status': 'error', 'message': 'Only admin can view all users'}, 403

        return UserModel.query.all()

    @marshal_with(user_fields)
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'status': 'error', 'message': 'Only admin can create users'}, 403

        args = user_args.parse_args()
        if not args['password'] or len(args['password']) < 6:
            return {'status': 'error', 'message': 'Password is required and must be at least 6 characters'}, 400

        if UserModel.query.filter_by(email=args['email']).first():
            return {"status": "error", "message": "User already exists with this email"}, 409

        if args['contact'] and UserModel.query.filter_by(contact=args['contact']).first():
            return {"status": "error", "message": "Contact already in use"}, 409

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
        user = UserModel.query.get_or_404(id, description="User not found")
        return user

    @marshal_with(user_fields)
    @jwt_required()
    def patch(self, id):
        claims = get_jwt()
        current_user_id = int(get_jwt_identity())
        if claims.get('role') != 'admin' and current_user_id != id:
            return {'status': 'error', 'message': 'Access denied'}, 403

        user = UserModel.query.get_or_404(id, description="User not found")
        args = user_args.parse_args()
        error = update_user_fields(user, args)
        if error:
            return error

        db.session.commit()
        return user

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'status': 'error', 'message': 'Only admin can delete users'}, 403

        user = UserModel.query.get_or_404(id, description="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204


# Get/update current user's profile
class UserMeResource(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = UserModel.query.get_or_404(user_id, description="User not found")
        return user

    @marshal_with(user_fields)
    @jwt_required()
    def patch(self):
        user_id = int(get_jwt_identity())
        user = UserModel.query.get_or_404(user_id, description="User not found")
        args = user_args.parse_args()
        error = update_user_fields(user, args, allow_email_change=True)
        if error:
            return error

        db.session.commit()
        return user
    @jwt_required()
    def delete(self):
        user_id = int(get_jwt_identity())
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")

        db.session.delete(user)
        db.session.commit()
        return {"msg": "User deleted successfully"}, 200

# Register routes
api.add_resource(UsersResource, '/')
api.add_resource(UserResource, '/<int:id>')
api.add_resource(UserMeResource, '/me')
