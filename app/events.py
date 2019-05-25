from flask import Blueprint, jsonify
from event_calendar.model.event import Event

events = Blueprint('events',__name__)

def search():
    return jsonify([
        {
            'id':   '12345',
            'info': [
                {
                    'language': 'en',
                    'title': 'Test'
                }
            ]        
        }
    ])

def get(event):
    return jsonify(
        {
            'id':   '12345',
            'info': [
                {
                    'language': 'en',
                    'title': 'Test'
                }
            ]
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
