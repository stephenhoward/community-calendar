from flask import jsonify, request
from event_calendar.site_settings import site_settings

def search():
    return jsonify( site_settings )

def post(self):
    request.json

    return jsonify( site_settings )
