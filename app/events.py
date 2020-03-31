from flask import g, request
from event_calendar.model.event import Event
from datetime import datetime, timedelta
import app.handlers as handlers

get     = handlers.get_for(Event)
post    = handlers.post_for(Event)
update  = handlers.update_for(Event)
delete  = handlers.delete_for(Event)
_search = handlers.search_for(Event)

search_parameters = {
    'from':       ( lambda value: ( 'start[ge]', datetime.strptime(value, "%Y-%m-%d") ) ),
    'to':         ( lambda value: ( 'start[le]', datetime.strptime(value, "%Y-%m-%d") + timedelta( hours=23, minutes=59, seconds=59 ) ) ),
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

add_comment    = handlers.post_comment_for(Event)
get_comments   = handlers.get_comments_for(Event)
update_comment = handlers.update_comment_for(Event)