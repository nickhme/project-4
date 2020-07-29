from app import db, ma
from models.base import BaseModel
from marshmallow import fields

class Ingredient(db.Model, BaseModel):

  __tablename__ = 'ingredients'

  name = db.Column(db.String(40), unique=True, nullable=True)

class IngredientSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = Ingredient
