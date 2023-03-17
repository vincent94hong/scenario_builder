from app import db
from sqlalchemy import func


class Scenario(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_idx = db.Column(db.Integer, db.ForeignKey('user.idx'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    # is_deleted = db.Column(db.Boolean(), nullable=False, default=False)

    # characters = db.relationship('Character')
    # elements = db.relationship('Elements')
    # episodes = db.relationship('Episode', backref=db.backref('scenarios'))

    @classmethod
    def find_scenario_by_title(cls,user_idx, scenario_title):
        return Scenario.query.filter_by(user_idx=user_idx, title=scenario_title).first()
    
    @classmethod
    def find_scenarios_sort_user(cls, user_idx):
        return Scenario.query.filter_by(user_idx=user_idx).all()
    
    @classmethod
    def find_scenarios_sort_title(cls, scenario_title):
        return Scenario.query.filter_by(title=scenario_title).all()
