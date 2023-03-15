from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class ScenarioForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    character1 = StringField('Character1')


class CharacterForm(FlaskForm):
    character_name = StringField('Character Name', validators=[DataRequired()])
    old = IntegerField('Character Old')
    character1 = StringField('Character1')


class ItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    item_effect = StringField('Item Effect', validators=[DataRequired()])


class EpisodeForm(FlaskForm):
    episode_number = IntegerField('Episode Number', validators=[DataRequired()])
    episode_name = StringField('Episode Name', validators=[DataRequired()])
    episode_content = StringField('Episode Content', validators=[DataRequired()])