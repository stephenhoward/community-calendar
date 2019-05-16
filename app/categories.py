from flask import Blueprint, jsonify

categories = Blueprint('categories',__name__)

def search():
    return jsonify([
        { 'name': 'Test',
          'id':   '12345'
        }
    ])


def get(category):
    return jsonify(
        { 'name': 'Test',
          'id':   '12345'
        }
    )

def post(category):
    return jsonify(
        ok = 1
    )

def update(category):
    return jsonify(
        ok = 1
    )
