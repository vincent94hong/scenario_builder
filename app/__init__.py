from flask import Flask, g
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)


    '''Configuration'''
    from .configs import DevelopmentConfig, ProductionConfig
    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()
    print('run with:', config)
    app.config.from_object(config)


    '''jwt tocken'''
    jwt = JWTManager(app)


    '''CSRFProtect'''
    csrf.init_app(app)


    '''Database Init'''
    db.init_app(app)
    migrate.init_app(app, db)


    '''Routes'''
    from app.routes import home_route, auth_route # project_route
    app.register_blueprint(home_route.bp)
    app.register_blueprint(auth_route.bp)
    # app.register_blueprint(project_route.bp)


    '''Request hook'''
    @app.before_request
    def before_request():
        g.db = db.session    

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()


    return app