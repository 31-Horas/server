from app.extensions import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(254), nullable=False)
    user_pswd = db.Column(db.String(100), nullable=False)

    def __init__(self, user_email, user_pswd):
        self.user_email = user_email
        self.user_pswd = user_pswd

    def get_id(self):
        return str(self.user_id)