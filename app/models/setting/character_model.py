from sqlalchemy import func
from app import db


class Character(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    scenario_idx = db.Column(db.Integer, db.ForeignKey('scenario.idx', ondelete='CASCADE'), nullable=False)
    scenario_title = db.Column(db.String(100), nullable=False)

    name = db.Column(db.String(50), nullable=False) # 중복조회(해당 유저의 시나리오에 한해서 unique)
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)

    elements = db.relationship('CharacterElement', backref=db.backref('character'))
    items = db.relationship('Item', secondary='items_characters', back_populates='characters')

    @classmethod
    def find_character(cls, user_id, scenario_title, character_name):
        return Character.query.filter_by(
            user_id=user_id,
            scenario_title=scenario_title, 
            name=character_name
        ).first()

    @classmethod
    def find_characters(cls, user_id, scenario_title): 
        '''공개 여부 관계없이, 모든 캐릭터'''
        return Character.query.filter_by(
            user_id=user_id,
            scenario_title=scenario_title
        ).all()

    @classmethod
    def find_opened_characters(cls, user_id, scenario_title, is_opened=True): 
        '''is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물'''
        return Character.query.filter_by( 
            user_id=user_id,
            scenario_title=scenario_title, 
            is_opened=is_opened
        ).all()


class CharacterElement(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    scenario_title = db.Column(db.String(100), nullable=False)
    character_idx = db.Column(db.Integer, db.ForeignKey('character.idx', ondelete='CASCADE'))
    character_name = db.Column(db.String(50), nullable=False)

    name = db.Column(db.String(100), nullable=False) # 중복조회(해당 유저의 시나리오에 한해서 unique)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)


    @classmethod
    def find_element(cls, user_id, scenario_title, character_name, element_name):
        return CharacterElement.query.filter_by(
            user_id=user_id,
            scenario_title=scenario_title,
            character_name=character_name,
            name=element_name
        ).first()

    @classmethod
    def find_elements(cls, user_id, scenario_title, character_name):
        return CharacterElement.query.filter_by(
            user_id=user_id, 
            scenario_title=scenario_title, 
            character_name=character_name
        ).all()

    @classmethod
    def find_characters_by_element(cls, user_id, scenario_title, element_name):
        return CharacterElement.query.filter_by(
            user_id=user_id,
            scenario_title=scenario_title,
            name=element_name
        ).all().character_name