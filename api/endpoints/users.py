from flask_rest_api import Blueprint, abort
from flask.views import MethodView
from flask_jwt_simple import get_jwt_identity

from api.lib.database import db
from api.models.user import User
from api.schemas.user_schema import UserSchema, UserPutSchema
from api.endpoints.auth import jwt_required


blp = Blueprint('users', 'users', url_prefix='/users',
                description='Operations on users')


@blp.route('/<id>')
class UserResource(MethodView):
    @jwt_required
    @blp.response(UserSchema)
    def get(self, id):
        """Get a single user by ID"""
        user = db.session.query(User).get(id)

        if user:
            # serialize and return
            user_schema = UserSchema()
            return user_schema.dump(user)

        return abort(404, message='User %s not found' % id)

    @jwt_required
    @blp.arguments(UserPutSchema, location='json')
    @blp.response(UserSchema)
    def put(self, data, id):
        """Update existing user"""
        # confirm current user is the one we are updating
        if get_jwt_identity() != id:
            return abort(403, message='Cannot update user %s' % id)

        user = db.session.query(User).get(id)

        if user:
            # update user record
            user.name = data['name']
            user.email = data['email']
            db.session.commit()

            # serialize and return
            user_schema = UserSchema()
            return user_schema.dump(user)

        return abort(404, message='User %s not found' % id)
