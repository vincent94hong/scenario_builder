from sqlalchemy import func
from app import db


class Country(db.Model):
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

    elements = db.relationship('CountryElement')

    @classmethod
    def find_country(cls, user_id, scenario_title, country_name):
        return Country.query.filter_by(
            user_id = user_id,
            scenario_title=scenario_title, 
            name=country_name
        ).first()

    @classmethod
    def find_countries(cls, user_id, scenario_title): 
        '''공개 여부 관계없이, 모든 캐릭터'''
        return Country.query.filter_by(
            user_id = user_id,
            scenario_title=scenario_title
        ).all()

    @classmethod
    def find_opened_countries(cls, user_id, scenario_title, is_opened=True): 
        '''is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물'''
        return Country.query.filter_by( 
            user_id = user_id,
            scenario_title=scenario_title, 
            is_opened=is_opened
        ).all()
    

class CountryElement(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    scenario_title = db.Column(db.String(100), nullable=False)
    country_idx = db.Column(db.Integer, db.ForeignKey('country.idx', ondelete='CASCADE'))
    country_name = db.Column(db.String(50), nullable=False)

    name = db.Column(db.String(100), nullable=False) # 중복조회(해당 유저의 시나리오에 한해서 unique)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())
    updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
    is_opened = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)


    @classmethod
    def find_element(cls, user_id, scenario_title, country_name, element_name):
        return CountryElement.query.filter_by(
            user_id=user_id,
            scenario_title=scenario_title,
            country_name=country_name,
            name=element_name
        ).first()

    @classmethod
    def find_elements(cls, user_id, scenario_title, country_name):
        return CountryElement.query.filter_by(
            user_id=user_id, 
            scenario_title=scenario_title,
            country_name=country_name
        ).all()
    
    @classmethod
    def find_countries_by_element(cls, user_id, scenario_title, element_name):
        return CountryElement.query.filter_by(
            user_id=user_id,
            scenario_title=scenario_title,
            name=element_name
        ).all().country_name