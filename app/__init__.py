from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)


    '''configuration'''
    from .configs import DevelopmentConfig, ProductionConfig
    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()
    print('run with:', config)
    app.config.from_object(config)


    '''CSRFProtect'''
    csrf.init_app(app)


    '''Database Init'''
    db.init_app(app)
    migrate.init_app(app, db)


    '''routes'''
    from app.routes import home_route, auth_route, my_scenario_route
    app.register_blueprint(home_route.bp)
    app.register_blueprint(auth_route.bp)
    app.register_blueprint(my_scenario_route.bp)


    return app