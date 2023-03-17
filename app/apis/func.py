from flask import g, abort
from app.models.scenario_model import Scenario
from app.models.setting.character_model import Character, Element


class Admin():
    def admin_check():
        if g.user.id != 'admin':
            return abort(403)
        
    def check_user(id):
        if g.user.id != id:
            return abort(403)
        
 
class Find():
    def find_scenario_idx(scenario_title):
        scenario = Scenario.find_scenario(g.user.id, scenario_title)
        if not scenario:
            return abort(404)
        return scenario

#     def find_character_by_name(args):
#         scenario = Scenario.find_scenario(g.user.idx, args['scenario_title'])
#         if not scenario:
#             return abort(404)
#         return Character.query.filter_by(
#             scenario_idx=scenario.idx, 
#             name=args['character_name']
#         ).first()

#     def find_characters(args): 
#         '''공개 여부 관계없이, 모든 캐릭터'''
#         scenario = Scenario.find_scenario(g.user.idx, args['scenario_title'])
#         if not scenario:
#             return abort(404)
#         return Character.query.filter_by(
#             scenario_idx=scenario.idx
#         ).all()

#     def find_opened_characters(args): 
#         '''is_opened = (True=default / False) : (공개된 / 공개되지 않은) 등장인물'''
#         scenario = Scenario.find_scenario(g.user.idx, args['scenario_title'])
#         if not scenario:
#             return abort(404)
#         return Character.query.filter_by( 
#             scenario_idx=scenario.idx, 
#             is_opened=args['is_opened']
#         ).all()


# class ElementFunc():
#     def find_elements(args):
#         character = Character.find_character_by_name(
#             g.user.idx, 
#             args['scenario_title'], 
#             args['character_name']
#         )
#         if not character:
#             return abort(404)
#         return Element.query.filter_by(character_idx=character.idx).all()
    
#     @classmethod
#     def find_element_by_character_name(args):
#         character = Character.find_character_by_name(
#             g.user.idx, 
#             args['scenario_title'], 
#             args['character_name']
#         )
#         if not character:
#             return abort(403)
#         return Element.query.filter_by(
#             character_idx=character.idx,
#             element=args['element_name']
#         ).first()