from flask import Blueprint, render_template, redirect, url_for, request
from app.forms.project_form import CharacterForm, ItemForm, EpisodeForm

NAME = 'project'
bp = Blueprint(NAME, __name__, url_prefix=f'/{NAME}')


@bp.route('/')
def item():
    form = ItemForm()
    return render_template('project.html', form=form)


@bp.route('/character', methods=['GET', 'POST'])
def character():
    form = CharacterForm()
    if request.method == 'POST' and form.validate_on_submit():
        character 
    return render_template('project.html', form=form)


@bp.route('/item')
def item():
    form = ItemForm()
    return render_template('project.html', form=form)


@bp.route('/main_story')
def main_story():
    form = EpisodeForm()
    return render_template('project.html', form=form)