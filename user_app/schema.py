
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from flask_marshmallow import Marshmallow
from user_app.models import User, db

from marshmallow import (
    fields,
    validate,
    ValidationError,
)

# ma = Marshmallow()

# Schema
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db
        load_instance = True
    
    # Override password field to add extra validations and load_only
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=36)], load_only=True
    )


def get_user_schema():
    return UserSchema()

def list_users_schema():
    return UserSchema(many=True)