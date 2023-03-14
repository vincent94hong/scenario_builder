from flask import Blueprint, render_template, redirect, url_for

NAME = 'my_scenario'
bp = Blueprint(NAME, __name__, url_prefix=f'/{NAME}')


@bp.route('/character')
def character():
    return render_template(f'{NAME}/character.html')


@bp.route('/item')
def item():
    return render_template(f'{NAME}/item.html')


@bp.route('/main_story')
def main_story():
    return render_template(f'{NAME}/main_story.html')