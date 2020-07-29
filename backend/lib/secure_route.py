from flask import request, jsonify, g
import jwt
from environment.config import secret
from models.user import User
from functools import wraps

def secure_route(fun):
  # ! Add fix to secure route.
  @wraps(fun)
  def wrapper(*args, **kwargs):
    # ! Do my secure route stuff!
    raw_token = request.headers['Authorization']
    clean_token = raw_token.replace('Bearer ', '')

    # * Decoding the token, getting out my juicy info.
    try:
      payload = jwt.decode(clean_token, secret)
      # ! g is a global object that flask gives us.
      print('This far...')
      g.current_user = User.query.get(payload['sub'])
    except jwt.ExpiredSignatureError:
      # ! Token has expired
      return jsonify({ 'message': 'Token has expired' }), 401
    except Exception as e:
      # ! Any error that's happened INSIDE the try block
      return jsonify({ 'message': 'Unauthorized' }), 401

    return fun(*args, **kwargs)

  return wrapper

