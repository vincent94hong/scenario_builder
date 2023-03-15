from app import db
from sqlalchemy import func


# characters_groups = db.Table(
#     'characters_groups',
#     db.Column('character_name', db.Integer, db.ForeignKey('character.name'), primary_key=True),
#     db.Column('group_name', db.Integer, db.ForeignKey('group.name'), primary_key=True),
# )


class Character(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    scenario_title = db.Column(db.String(100), db.ForeignKey('scenario.title', ondelete='CASCADE', onupdate='CASCADE'))
    name = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.String(500), nullable=False)

    elements = db.relationship('Element') # , backref=db.backref('characters')
    # group_name = db.relationship('Group', secondary=characters_groups) # backref=db.backref('characters')

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), nullable=False, default=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)


    @classmethod
    def find_one_by_character_name(cls, char_name):
        return Character.query.filter_by(name=char_name).first()
    

    @classmethod
    def find_all_characters_by_scenario_title(cls, scenario_title): 
        '''공개 여부 관계없이, 모든 캐릭터'''
        return Character.query.filter_by(scenario_title=scenario_title)

    @classmethod
    def find_characters_by_scenario_title(cls, scenario_title, is_opened=True): 
        '''is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물'''
        return Character.query.filter_by(scenario_title=scenario_title, is_opened=is_opened)
    

class Element(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(50), db.ForeignKey('character.name', ondelete='CASCADE'))
    content_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), nullable=False, default=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
