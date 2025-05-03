from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import UserModel
from app import db
from passlib.hash import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    address=data.get('address')
    contact=data.get('contact')
    role = data.get('role', 'user')  # default role is 'user'

    if UserModel.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = bcrypt.hash(password)
    new_user = UserModel(name=name, email=email, password=hashed_password,address=address, role=role,contact=contact)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = UserModel.query.filter_by(email=email).first()
    if not user or not bcrypt.verify(password, user.password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(
    identity=str(user.id),  # must be a string
    additional_claims={"role": user.role})


    return jsonify(access_token=access_token), 200
