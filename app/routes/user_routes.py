from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from app.models.user import User
from app.schemas.user_schema import RegisterSchema
from db.connection import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    schema = RegisterSchema() 

    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"status": "error", "errors": err.messages}), 400  

    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({"status": "error", "message": "Email already exists."}), 400

    existing_username = User.query.filter_by(username=data['username']).first()
    if existing_username:
        return jsonify({"status": "error", "message": "Username already exists."}), 400

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password']) 

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        return jsonify({"status": "error", "message": "Database error occurred."}), 500

    return jsonify({"status": "success", "message": "User registered successfully."}), 201
