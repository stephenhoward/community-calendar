from flask import Blueprint, jsonify

categories = Blueprint('categories',__name__)

def search():
    return jsonify([
        {
            'id':   '12345',
            'info': [
                {
                    'language': 'en',
                    'name': 'Test'
                }
            ]
        }
    ])


def get(category):
    return jsonify(
        {
            'id':   '12345',
            'info': [
                {
                    'language': 'en',
                    'name': 'Test'
                }
            ]
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
