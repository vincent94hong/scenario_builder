from app import db
from sqlalchemy import func


class Scenario(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())

    characters = db.relationship('Character')

    @classmethod
    def find_scenario(cls,user_id, scenario_title):
        return Scenario.query. filter_by(user_id=user_id, title=scenario_title).first()
    
    @classmethod
    def find_scenarios(cls, user_id):
        return Scenario.query.filter_by(user_id=user_id).all()
    
