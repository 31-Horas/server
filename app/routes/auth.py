from flask import Blueprint, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signin', methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return 'Already logged in', 200

    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember = True if data.get('remember') else False

        user = User.query.filter_by(user_email=email).first()

        if not user or not check_password_hash(user.user_pswd, password):
            flash('Invalid email or password', 'error')
            return 'Invalid email or password', 401

        login_user(user, remember=remember)

        return 'Logged in successfully', 200
    else:
        return 'Session Expired', 202

@auth_bp.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated:
        return 'Already logged in', 200

    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(user_email=email).first()

        if user:
            flash('Email address already exists', 'error')
            return 'Email address already exists', 201

        new_user = User(user_email=email, user_pswd=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please sign in.', 'success')
        return 'Account created successfully. Please sign in.', 202


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully', 200


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form.get('newPassword')
    repeat_password = request.form.get('repeatPassword')

    if new_password != repeat_password:
        flash('Passwords do not match', 'error')
    else:
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        flash('Password updated successfully', 'success')

    return redirect(url_for('main.profile'))