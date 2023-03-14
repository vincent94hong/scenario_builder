from flask import Blueprint, render_template

NAME = 'home'
bp = Blueprint(NAME, __name__)

@bp.route('/')
def home():
    return render_template('home.html')