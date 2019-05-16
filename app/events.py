from flask import Blueprint, jsonify

events = Blueprint('events',__name__)

def search():
    return jsonify([
        { 'title': 'Test',
          'id':    '12345'
        }
    ])

def get(event):
    return jsonify(
        { 'title': 'Test',
          'id':    '12345'
        }
    )

def post(event):
    return jsonify(
        ok = 1
    )

def update(event):
    return jsonify(
        ok = 1
    )
