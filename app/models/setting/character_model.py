from app import db
from app.models.scenario_model import Scenario
from sqlalchemy import func


class Character(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    scenario_idx = db.Column(db.Integer, db.ForeignKey('scenario.idx', ondelete='CASCADE'))
    name = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(100), nullable=False)
    elements = db.relationship('Element', backref=db.backref('characters'))

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), nullable=False, default=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)


    @classmethod
    def find_one_by_character_name(cls, char_name):
        return Character.query.filter_by(name=char_name).first()     
    

    @classmethod
    def find_all_characters_by_scenario_title(cls, scenario_title, only_name=False): 
        '''
        캐릭터의 공개여부와 관계없이,
        only_name = (True / False=default) : 등장인물 모델 (name, content만 dict 형태로 / 전부를) return.
        '''
        scenario_idx = Scenario.find_one_by_scenario_title(scenario_title).idx
        characters = Character.query.filter_by(scenario_idx=scenario_idx)
        if only_name == False:
            return characters
        
        contents = dict()
        scenario_idx = Scenario.find_idx_by_scenario_title(scenario_title)
        for character in characters:
            contents[character.name] = character.content
        return contents

    @classmethod
    def find_characters_by_scenario_title(cls, scenario_title, only_name=False, is_opened=True): 
        '''
        is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물의,
        only_name = (True / False=default) : 등장인물 모델 (name, content만 dict 형태로 / 전부를) return.
        '''
        scenario_idx = Scenario.find_one_by_scenario_title(scenario_title).idx
        characters = Character.query.filter_by(scenario_idx=scenario_idx, is_opened=is_opened)

        if only_name == False:
            return characters

        contents = dict()
        for character in characters:
            contents[character.name] = character.content
        return contents
    


class Element(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    char_idx = db.Column(db.Integer, db.ForeignKey('character.idx', ondelete='CASCADE'))
    content_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), nullable=False, default=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)


    @classmethod
    def find_all_elements_by_character_name(cls, char_name, only_name=False):
        '''
        캐릭터의 공개여부와 관계없이, 
        only_name = (True / False=default) : 속성 모델 (name, content만 dict 형태로 / 전부를) return.
        '''
        char_idx = Character.find_one_by_character_name(char_name).idx
        elements = Element.query.filter_by(char_idx=char_idx)

        if only_name == False:
            return elements

        contents = dict()
        contents['name'] = Character.name
        for element in elements:
            contents[element.content_name] = element.content
        return contents
    
    
    @classmethod
    def find_elements_by_character_name(cls, char_name, only_name=False, is_opened=True):
        '''
        is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물의,
        only_name = (True / False=default) : 등장인물 모델 (name, content만 dict 형태로 / 전부를) return.
        '''
        char_idx = Character.find_one_by_character_name(char_name).idx
        elements = Element.query.filter_by(char_idx=char_idx, is_opened=is_opened)

        if only_name == False:
            return elements

        contents = dict()
        contents['name'] = Character.name      
        for element in elements:
            contents[element.content_name] = element.content
        return contents
    