from app import db
from sqlalchemy import func


class User(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(200), nullable=True)
    user_phone = db.Column(db.String(13), nullable=True)
    user_pw = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())

    @classmethod
    def find_one_by_user_id(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()