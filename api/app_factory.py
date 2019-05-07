from flask import Flask

from api.config import config


def create_app(config_name):
    app = Flask('Backend')
    app.config.from_object(config[config_name])

    from api.lib.database import db
    db.init_app(app)

    app.config['OPENAPI_URL_PREFIX'] = ''
    app.config['API_VERSION'] = '1.0.0'
    app.config['OPENAPI_VERSION'] = '2.0'

    # use JSON web tokens for protected endpoints
    from api.endpoints.auth import jwt
    jwt.init_app(app)

    # run Swagger and ReDoc in development
    if app.config['FLASK_ENV'] == 'development':
        app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
        app.config['OPENAPI_SWAGGER_UI_VERSION'] = '3.22.0'
        app.config['OPENAPI_REDOC_PATH'] = '/redoc'

    # init API and endpoints
    from api.lib.api import api
    api.init_app(app)

    # add endpoints
    from api.endpoints.auth import blp as auth_blp
    from api.endpoints.users import blp as users_blp

    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)

    return app
