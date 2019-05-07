from flask_rest_api import Blueprint, abort
from flask.views import MethodView
from flask_jwt_simple import create_jwt, jwt_required as orig_jwt_required
from functools import wraps
from flask import current_app
from flask_jwt_simple import JWTManager

from api.lib.database import db
from api.models.user import User
from api.schemas.auth_schema import AuthLoginSchema, AuthResponseSchema
from api.schemas.user_schema import UserSchema


jwt = JWTManager()


def jwt_required(func):
    """
    Requre a valid JSON Web Token for the wrapped function
    """

    # apply the decorator
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('config')
        print(current_app.config['TESTING'])
        if current_app.config['TESTING']:
            # skip for test suite
            auth_required_func = func
        else:
            # use original jwt_required function
            auth_required_func = orig_jwt_required(func)

        return auth_required_func(*args, **kwargs)

    # add header requirements to API docs (i.e. Swagger)
    parameters = {
        'name': 'Authorization',
        'in': 'header',
        'description': 'Bearer <access_token>',
        'required': 'true'
    }

    wrapper._apidoc = getattr(func, '_apidoc', {})
    wrapper._apidoc.setdefault('parameters', []).append(parameters)

    return wrapper


blp = Blueprint('auth', 'auth', url_prefix='/auth',
                description='Authorization endpoint')


@blp.route('/login')
class AuthResource(MethodView):
    @blp.arguments(AuthLoginSchema, location='json')
    @blp.response(AuthResponseSchema)
    def post(self, body):
        """Generate a web token for user if they exist"""
        user = db.session.query(User).get(body['id'])

        if not user:
            abort(403, message='User not found')

        token = create_jwt(identity=user.id)

        user_schema = UserSchema()
        user = user_schema.dump(user)

        return {'token': token, 'user': user}
