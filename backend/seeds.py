from app import app, db

# ! use the . to drill down inside a module
# ? importing my model here.
from models.tea import Tea, Comment, Ingredient
from models.user import User

# ! in here, we're connecting our database. 'with' will cleanup connections
# ! once we're done.
with app.app_context():
  # ? This code will seed stuff into the database.
  # ? its sqlalchemy code.
  db.drop_all() # drop all tables in database
  db.create_all() # create all tables in database

  # ! Create my ingredients
  honey = Ingredient(name='Honey')
  cinnamon = Ingredient(name='Cinnamon')
  leaves = Ingredient(name='tea leaves')

  nick = User(
    username="nick",
    email="nick",
    password="nick"
  )

  db.session.add(nick)
  db.session.commit()

  # Create some teas
  chai = Tea(
    name="chai",
    nicks_rating=4,
    in_stock=True,
    ingredients=[honey, cinnamon, leaves],
    drinker=nick
  )
  rooibos = Tea(
    name="rooibos",
    nicks_rating=5,
    in_stock=True,
    description="tasty",
    ingredients=[leaves]
  )

  comment1 = Comment(
    content='I will do a better job explaining 1-M with SQLAlchemy next time!',
    tea=rooibos
  )

  comment2 = Comment(
    content='One more time',
    tea=chai
  )

  # ! Add the teas to our 'open session'
  db.session.add(chai)
  db.session.add(rooibos)
  db.session.add(comment1)
  db.session.add(comment2)

  # # ! Save the data to the database
  db.session.commit()
