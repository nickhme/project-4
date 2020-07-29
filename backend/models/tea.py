from app import db, ma
from models.base import BaseModel, BaseSchema
from marshmallow import post_load, fields
from models.ingredient import Ingredient, IngredientSchema
# ! Import user to avoid circular errors.
from models.user import User

# ! This SQLAlchemy code will create a join table
# db.Column(db.Integer, db.ForeignKey('teas.id'))
teas_ingredients = db.Table('teas_ingredients',
  # ! We create the primary key from the (ingredient_id, tea_id), which is unique.
  db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True),
  db.Column('tea_id', db.Integer, db.ForeignKey('teas.id'), primary_key=True)
)


class Tea(db.Model, BaseModel):

  __tablename__ = 'teas'

  name = db.Column(db.String(40), nullable=False, unique=True)
  nicks_rating = db.Column(db.Integer, nullable=False)
  in_stock = db.Column(db.Boolean, nullable=False)
  description = db.Column(db.String(100))
  # ! In order to give my tea ingredients when I create it...
  ingredients = db.relationship('Ingredient', secondary=teas_ingredients, backref='teas')
  # Using the primary key of the users table
  drinker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  # ! not really using this backref
  drinker = db.relationship('User', backref='drinker_teas')


class Comment(db.Model, BaseModel):

  __tablename__ = 'comments'

  # Use text when its gonna be longer text.
  content = db.Column(db.Text, nullable=False)
  # ! in SQL, we added a foriegn key.
  # The argument passed to foreignkey should be tablename.identifier
  tea_id = db.Column(db.Integer, db.ForeignKey('teas.id'))
  tea = db.relationship('Tea', backref='comments')

class CommentSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = Comment
    load_instance = True



class TeaSchema(ma.SQLAlchemyAutoSchema, BaseSchema):

  class Meta:
    model = Tea # or whatever model we're talking about
    load_instance = True

  # * This tells our TeaSchema about comments!!!!
  comments = fields.Nested('CommentSchema', many=True)
   # * This tells our TeaSchema about ingredients!!!!
  ingredients = fields.Nested('IngredientSchema', many=True)
  # ! This will include the user on the response
  drinker = fields.Nested('UserSchema', only=('id', 'username'))
  drinker_id = fields.Integer()