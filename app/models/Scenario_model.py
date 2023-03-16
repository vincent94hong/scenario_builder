from app import db
from sqlalchemy import func


class Scenario(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500))
    # characters = db.relationship('Character', backref=db.backref('characters'))
    # episodes = db.relationship('Episode', backref=db.backref('scenarios'))

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    # is_deleted = db.Column(db.Boolean(), nullable=False, default=False)


    @classmethod
    def find_scenario_specify(cls,user_id, scenario_title):
        return Scenario.query.filter_by(user_id=user_id, title=scenario_title).first()
    
    @classmethod
    def find_scenario_by_user_id(cls, user_id):
        return Scenario.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def find_scenario_by_title(cls, scenario_title):
        return Scenario.query.filter_by(title=scenario_title).all()
