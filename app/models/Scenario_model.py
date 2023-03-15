from app import db
from sqlalchemy import func


class Scenario(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_idx = db.Column(db.String(20), db.ForeignKey('user.idx', ondelete='CASCADE'))
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(1000))
    characters = db.relationship('Character', backref=db.backref('scenarios'))
    # episodes = db.relationship('Episode', backref=db.backref('scenarios'))

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)


    @classmethod
    def find_one_by_scenario_title(cls, scenario_title, search_idx=False):
        return Scenario.query.filter_by(title=scenario_title).first()
