from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal_with,Api, abort
from app.models.user import UserModel
from app import db, api

user_bp = Blueprint('user_bp', __name__)
api = Api(user_bp) 

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")


class UsersResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        return UserModel.query.all()

    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user

    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

api.add_resource(UsersResource,'/')
api.add_resource(UserResource, '/<int:id>')