from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.blueprints import Blueprint

from app.extensions import db

# Define a blueprint for the users
users_bp = Blueprint('users', __name__, url_prefix='/users')


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(254), nullable=False)
    user_pswd = db.Column(db.String(45), nullable=False)

    def __init__(self, user_email, user_pswd):
        self.user_email = user_email
        self.user_pswd = user_pswd

# Flask routes for user operations
@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    new_user = User(email, password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201

@users_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {'id': user.user_id, 'email': user.user_email}
        result.append(user_data)
    return jsonify(result), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {'id': user.user_id, 'email': user.user_email}
    return jsonify(user_data), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.user_email = data['email']
    user.user_pswd = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully.'}), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200