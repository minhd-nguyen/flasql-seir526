from models import app, User
from flask import jsonify, request
from crud.user_crud import get_all_users

@app.route('/')
def home():
  return jsonify(message='Welcome Home')

@app.route('/randomUser')
def rand_user():
  first_user = User.query.first()
  print(f'👿 {first_user}')
  return jsonify(user=first_user.as_dict())

@app.route('/users', methods=['GET', 'POST'])
def user_index_create():
  if request.method == 'GET':
    return get_all_users()
  else:
    return jsonify(message='route coming soon')