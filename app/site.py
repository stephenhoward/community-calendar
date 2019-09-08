from flask import jsonify, request
from event_calendar.site_settings import site_settings
from event_calendar.model.image import SiteImage
import app.handlers as handlers

post_image = handlers.upload_file_for(SiteImage)

def search():
    return jsonify( site_settings )

def post():
    request.json
    return jsonify( site_settings )
