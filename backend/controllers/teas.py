
from flask import Blueprint, request, jsonify, g
from models.tea import Tea, TeaSchema, CommentSchema
from app import db
from lib.secure_route import secure_route
from marshmallow import ValidationError

tea_schema = TeaSchema()
comment_schema = CommentSchema()

router = Blueprint(__name__, 'teas')

@router.route('/teas', methods=['GET'])
def index():
  teas = Tea.query.all()
  return tea_schema.jsonify(teas, many=True), 200

@router.route('/teas/<int:id>', methods=['GET'])
def show(id):
  tea = Tea.query.get(id)

  if not tea:
    return jsonify({'message': 'Tea not in stock'}), 404

  return tea_schema.jsonify(tea), 200

@router.route('/teas', methods=['POST'])
@secure_route
def create():
  json_im_posting = request.get_json()
  json_im_posting['drinker_id'] = g.current_user.id

  try:
    tea = tea_schema.load(json_im_posting)
  except ValidationError as e:
    return jsonify({ 'errors': e.messages, 'message': 'Something went wrong!' })

  tea.save()
  return tea_schema.jsonify(tea), 201

@router.route('/teas/<int:id>', methods=['PUT'])
@secure_route
def update(id):
  existing_tea = Tea.query.get(id)
  tea = tea_schema.load(request.get_json(), instance=existing_tea, partial=True)

  print(tea.drinker)

  # ! Before we save the tea, check if this is MY tea!
  if tea.drinker != g.current_user:
    return jsonify({'message': 'Unauthorized'}), 401

  tea.save()
  return tea_schema.jsonify(tea), 201

@router.route('/teas/<int:id>', methods=['DELETE'])
@secure_route
def remote(id):
  tea = Tea.query.get(id)
  tea.remove()
  return jsonify({ 'message': 'Tea removed successfully' })

@router.route('/teas/<int:tea_id>/comments', methods=['POST'])
def comment_create(tea_id):
  comment_data = request.get_json()
  tea = Tea.query.get(tea_id)
  comment = comment_schema.load(comment_data)
  # At this stage, comment has only comment.content !!!
  # ! This tells sqlalchemy which tea our comment is associated with
  comment.tea = tea
  # At this stage, the comment is complete
  comment.save()
  return comment_schema.jsonify(comment)
