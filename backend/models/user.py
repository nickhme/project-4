from app import db, ma, bcrypt
from models.base import BaseModel, BaseSchema
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields, validates_schema, ValidationError, post_dump
from datetime import *
from environment.config import secret
import jwt

class User(db.Model, BaseModel):

  __tablename__ = 'users'

  username = db.Column(db.String(20), nullable=False, unique=True)
  email = db.Column(db.String(128), nullable=True, unique=True)
  password_hash = db.Column(db.String(128), nullable=True)

  # ! This field will exist temporarily when posting, but does not
  # ! Get stored in the DB
  @hybrid_property
  def password(self):
    pass

  # * The first part of this has to match a hybrid property function
  @password.setter
  def password(self, password_plaintext):
    # ! Use bcrypt now to encrypt my password.
    self.password_hash = bcrypt.generate_password_hash(password_plaintext).decode('utf-8')

  def validate_password(self, password_plaintext):
    # * Compare the password the user is logging in with, with the hashed
    # * password we've stored in the database.
    return bcrypt.check_password_hash(self.password_hash, password_plaintext)

  def generate_token(self):
    # ! Stuff we need to put in the token.
    payload = {
      # Expiry date, helped out by datetime (python built in)
      # * Expire in 1 days time.
      'exp': datetime.utcnow() + timedelta(days=1),
      # Current time when we create the token
      'iat': datetime.utcnow(),
      # This is just the user id
      'sub': self.id
    }

    token = jwt.encode(
      payload,
      secret,
      # ! Algo it uses to encode, should be HS256
      'HS256'
    ).decode('utf-8')

    return token


class UserSchema(ma.SQLAlchemyAutoSchema, BaseSchema):

  @validates_schema
  def check_passwords_match(self, data, **kwargs):
    if data['password'] != data['password_confirmation']:
      # ! Provided by marshmallow.
      # This what marshmallow does when you don't provide the right properties
      # when trying to serialise
      raise ValidationError(
        'Passwords dont match',
        'password_confirmation'
      )

  # ! I can give my schema any fields I like myself!
  password = fields.String(required=True)
  password_confirmation = fields.String(required=True)
  drinker_teas = fields.Nested('TeaSchema', many=True)

  class Meta:
    model = User
    load_instance = True
    # ! We can exclude fields so they're never sent back
    exclude = ('password_hash',)
    load_only = ('email', 'password')