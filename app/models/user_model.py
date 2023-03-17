from app import db
from sqlalchemy import func


class User(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(13), nullable=True)
    pw = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())

    # scenarios = db.relationship('Scenario')
    # characters = db.relationship('Character')
    # elements = db.relationship('Elements')

    @classmethod
    def find_user(cls, id):
        return User.query.filter_by(id=id).first()