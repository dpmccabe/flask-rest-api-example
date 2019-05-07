from marshmallow import Schema, fields

from api.schemas.user_schema import UserSchema


class AuthLoginSchema(Schema):
    """JSON body schema for auth login endpoint"""
    id = fields.String(example='30651c69-6aad-4832-9889-c81ab773424e')


class AuthResponseSchema(Schema):
    """Response schema for JWT object"""
    token = fields.String(required=True, example=(
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.'
        'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    ))
    user = fields.Nested(UserSchema, required=True)
