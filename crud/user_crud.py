from flask import jsonify
from models import User

def get_all_users():
  all_users = User.query.all()
  results = []
  for user in all_users:
    results.append(user.as_dict())
  # results = [user.as_dict() for user in all_users]
  return jsonify(results)