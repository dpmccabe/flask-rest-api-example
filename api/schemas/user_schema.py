from marshmallow import Schema, fields

from api.lib.api import api


@api.definition('User')
class UserSchema(Schema):
    """Marshmallow schema for serializing a user instance"""
    id = fields.String(required=True, example='30651c69-6aad-4832-9889-c81ab773424e')
    name = fields.String(required=True, example='John Doe')
    email = fields.Email(required=True, example='john_doe@harvard.edu')


class UserPutSchema(Schema):
    """Marshmallow schema for updating a user instance"""
    name = fields.String(required=True, example='John Doe')
    email = fields.Email(required=True, example='john_doe@harvard.edu')
