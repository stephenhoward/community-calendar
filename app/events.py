from flask import g, request
from event_calendar.model.event import Event
from event_calendar.model.image import EventImage
from datetime import datetime
import app.handlers as handlers

get     = handlers.get_for(Event)
post    = handlers.post_for(Event)
update  = handlers.update_for(Event)
delete  = handlers.delete_for(Event)
_search = handlers.search_for(Event)

search_parameters = {
    'from':       ( lambda value: ( 'start[ge]', datetime.strptime(value, "%Y-%m-%d") ) ),
    'to':         ( lambda value: ( 'end[le]',   datetime.strptime(value, "%Y-%m-%d") ) ),
    'categories': ( lambda value: ( ) )
}

def search():
    query = {};

    for arg in request.args:
        if len( request.args[arg] ):
            if ( arg in search_parameters ):
                (key,value) = search_parameters[arg]( request.args[arg] )
                query[key] = value
            else:
                query[arg] = request.args[arg]

    g.search_args = query

    return _search()

post_image = handlers.upload_file_for(EventImage)
get_image  = handlers.serve_file_for(EventImage)