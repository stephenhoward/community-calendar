from flask import Blueprint, jsonify, request, abort
from event_calendar.site_settings import site_settings

site = Blueprint('site',__name__)

def search():
    return jsonify( site_settings )

def post(self):
    request.json

    return jsonify( site_settings )
