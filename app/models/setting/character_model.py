from sqlalchemy import func
from app import db


class Character(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    scenario_idx = db.Column(db.Integer, db.ForeignKey('scenario.idx', ondelete='CASCADE'), nullable=False)

    scenario_title = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)

    elements = db.relationship('Element')

    @classmethod
    def find_character(cls, scenario_title, character_name):
        return Character.query.filter_by(
            scenario_title=scenario_title, 
            name=character_name
        ).first()

    @classmethod
    def find_characters(cls, scenario_title): 
        '''공개 여부 관계없이, 모든 캐릭터'''
        return Character.query.filter_by(
            scenario_title=scenario_title
        ).all()

    @classmethod
    def find_opened_characters(cls, scenario_title, is_opened=True): 
        '''is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물'''
        return Character.query.filter_by( 
            scenario_title=scenario_title, 
            is_opened=is_opened
        ).all()
    

class Element(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    character_idx = db.Column(db.Integer, db.ForeignKey('character.idx', ondelete='CASCADE'))
    
    character_name = db.Column(db.String(50), nullable=False)
    element = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)


    @classmethod
    def find_elements(cls, character_name):
        return Element.query.filter_by(character_name=character_name).all()
    
    # @classmethod
    # def find_element_by_element_name(cls, character_idx, element_name):
    #     return Element.query.filter_by(
    #         character_idx=character_idx,
    #         element=element_name
    #     ).first()