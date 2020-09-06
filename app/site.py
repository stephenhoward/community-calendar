from flask import jsonify, request
from event_calendar.model.user import User
from event_calendar.model.org import Org
from event_calendar.site_settings import site_settings, languages
from event_calendar.model.image import SiteImage
from app.guards import guard_passthrough
import app.handlers as handlers


def search():
    return jsonify( site_settings )

def post():
    site_settings.update_values( **request.json )
    site_settings.save()

    return jsonify( site_settings )

def get_languages():
    return jsonify( languages )

def post_image():
    image = handlers.upload_file_for(SiteImage)
    return jsonify( image )

def initialize():
    if ( site_settings.needs_setup!= 1 ):
        abort(403)

    handler = guard_passthrough( User, method = handlers.post )

    return handler()
