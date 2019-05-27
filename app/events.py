from flask import Blueprint, jsonify, request, abort
from event_calendar.model.event import Event
import app.handlers as handlers

events = Blueprint('events',__name__)

search = handlers.search_for(Event)
get    = handlers.get_for(Event)
post   = handlers.post_for(Event)
update = handlers.update_for(Event)
delete = handlers.delete_for(Event)
