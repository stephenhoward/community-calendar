from flask import g, request
from event_calendar.model.event import Event
from datetime import datetime, timedelta
import app.handlers as handlers
from app.guards import guard_content

get     = guard_content( Event, method = handlers.get    )
post    = guard_content( Event, method = handlers.post   )
update  = guard_content( Event, method = handlers.update )
delete  = guard_content( Event, method = handlers.delete )
_search = guard_content( Event, method = handlers.search )

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
