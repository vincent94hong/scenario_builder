from flask import abort
from sqlalchemy import func

from app import db
from app.models.scenario_model import Scenario


# characters_groups = db.Table(
#     'characters_groups',
#     db.Column('character_name', db.Integer, db.ForeignKey('character.name'), primary_key=True),
#     db.Column('group_name', db.Integer, db.ForeignKey('group.name'), primary_key=True),
# )


class Character(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    scenario_idx = db.Column(db.Integer, db.ForeignKey('scenario.idx'))
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)

    elements = db.relationship('Element', backref=db.backref('characters'))
    # group_name = db.relationship('Group', secondary=characters_groups) # backref=db.backref('characters')

    @classmethod
    def find_character_by_name(cls, scenario_idx, character_name):
        return Character.query.filter_by(
            scenario_idx=scenario_idx, 
            name=character_name
        ).first()

    @classmethod
    def find_characters(cls, scenario_idx): 
        '''공개 여부 관계없이, 모든 캐릭터'''
        return Character.query.filter_by(
            scenario_idx=scenario_idx
        ).all()

    @classmethod
    def find_opened_characters(cls, scenario_idx, is_opened=True): 
        '''is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물'''
        return Character.query.filter_by( 
            scenario_idx=scenario_idx, 
            is_opened=is_opened
        ).all()
    

class Element(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    character_idx = db.Column(db.Integer, db.ForeignKey('character.idx'))
    element = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)


    @classmethod
    def find_elements(cls, character_idx):
        return Element.query.filter_by(character_idx=character_idx).all()
    
    @classmethod
    def find_element_by_element_name(cls, character_idx, element_name):
        return Element.query.filter_by(
            character_idx=character_idx,
            element=element_name
        ).first()