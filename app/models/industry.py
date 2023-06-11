from app.extensions import db

from flask_login import UserMixin


class Industry(db.Model, UserMixin):
    __tablename__ = "industryFile"

    industryFile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    industryFile_name = db.Column(db.String(45), nullable=False)
    industryFile_path = db.Column(db.String(45), nullable=False)

    def __init__(self, industryFile_name, industryFile_path):
        self.industryFile_name = industryFile_name
        self.industryFile_path = industryFile_path

    def get_id(self):
        return str(self.industryFile_id)
