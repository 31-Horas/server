from app.extensions import db

class Bucket(db.Model):
    __tablename__ = 'bucketfile'

    bucketfile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucketfile_name = db.Column(db.String(100), nullable=False)
    bucketfile_code = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __init__(self, bucketfile_name, bucketfile_code, user_id):
        self.bucketfile_name = bucketfile_name
        self.bucketfile_code = bucketfile_code
        self.user_id = user_id
        