
from flask import Blueprint, request, jsonify, g
from models.user import User, UserSchema
from app import db
from lib.secure_route import secure_route
from lib.secure_route import secure_route

user_schema = UserSchema()

router = Blueprint(__name__, 'users')

@router.route('/register', methods=['POST'])
def register():
  user = user_schema.load(request.get_json())
  user.save()
  return user_schema.jsonify(user)

@router.route('/profile', methods=['GET'])
@secure_route
def profile():
  user = User.query.get(g.current_user.id)
  return user_schema.jsonify(user)


@router.route('/login', methods=['POST'])
def login():
  # * Does the user exist?
  data = request.get_json()
  # * Filter a user by an email
  user = User.query.filter_by(email=data['email']).first()

  # * 1) Check if a user came back with an email matching the 1 we sent.
  # * 2) Need to check the password against the one in the DB.
  if not user or not user.validate_password(data['password']):
    return jsonify( {'message': 'Unauthorized'} )

  # * Give them the token!
  # * installing pyjwt, then we add a method to our model again, to generate
  # * a token.
  token = user.generate_token()

  return jsonify( { 'token': token, 'message': 'Welcome back!' })


# ! One way of doing password confirmation.
# @router.route('/register', methods=['POST'])
# def index():
#   data = request.get_json()
#   if (data['password'] == data['password_confirmation']):
#     del data['password_confirmation']
#     user = user_schema.load(data)
#     user.save()
#     return user_schema.jsonify(user)
#   else:
#     return jsonify({ 'message': 'passwords dont match' })


